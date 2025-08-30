import { useState, useCallback } from '@lynx-js/react';
import type { AnalysisRequest } from '../services/api.js';

interface InputSectionProps {
  onAnalyze: (data: AnalysisRequest) => void;
}

// Fixed values for demonstration/testing consistency
const FIXED_URL = 'https://vt.tiktok.com/ZSAXQoBdB/';
const FIXED_DESCRIPTION = 'A TikTok video with a cat.';

export function InputSection({ onAnalyze }: InputSectionProps) {
  // Use fixed values directly, state management is simplified
  const url = FIXED_URL;
  const description = FIXED_DESCRIPTION;
  const [isLoading, setIsLoading] = useState(false);

  // The handleSubmit function remains the core logic
  const handleSubmit = useCallback(() => {
    // The URL check is now guaranteed to pass if FIXED_URL is valid,
    // but we keep the trim check just in case.
    if (!url.trim() || isLoading) return;

    // We can rely on the backend validation since the frontend URL is fixed,

    setIsLoading(true);
    // Call the parent handler with the fixed data
    onAnalyze({
      url: url.trim(),
      description: description.trim(),
    });

    // Note: setIsLoading(false) should happen in App.tsx when analysis completes (success/error)
    // but since this component unmounts on state change, it's safer to let the parent control loading.
    // However, if the user navigates back to 'input', the state resets.
  }, [url, description, onAnalyze, isLoading]);

  // Placeholder tap handlers are simplified or removed,
  // as the fields are read-only now (pre-filled).
  const handleInputTap = useCallback(() => {
    console.log('Input fields are pre-filled for consistent analysis.');
  }, []);

  const isButtonDisabled = !url.trim() || isLoading;

  return (
    <view className="input-section">
      <view className="input-card">
        <text className="section-title">🔗 Analyze Pre-set Video</text>
        <text className="section-subtitle">
          The video details are pre-filled for consistent AI analysis.
        </text>

        <view className="url-input-group">
          <view className="url-input-container" bindtap={handleInputTap}>
            <text className="url-input-text">{url}</text>
          </view>

          {/* Analyze Button */}
          <view
            // The button will be enabled immediately upon loading
            className={`analyze-btn ${isButtonDisabled ? 'disabled' : ''}`}
            bindtap={handleSubmit}
          >
            <text className="btn-icon">✨</text>
            {isLoading ? (
              <text className="btn-text">Analyzing...</text>
            ) : (
              <text className="btn-text">Analyze</text>
            )}
          </view>
        </view>

        <view className="description-input">
          <text className="input-label">Video Description:</text>
          <view className="description-container" bindtap={handleInputTap}>
            <text className="description-text">{description}</text>
          </view>
        </view>
      </view>
    </view>
  );
}
