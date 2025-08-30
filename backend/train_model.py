#!/usr/bin/env python3
"""
TikTok AI Model Trainer - Add training data and train your model
"""

import sys
import os
sys.path.append('src')
from data_collector import TikTokDataCollector
from simple_tiktok_downloader import add_tiktok_video_to_dataset
from simple_model import TikTokModelTrainer
import numpy as np
import torch

def train_ai_model():
    """Train the AI model with current dataset"""
    
    print("🚀 Training AI model...")
    
    try:
        # Load dataset
        collector = TikTokDataCollector()
        dataset = collector.get_dataset()
        
        if len(dataset) < 2:
            print("⚠️  Need at least 2 videos to train. Add more videos first.")
            return False
        
        print(f"📊 Found {len(dataset)} videos in dataset")
        
        # Extract features and scores
        from feature_extractor import TikTokFeatureExtractor
        extractor = TikTokFeatureExtractor()
        
        features = []
        scores = []
        
        for _, row in dataset.iterrows():
            try:
                # Extract features for each video
                video_features = extractor.extract_video_features(row['video_path'])
                audio_features = extractor.extract_audio_features(row['video_path'])
                text_features = extractor.extract_text_features(row['description'])
                
                # Combine features
                combined_features = np.concatenate([video_features, audio_features, text_features])
                features.append(combined_features)
                
                # Get scores
                video_scores = [row['accuracy'], row['homogeneity'], row['comedy'], row['theatrism'], row['coherence']]
                scores.append(video_scores)
                
            except Exception as e:
                print(f"⚠️  Skipping video due to error: {e}")
                continue
        
        if len(features) < 2:
            print("⚠️  Not enough valid videos to train. Add more videos first.")
            return False
        
        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(scores)
        
        print(f"✅ Extracted features shape: {X.shape}")
        print(f"✅ Scores shape: {y.shape}")
        
        # Train model
        trainer = TikTokModelTrainer()
        X_train, X_test, y_train, y_test = trainer.prepare_data(X, y)
        
        print("🚀 Training model...")
        trainer.train(X_train, y_train, epochs=100)
        
        # Evaluate model
        print("📈 Evaluating model...")
        metrics = trainer.evaluate(X_test, y_test)
        
        # Display results
        for metric_name, metric_values in metrics.items():
            print(f"{metric_name}: MSE={metric_values['mse']:.4f}, MAE={metric_values['mae']:.4f}")
        
        print("🎉 Model training complete!")
        print("You can now use ai_analyzer.py to analyze new videos!")
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

def add_single_video():
    """Add a single video with manual rating"""
    
    print("🎬 Add Single Video with Manual Rating")
    print("=" * 50)
    
    # Get TikTok URL from user
    url = input("Enter TikTok URL: ").strip()
    if not url:
        print("❌ No URL provided")
        return False
    
    # Get description
    description = input("Enter video description: ").strip()
    if not description:
        description = "TikTok video"
    
    print("\n📺 Please watch the video and rate it on these 5 metrics (1-10 scale):")
    print("   Accuracy: How accurate is the information?")
    print("   Homogeneity: How consistent is the plot structure?") 
    print("   Comedy: How funny is it?")
    print("   Theatrism: How theatrical/performative is it?")
    print("   Coherence: How coherent is the plot?")
    print()
    
    # Get manual ratings
    scores = {}
    metrics = ['accuracy', 'homogeneity', 'comedy', 'theatrism', 'coherence']
    
    for metric in metrics:
        while True:
            try:
                score = int(input(f"{metric.capitalize()} (1-10): "))
                if 1 <= score <= 10:
                    scores[metric] = score
                    break
                else:
                    print("Please enter a score between 1 and 10")
            except ValueError:
                print("Please enter a valid number")
    
    print(f"\n📊 Your Ratings:")
    for metric, score in scores.items():
        print(f"   {metric.capitalize()}: {score}/10")
    
    # Calculate average score
    avg_score = sum(scores.values()) / len(scores)
    print(f"   Average Score: {avg_score:.1f}/10")
    
    # Determine reward tier
    if avg_score >= 8:
        tier = "Diamond"
    elif avg_score >= 6:
        tier = "Gold"
    elif avg_score >= 4:
        tier = "Silver"
    else:
        tier = "Bronze"
    print(f"   Reward Tier: {tier}")
    
    # Confirm before adding
    confirm = input(f"\n✅ Add this video to your dataset? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return False
    
    # Download and add to dataset
    print(f"\n📱 Downloading and adding video...")
    success = add_tiktok_video_to_dataset(url, scores, description)
    
    if success:
        print(f"✅ Successfully added: {description}")
        
        # Show updated dataset
        collector = TikTokDataCollector()
        dataset = collector.get_dataset()
        print(f"\n📋 Dataset now contains {len(dataset)} video(s)")
        
        return True
    else:
        print(f"❌ Failed to add video")
        return False

def add_batch_videos():
    """Add multiple videos with manual ratings"""
    
    print("🎬 Add Multiple Videos with Manual Ratings")
    print("=" * 50)
    
    # Get number of videos
    try:
        num_videos = int(input("How many videos do you want to add? "))
        if num_videos <= 0:
            print("❌ Please enter a positive number")
            return False
    except ValueError:
        print("❌ Please enter a valid number")
        return False
    
    success_count = 0
    
    for i in range(num_videos):
        print(f"\n🎬 Video {i+1}/{num_videos}")
        print("-" * 30)
        
        success = add_single_video()
        if success:
            success_count += 1
        
        if i < num_videos - 1:
            continue_choice = input(f"\nContinue with next video? (y/n): ").strip().lower()
            if continue_choice != 'y':
                break
    
    print(f"\n📊 Batch Addition Summary:")
    print(f"✅ Successfully added: {success_count}/{num_videos} videos")
    
    return success_count > 0

def view_dataset():
    """View current training dataset"""
    
    collector = TikTokDataCollector()
    dataset = collector.get_dataset()
    
    if len(dataset) > 0:
        print(f"\n📋 Current Training Dataset ({len(dataset)} videos):")
        print("=" * 60)
        
        for index, row in dataset.iterrows():
            avg_score = (row['accuracy'] + row['homogeneity'] + row['comedy'] + 
                        row['theatrism'] + row['coherence']) / 5
            
            if avg_score >= 8:
                tier = "Diamond"
            elif avg_score >= 6:
                tier = "Gold"
            elif avg_score >= 4:
                tier = "Silver"
            else:
                tier = "Bronze"
            
            print(f"Video {index + 1}: {row['description']}")
            print(f"  Scores: A={row['accuracy']}, H={row['homogeneity']}, C={row['comedy']}, T={row['theatrism']}, Co={row['coherence']}")
            print(f"  Average: {avg_score:.1f}/10 | Tier: {tier}")
            print()
    else:
        print("📋 No videos in training dataset yet")

def main():
    """Main training interface"""
    
    print("🎬 TikTok AI Model Trainer")
    print("Add training data and train your AI model!")
    print("=" * 50)
    
    while True:
        print("\nTraining Options:")
        print("1. Add single video with manual rating")
        print("2. Add multiple videos with manual ratings")
        print("3. View current dataset")
        print("4. Train AI model")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            add_single_video()
            
        elif choice == '2':
            add_batch_videos()
            
        elif choice == '3':
            view_dataset()
            
        elif choice == '4':
            train_ai_model()
                
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
