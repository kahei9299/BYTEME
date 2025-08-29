import cv2
import numpy as np
import librosa
from sklearn.feature_extraction.text import TfidfVectorizer

class TikTokFeatureExtractor:
    def __init__(self):
        self.text_vectorizer = TfidfVectorizer(max_features=100)
        
    def extract_video_features(self, video_path):
        """Extract basic video features"""
        cap = cv2.VideoCapture(video_path)
        features = []
        
        # Extract frames
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Resize frame
            frame = cv2.resize(frame, (224, 224))
            
            # Convert to grayscale for simplicity
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Extract basic features
            mean_brightness = np.mean(gray)
            std_brightness = np.std(gray)
            
            features.append([mean_brightness, std_brightness])
            frame_count += 1
            
            # Limit to first 30 frames for now
            if frame_count >= 30:
                break
        
        cap.release()
        
        if features:
            # Average features across frames
            return np.mean(features, axis=0)
        return np.array([0, 0])
    
    def extract_audio_features(self, video_path):
        """Extract basic audio features"""
        try:
            # Extract audio from video
            y, sr = librosa.load(video_path)
            
            # Extract basic features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=5)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            
            # Average across time
            mfcc_mean = np.mean(mfcc, axis=1)
            spectral_centroid_mean = np.mean(spectral_centroid)
            
            return np.concatenate([mfcc_mean, [spectral_centroid_mean]])
        except:
            # Return zeros if audio extraction fails
            return np.zeros(6)
    
    def extract_text_features(self, description):
        """Extract text features from description"""
        if not description:
            return np.zeros(100)
        
        # Simple TF-IDF features
        try:
            features = self.text_vectorizer.fit_transform([description])
            feature_array = features.toarray()[0]
            
            # Ensure we have exactly 100 features
            if len(feature_array) < 100:
                # Pad with zeros if needed
                padded_features = np.zeros(100)
                padded_features[:len(feature_array)] = feature_array
                return padded_features
            elif len(feature_array) > 100:
                # Truncate if too many
                return feature_array[:100]
            else:
                return feature_array
        except:
            # Return zeros if TF-IDF fails
            return np.zeros(100)

# Example usage
if __name__ == "__main__":
    extractor = TikTokFeatureExtractor()
    
    # Test feature extraction
    video_path = "data/videos/sample.mp4"
    video_features = extractor.extract_video_features(video_path)
    audio_features = extractor.extract_audio_features(video_path)
    text_features = extractor.extract_text_features("Funny cooking tutorial")
    
    print(f"Video features: {video_features}")
    print(f"Audio features: {audio_features}")
    print(f"Text features shape: {text_features.shape}")