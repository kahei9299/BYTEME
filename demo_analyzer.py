#!/usr/bin/env python3
"""
TikTok Content Analyzer - Demo Version
Pre-trained YOLOv8 for content analysis
No custom training required
"""

import cv2
import torch
import numpy as np
from ultralytics import YOLO
import json
from pathlib import Path
import time
from collections import defaultdict, Counter

class InstantTikTokAnalyzer:
    """Ready-to-use TikTok content analyzer using YOLOv8 pre-trained model"""

    def __init__(self):
        print("🚀 Initializing TikTok Content Analyzer...")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"📱 Using device: {self.device}")

        # Load YOLOv8 pre-trained model
        print("📦 Loading YOLOv8 model...")
        self.model = YOLO('yolov8n.pt')  # auto-download if not found

        print("✅ Analyzer ready!")

    def analyze_video(self, video_path: str, sample_rate: int = 30) -> dict:
        """
        Analyze a video and return metrics, frame data, and insights
        Args:
            video_path (str): path to the video file
            sample_rate (int): analyze every N frames
        """
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        print(f"🎥 Analyzing video: {video_path}")
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0

        frame_data = []
        object_timeline = defaultdict(list)
        scene_changes = []
        visual_complexity = []

        frame_idx = 0
        analyzed_frames = 0
        prev_hist = None
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % sample_rate == 0:
                results = self.model(frame, verbose=False)
                frame_analysis = self._analyze_frame(frame, results[0], frame_idx, fps)
                frame_data.append(frame_analysis)

                # Track objects
                for det in frame_analysis['detections']:
                    object_timeline[det['class']].append({
                        'timestamp': frame_idx / fps,
                        'confidence': det['confidence'],
                        'frame_idx': frame_idx
                    })

                # Scene change detection
                curr_hist = self._calculate_histogram(frame)
                if prev_hist is not None and self._detect_scene_change(prev_hist, curr_hist):
                    scene_changes.append(frame_idx / fps)
                prev_hist = curr_hist

                # Visual complexity
                visual_complexity.append(self._calculate_visual_complexity(frame, frame_analysis['detections']))

                analyzed_frames += 1
                if analyzed_frames % 10 == 0:
                    progress = (frame_idx / total_frames) * 100
                    print(f"⏳ Progress: {progress:.1f}% ({analyzed_frames} frames analyzed)")

            frame_idx += 1

        cap.release()
        analysis_time = time.time() - start_time
        print(f"✅ Analysis complete! {analysis_time:.1f}s for {analyzed_frames} frames")

        metrics = self._calculate_content_metrics(frame_data, object_timeline, scene_changes, visual_complexity, duration)

        return {
            'video_info': {
                'path': video_path,
                'total_frames': total_frames,
                'fps': fps,
                'duration': duration,
                'analyzed_frames': analyzed_frames
            },
            'metrics': metrics,
            'frame_data': frame_data,
            'object_timeline': dict(object_timeline),
            'scene_changes': scene_changes,
            'visual_complexity': visual_complexity,
            'analysis_time': analysis_time
        }

    def _analyze_frame(self, frame, result, frame_idx, fps):
        """Analyze individual frame using YOLO detections"""
        detections = []
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                class_id = int(box.cls[0].cpu().numpy())
                detections.append({
                    'class': self.model.names[class_id],
                    'class_id': class_id,
                    'confidence': float(confidence),
                    'bbox': [float(x1), float(y1), float(x2), float(y2)],
                    'area': float((x2-x1) * (y2-y1)),
                    'center': [float((x1+x2)/2), float((y1+y2)/2)]
                })

        return {
            'frame_idx': frame_idx,
            'timestamp': frame_idx / fps,
            'detections': detections,
            'num_objects': len(detections),
            'frame_shape': frame.shape
        }

    def _calculate_histogram(self, frame):
        """Calculate HSV histogram for scene change detection"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1, 2], None, [50, 60, 60], [0, 180, 0, 256, 0, 256])
        return cv2.normalize(hist, hist).flatten()

    def _detect_scene_change(self, prev_hist, curr_hist, threshold=0.3):
        """Detect scene change based on histogram correlation"""
        return cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_CORREL) < (1.0 - threshold)

    def _calculate_visual_complexity(self, frame, detections):
        """Estimate visual complexity (edges + color variance + object density)"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (frame.shape[0] * frame.shape[1])
        color_std = np.std(frame)
        object_density = len(detections) / 20
        return min(1.0, edge_density*2 + color_std/100 + object_density)

    def _calculate_content_metrics(self, frame_data, object_timeline, scene_changes, visual_complexity, duration):
        """Compute all 5 key metrics and overall score"""
        if not frame_data or duration <= 0:
            return self._default_metrics()

        metrics = {}

        # Accuracy
        info_objs = ['book', 'laptop', 'tv', 'cell phone']
        info_count = sum(len(object_timeline.get(obj, [])) for obj in info_objs)
        person_presence = len(object_timeline.get('person', [])) / len(frame_data)
        metrics['accuracy'] = max(0.3, min(1.0, (info_count/50)*0.6 + person_presence*0.4))

        # Plot Homogeneity (monotony)
        scene_rate = len(scene_changes)/duration
        complexity_var = np.std(visual_complexity) if visual_complexity else 0
        object_var = np.std([f['num_objects'] for f in frame_data])
        variation_score = min(1.0, scene_rate*0.4 + complexity_var*0.3 + (object_var/10)*0.3)
        metrics['plot_homogeneity'] = max(0.0, 1.0 - variation_score)

        # Comedic value
        activity_objs = ['sports ball','frisbee','skateboard','surfboard','kite']
        fun_objs = ['cake','pizza','donut','teddy bear']
        activity_count = sum(len(object_timeline.get(obj, [])) for obj in activity_objs)
        fun_count = sum(len(object_timeline.get(obj, [])) for obj in fun_objs)
        avg_complexity = np.mean(visual_complexity) if visual_complexity else 0
        metrics['comedic_value'] = min(1.0, (activity_count/20)*0.3 + (fun_count/10)*0.3 + avg_complexity*0.4)

        # Theatrism
        person_frames = len(object_timeline.get('person', []))
        total_frames = len(frame_data)
        person_consistency = person_frames/total_frames if total_frames > 0 else 0
        scene_dynamism = min(1.0, len(scene_changes)/5)
        avg_objects = np.mean([f['num_objects'] for f in frame_data])
        visual_richness = min(1.0, avg_objects/8)
        metrics['theatrism'] = person_consistency*0.4 + scene_dynamism*0.3 + visual_richness*0.3

        # Plot coherence
        common_objs = [obj for obj,timeline in object_timeline.items() if len(timeline)>total_frames*0.3]
        obj_consistency = len(common_objs)/max(1,len(object_timeline))
        ideal_scene_changes = duration/10
        scene_coherence = max(0,1-abs(len(scene_changes)-ideal_scene_changes)/max(1,ideal_scene_changes))
        metrics['plot_coherence'] = obj_consistency*0.6 + scene_coherence*0.4

        # Overall score
        weights = {'accuracy':0.25,'plot_homogeneity':0.15,'comedic_value':0.2,'theatrism':0.2,'plot_coherence':0.2}
        metrics['overall_score'] = sum(metrics[m]*weights[m] for m in weights)

        return metrics

    def _default_metrics(self):
        """Return default metrics if analysis fails"""
        return {
            'accuracy': 0.5, 'plot_homogeneity': 0.5,
            'comedic_value': 0.3, 'theatrism': 0.4,
            'plot_coherence': 0.5, 'overall_score': 0.44
        }

    def generate_report(self, results: dict, save_path: str = None):
        """Generate structured report with insights and recommendations"""
        report = {
            'summary': {
                'video': results['video_info']['path'],
                'duration': f"{results['video_info']['duration']:.1f} seconds",
                'overall_score': f"{results['metrics']['overall_score']:.3f}",
                'analysis_time': f"{results['analysis_time']:.1f} seconds"
            },
            'detailed_metrics': results['metrics'],
            'insights': self._generate_insights(results),
            'recommendations': self._generate_recommendations(results['metrics'])
        }

        if save_path:
            with open(save_path,'w') as f:
                json.dump(report,f,indent=2)
            print(f"📄 Report saved to: {save_path}")

        return report

    def _generate_insights(self, results):
        insights = []
        counts = Counter({obj: len(timeline) for obj, timeline in results['object_timeline'].items()})
        if counts:
            top_objs = counts.most_common(3)
            insights.append(f"Most frequent objects: {', '.join([f'{obj} ({c})' for obj,c in top_objs])}")
        # Scene analysis
        scene_count = len(results['scene_changes'])
        duration = results['video_info']['duration']
        if scene_count:
            avg_scene_len = duration/(scene_count+1)
            insights.append(f"Average scene length: {avg_scene_len:.1f}s ({scene_count} changes)")
        # Visual complexity
        if results['visual_complexity']:
            insights.append(f"Average visual complexity: {np.mean(results['visual_complexity']):.3f}")
        # Person presence
        person_frames = results['object_timeline'].get('person', [])
        if person_frames:
            presence_pct = len(person_frames)/len(results['frame_data'])*100
            insights.append(f"Person visible in {presence_pct:.1f}% of frames")
        return insights

    def _generate_recommendations(self, metrics):
        recs = []
        if metrics['accuracy'] < 0.6:
            recs.append("Add educational or informational content to improve accuracy")
        if metrics['plot_homogeneity'] > 0.7:
            recs.append("Introduce more visual variety to reduce monotony")
        if metrics['comedic_value'] < 0.4:
            recs.append("Add engaging or dynamic elements for entertainment value")
        if metrics['theatrism'] < 0.5:
            recs.append("Increase consistent person presence and visual richness")
        if metrics['plot_coherence'] < 0.6:
            recs.append("Improve narrative flow with consistent visual elements")
        if not recs:
            recs.append("Content shows good overall quality across all metrics!")
        return recs

    def demo_analysis(self, video_path: str):
        """Run full analysis demo and print summary"""
        print("="*60)
        print("🎬 TIKTOK CONTENT ANALYZER DEMO")
        print("="*60)
        try:
            results = self.analyze_video(video_path)
            report = self.generate_report(results)

            # Print summary
            print("\n📊 ANALYSIS RESULTS")
            for metric, score in results['metrics'].items():
                if isinstance(score,float):
                    print(f"{metric.replace('_',' ').title()}: {score:.3f}")

            print("\n💡 INSIGHTS")
            for insight in report['insights']:
                print(f"• {insight}")

            print("\n🚀 RECOMMENDATIONS")
            for rec in report['recommendations']:
                print(f"• {rec}")

            # Reward tier
            overall = results['metrics']['overall_score']
            if overall >= 0.8: tier, multiplier = "🥇 GOLD", 2.5
            elif overall >= 0.6: tier, multiplier = "🥈 SILVER", 1.5
            else: tier, multiplier = "🥉 BRONZE", 1.0
            base_reward = 100
            print(f"\n💰 REWARD TIER: {tier} ({overall:.3f}) -> {base_reward*multiplier:.0f} credits")
            return results

        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            return None

def main():
    """Main interactive demo"""
    print("🎬 TikTok Content Analyzer - YOLOv8 Demo")
    analyzer = InstantTikTokAnalyzer()

    print("Demo options:")
    print("1. Analyze your own video")
    print("2. Download and analyze sample video")
    print("3. Batch analyze multiple videos")

    choice = input("Choose option (1-3): ").strip()
    if choice=="1":
        path = input("Enter video path: ").strip()
        if Path(path).exists(): analyzer.demo_analysis(path)
        else: print("❌ Video not found")
    elif choice=="2":
        print("📥 Download a sample video (e.g., https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4)")
        path = input("Enter path to video: ").strip()
        if Path(path).exists(): analyzer.demo_analysis(path)
        else: print("❌ Video not found")
    elif choice=="3":
        folder = input("Enter folder path: ").strip()
        if Path(folder).exists():
            files = list(Path(folder).glob("*.mp4"))
            if files:
                print(f"Found {len(files)} .mp4 files. Analyzing first 3...")
                for f in files[:3]: analyzer.demo_analysis(str(f))
            else: print("❌ No .mp4 files found")
        else: print("❌ Folder not found")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()