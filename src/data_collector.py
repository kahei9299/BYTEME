import os
import pandas as pd
import cv2
import numpy as np

class TikTokDataCollector:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.videos_dir = os.path.join(data_dir, "videos")
        self.annotations_file = os.path.join(data_dir, "annotations.csv")
        
        # Create directories if they don't exist
        os.makedirs(self.videos_dir, exist_ok=True)
        
    def add_video(self, video_path, scores, description=""):
        """Add a video with manual scores"""
        # Copy video to data directory
        video_name = os.path.basename(video_path)
        dest_path = os.path.join(self.videos_dir, video_name)
        
        # For now, just record the path
        video_data = {
            'video_name': video_name,
            'video_path': dest_path,
            'description': description,
            'accuracy': scores.get('accuracy', 0),
            'homogeneity': scores.get('homogeneity', 0),
            'comedy': scores.get('comedy', 0),
            'theatrism': scores.get('theatrism', 0),
            'coherence': scores.get('coherence', 0)
        }
        
        # Save to CSV
        if os.path.exists(self.annotations_file):
            df = pd.read_csv(self.annotations_file)
            df = pd.concat([df, pd.DataFrame([video_data])], ignore_index=True)
        else:
            df = pd.DataFrame([video_data])
        
        df.to_csv(self.annotations_file, index=False)
        
        print(f"Added video: {video_name}")
        
    def get_dataset(self):
        """Load the dataset"""
        if os.path.exists(self.annotations_file):
            return pd.read_csv(self.annotations_file)
        return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    collector = TikTokDataCollector()
    
    # Add your first video with manual scores
    scores = {
        'accuracy': 8,
        'homogeneity': 6,
        'comedy': 7,
        'theatrism': 5,
        'coherence': 9
    }
    
    # collector.add_video("path/to/your/video.mp4", scores, "Funny cooking tutorial")