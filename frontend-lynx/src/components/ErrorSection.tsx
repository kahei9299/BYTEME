interface ErrorSectionProps {
  error: string;
  onRetry: () => void;
}

export function ErrorSection({ error, onRetry }: ErrorSectionProps) {
  return (
    <view className="error-section">
      <view className="error-card">
        <view className="error-icon">
          <text className="error-emoji">⚠️</text>
        </view>
        <text className="error-title">Analysis Failed</text>
        <text className="error-message">{error}</text>
        <view className="retry-btn" bindtap={onRetry}>
          <text className="btn-icon">🔄</text>
          <text className="btn-text">Try Again</text>
        </view>
      </view>
    </view>
  );
}
