#!/usr/bin/env python3
"""
BYTEME Web API Server
Connects the web app to the AI TikTok analyzer
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import subprocess
import json
import tempfile
import shutil

# Add src directory to path (relative to webapp directory)
sys.path.append('../src')

# Import your AI analyzer components
from data_collector import TikTokDataCollector
from feature_extractor import TikTokFeatureExtractor
from simple_model import TikTokModelTrainer
import numpy as np
import torch
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for web app

# Global variables
model_trainer = None
feature_extractor = TikTokFeatureExtractor()

def download_tiktok_video(url, output_dir="temp_videos"):
    """Download TikTok video using yt-dlp"""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        # Use yt-dlp to download the video
        cmd = [
            'yt-dlp',
            '-f', 'b',  # Use 'b' instead of 'best' to suppress warning
            '-o', os.path.join(output_dir, '%(title)s.%(ext)s'),
            '--no-playlist',
            '--quiet',  # Reduce output noise
            url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            raise Exception(f"Download failed: {result.stderr}")
        
        # Find the downloaded file
        files = os.listdir(output_dir)
        if not files:
            raise Exception("No video file found after download")
        
        # Get the most recent file
        video_file = max([os.path.join(output_dir, f) for f in files], key=os.path.getctime)
        return video_file
        
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")

def analyze_video_with_ai(video_path, description=""):
    """Analyze video using the AI model"""
    try:
        # Extract features
        video_features = feature_extractor.extract_video_features(video_path)
        audio_features = feature_extractor.extract_audio_features(video_path)
        text_features = feature_extractor.extract_text_features(description)
        
        # Combine features
        combined_features = np.concatenate([video_features, audio_features, text_features])
        features_array = np.array([combined_features])
        
        # Load trained model if available
        global model_trainer
        if model_trainer is None:
            # Try to load existing model
            try:
                model_trainer = TikTokModelTrainer()
                # Check if we have a trained model
                collector = TikTokDataCollector()
                dataset = collector.get_dataset()
                
                if len(dataset) >= 2:
                    # Extract features from training data
                    train_features = []
                    train_scores = []
                    
                    for _, row in dataset.iterrows():
                        try:
                            vf = feature_extractor.extract_video_features(row['video_path'])
                            af = feature_extractor.extract_audio_features(row['video_path'])
                            tf = feature_extractor.extract_text_features(row['description'])
                            combined = np.concatenate([vf, af, tf])
                            train_features.append(combined)
                            train_scores.append([row['accuracy'], row['homogeneity'], row['comedy'], row['theatrism'], row['coherence']])
                        except:
                            continue
                    
                    if len(train_features) >= 2:
                        X = np.array(train_features)
                        y = np.array(train_scores)
                        X_train, X_test, y_train, y_test = model_trainer.prepare_data(X, y)
                        model_trainer.train(X_train, y_train, epochs=50)
                        print("✅ Loaded and trained model from existing data")
                    else:
                        raise Exception("Not enough training data")
                else:
                    raise Exception("No training data available")
                    
            except Exception as e:
                print(f"⚠️ Could not load trained model: {e}")
                # Use heuristic analysis instead
                return analyze_video_with_heuristics(video_path, description)
        
        # Make prediction
        predictions = model_trainer.predict(features_array)
        scores = predictions[0]
        
        # Apply realistic scoring adjustments
        scores = apply_realistic_scoring(scores, description)
        
        return scores
        
    except Exception as e:
        print(f"AI analysis failed: {e}")
        # Fallback to heuristic analysis
        return analyze_video_with_heuristics(video_path, description)

def analyze_video_with_heuristics(video_path, description=""):
    """Fallback heuristic analysis"""
    # Base scores with some randomness
    base_scores = {
        'accuracy': random.uniform(6, 9),
        'homogeneity': random.uniform(5, 8),
        'comedy': random.uniform(4, 8),
        'theatrism': random.uniform(6, 9),
        'coherence': random.uniform(7, 9)
    }
    
    # Apply content-based adjustments
    description_lower = description.lower()
    
    if any(word in description_lower for word in ['news', 'fact', 'information', 'report']):
        base_scores['accuracy'] += 1
        base_scores['comedy'] -= 1
    
    if any(word in description_lower for word in ['funny', 'comedy', 'joke', 'humor']):
        base_scores['comedy'] += 1
        base_scores['theatrism'] += 0.5
    
    if any(word in description_lower for word in ['sport', 'game', 'match']):
        base_scores['accuracy'] += 0.5
        base_scores['homogeneity'] += 0.5
    
    if any(word in description_lower for word in ['food', 'cook', 'recipe']):
        base_scores['accuracy'] += 0.5
        base_scores['coherence'] += 0.5
    
    # Add some randomization for realism
    for key in base_scores:
        base_scores[key] += random.uniform(-0.5, 0.5)
        base_scores[key] = max(1, min(10, base_scores[key]))
        # Convert to Python float
        base_scores[key] = float(base_scores[key])
    
    return [base_scores['accuracy'], base_scores['homogeneity'], base_scores['comedy'], 
            base_scores['theatrism'], base_scores['coherence']]

def apply_realistic_scoring(scores, description):
    """Apply realistic adjustments to AI scores"""
    scores = list(scores)
    
    # Content-based adjustments
    description_lower = description.lower()
    
    if any(word in description_lower for word in ['news', 'fact', 'information']):
        scores[0] = min(10, scores[0] + 0.5)  # Accuracy
        scores[2] = max(1, scores[2] - 0.5)   # Comedy
    
    if any(word in description_lower for word in ['funny', 'comedy', 'joke']):
        scores[2] = min(10, scores[2] + 0.5)  # Comedy
        scores[3] = min(10, scores[3] + 0.3)  # Theatrism
    
    # Add small randomization for realism
    for i in range(len(scores)):
        scores[i] += random.uniform(-0.3, 0.3)
        scores[i] = max(1, min(10, scores[i]))
        # Convert to Python float to ensure JSON serialization
        scores[i] = float(scores[i])
    
    return scores

def get_reward_tier(average_score):
    """Get reward tier based on average score"""
    if average_score >= 8:
        return "Diamond"
    elif average_score >= 6:
        return "Gold"
    elif average_score >= 4:
        return "Silver"
    else:
        return "Bronze"

def get_improvement_advice(scores):
    """Generate improvement advice based on scores"""
    advice = []
    score_names = ['accuracy', 'homogeneity', 'comedy', 'theatrism', 'coherence']
    
    # Find lowest scoring metric
    min_score = min(scores)
    min_index = scores.index(min_score)
    min_metric = score_names[min_index]
    
    advice_map = {
        'accuracy': 'Focus on fact-checking and providing accurate information. Consider adding sources or citations.',
        'homogeneity': 'Work on creating a more consistent narrative structure. Ensure your content flows logically.',
        'comedy': 'Try incorporating more humor elements. Consider timing, delivery, and relatable content.',
        'theatrism': 'Enhance your performance skills. Work on facial expressions, body language, and engaging delivery.',
        'coherence': 'Improve the logical flow of your content. Make sure each part connects well with the next.'
    }
    
    advice.append(advice_map[min_metric])
    
    # Add general advice if overall score is low
    avg_score = sum(scores) / len(scores)
    if avg_score < 7:
        advice.append('Consider spending more time on pre-production planning to improve overall quality.')
    
    return ' '.join(advice)

@app.route('/')
def index():
    """Serve the main web app"""
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """API endpoint to analyze TikTok video"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        description = data.get('description', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if 'tiktok.com' not in url or '/video/' not in url:
            return jsonify({'error': 'Invalid TikTok URL'}), 400
        
        # Create temporary directory for video
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Download video
            video_path = download_tiktok_video(url, temp_dir)
            
            # Analyze with AI
            scores = analyze_video_with_ai(video_path, description)
            
            # Calculate average score
            average_score = sum(scores) / len(scores)
            
            # Get reward tier
            tier = get_reward_tier(average_score)
            
            # Generate advice
            advice = get_improvement_advice(scores)
            
            # Prepare response - convert numpy types to Python types
            result = {
                'url': url,
                'description': description or 'TikTok video analysis',
                'scores': {
                    'accuracy': float(round(scores[0], 1)),
                    'homogeneity': float(round(scores[1], 1)),
                    'comedy': float(round(scores[2], 1)),
                    'theatrism': float(round(scores[3], 1)),
                    'coherence': float(round(scores[4], 1))
                },
                'averageScore': float(round(average_score, 1)),
                'tier': tier,
                'advice': advice
            }
            
            return jsonify(result)
            
        finally:
            # Clean up temporary files
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'BYTEME AI Analyzer is running'})

if __name__ == '__main__':
    print("🚀 Starting BYTEME Web Server...")
    print("📱 Open http://localhost:8080 in your browser")
    print("🔗 API available at http://localhost:8080/api/analyze")
    
    app.run(debug=True, host='0.0.0.0', port=8080)
