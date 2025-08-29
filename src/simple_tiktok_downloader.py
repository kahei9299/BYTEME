#!/usr/bin/env python3
"""
Simple TikTok video downloader and dataset manager
"""

import os
import subprocess
import sys
sys.path.append('src')
from data_collector import TikTokDataCollector

def download_tiktok_video(url, output_dir="data/videos"):
    """Download TikTok video using yt-dlp"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Change to output directory
    original_dir = os.getcwd()
    os.chdir(output_dir)
    
    try:
        # Use yt-dlp command line
        cmd = [
            'yt-dlp',
            '--format', 'best',
            '--output', '%(title)s.%(ext)s',
            '--no-playlist',
            url
        ]
        
        print(f"📱 Downloading TikTok video...")
        
        # Run the download command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Download successful!")
            
            # Find the downloaded file
            files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.webm', '.mkv'))]
            if files:
                # Get the most recent file
                latest_file = max(files, key=lambda x: os.path.getctime(x))
                print(f"📁 Downloaded: {latest_file}")
                return os.path.join(output_dir, latest_file), latest_file
            else:
                print("❌ No video file found")
                return None, None
        else:
            print(f"❌ Download failed: {result.stderr}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None
    finally:
        # Change back to original directory
        os.chdir(original_dir)

def add_tiktok_video_to_dataset(url, scores, description=""):
    """Complete pipeline: Download + Add to dataset"""
    
    print(f"🎬 Processing TikTok video: {url}")
    print("=" * 50)
    
    # Step 1: Download video
    video_path, filename = download_tiktok_video(url)
    
    if video_path is None:
        print("❌ Failed to download video")
        return False
    
    # Step 2: Add to dataset
    collector = TikTokDataCollector()
    
    # Create description from filename if not provided
    if not description:
        description = filename.replace('.mp4', '').replace('.webm', '').replace('.mkv', '')
        if len(description) > 50:
            description = description[:47] + "..."
    
    try:
        collector.add_video(video_path, scores, description)
        print(f"Added video: {filename}")
        print(f"✅ Added to dataset: {description}")
        return True
        
    except Exception as e:
        print(f"❌ Error adding to dataset: {e}")
        return False

if __name__ == "__main__":
    # Test the downloader
    url = input("Enter TikTok URL: ")
    if url:
        video_path, filename = download_tiktok_video(url)
        if video_path:
            print(f"✅ Successfully downloaded: {filename}")
        else:
            print("❌ Download failed")
