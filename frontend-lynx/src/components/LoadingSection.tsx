import { useState, useEffect } from '@lynx-js/react';

export function LoadingSection() {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { icon: '⬇️', text: 'Downloading video' },
    { icon: '👁️', text: 'Extracting features' },
    { icon: '🧠', text: 'AI analysis' },
    { icon: '📊', text: 'Generating results' },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % steps.length);
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  return (
    <view className="loading-section">
      <view className="loading-card">
        <view className="loading-spinner">
          <text className="spinner-icon">⚙️</text>
        </view>
        <text className="loading-title">Analyzing Video...</text>
        <text className="loading-subtitle">
          Our AI is processing your TikTok video
        </text>

        <view className="loading-steps">
          {steps.map((step, index) => (
            <view
              key={index}
              className={`step ${index <= currentStep ? 'active' : ''}`}
            >
              <text className="step-icon">{step.icon}</text>
              <text className="step-text">{step.text}</text>
            </view>
          ))}
        </view>
      </view>
    </view>
  );
}
