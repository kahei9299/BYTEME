import { useCallback } from '@lynx-js/react';
import type { AnalysisResponse } from '../services/api.js';

interface ResultsSectionProps {
  results: AnalysisResponse;
  onNewAnalysis: () => void;
}

export function ResultsSection({
  results,
  onNewAnalysis,
}: ResultsSectionProps) {
  const getTierColor = useCallback((tier: string) => {
    switch (tier.toLowerCase()) {
      case 'diamond':
        return '#b9f2ff';
      case 'gold':
        return '#ffd700';
      case 'silver':
        return '#c0c0c0';
      case 'bronze':
        return '#cd7f32';
      default:
        return '#gray';
    }
  }, []);

  const getScoreColor = useCallback((score: number) => {
    if (score >= 8) return '#4ade80';
    if (score >= 6) return '#fbbf24';
    if (score >= 4) return '#fb923c';
    return '#ef4444';
  }, []);

  return (
    <scroll-view scroll-orientation="vertical" className="results-section">
      <view className="results-card">
        <view className="results-header">
          <view className="results-title-container">
            <text className="results-title-icon">📊</text>
            <text className="results-title">Analysis Results</text>
          </view>
          <view className="new-analysis-btn" bindtap={onNewAnalysis}>
            <text className="btn-icon">➕</text>
            <text className="btn-text">New Analysis</text>
          </view>
        </view>

        <view className="video-info">
          <view className="video-thumbnail">
            <text className="thumbnail-icon">🎥</text>
          </view>
          <view className="video-details">
            <text className="video-title">TikTok Video</text>
            <text className="video-desc">{results.description}</text>
          </view>
        </view>

        <view className="metrics-grid">
          {Object.entries(results.scores).map(([key, score]) => (
            <view key={key} className="metric-card">
              <view className="metric-icon">
                <text className="metric-emoji">
                  {key === 'accuracy'
                    ? '✅'
                    : key === 'coherence'
                      ? '🧩'
                      : key === 'comedy'
                        ? '😂'
                        : key === 'homogeneity'
                          ? '📚'
                          : '🎭'}
                </text>
              </view>
              <text className="metric-name">
                {key.charAt(0).toUpperCase() + key.slice(1)}
              </text>
              <view className="score-container">
                <text className="score" style={{ color: getScoreColor(score) }}>
                  {score.toFixed(1)}
                </text>
                <text className="score-max">/10</text>
              </view>
              <view className="progress-bar">
                <view
                  className="progress-fill"
                  style={{
                    width: `${(score / 10) * 100}%`,
                    backgroundColor: getScoreColor(score),
                  }}
                />
              </view>
            </view>
          ))}
        </view>

        <view className="overall-score-card">
          <view className="overall-score-item">
            <text className="overall-title">Overall Score</text>
            <view className="big-score">
              <text
                className="big-score-value"
                style={{ color: getScoreColor(results.averageScore) }}
              >
                {results.averageScore.toFixed(1)}
              </text>
              <text className="big-score-max">/10</text>
            </view>
          </view>
          <view className="overall-score-item">
            <text className="overall-title">Reward Tier</text>
            <view
              className="tier-badge"
              style={{ backgroundColor: getTierColor(results.tier) }}
            >
              <text className="tier-text">{results.tier}</text>
            </view>
          </view>
        </view>

        <view className="improvement-section">
          <view className="improvement-header">
            <text className="improvement-icon">💡</text>
            <text className="improvement-title">Improvement Advice</text>
          </view>
          <view className="advice-content">
            <text className="advice-text">{results.advice}</text>
          </view>
        </view>
      </view>
    </scroll-view>
  );
}
