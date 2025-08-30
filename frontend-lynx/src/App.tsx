import { useState } from "@lynx-js/react";
import "./App.css";

interface AnalysisResults {
  scores: {
    accuracy: number;
    plot_homogeneity: number;
    comedic_value: number;
    theatrism: number;
    plot_coherence: number;
    overall: number;
  };
  tier: string;
  recommendations: string[];
  earnings: {
    amount: number;
    breakdown: string;
  };
}

// --- MOCK DATA ---
// Create a sample results object that mimics a real API response.
// You can change these values to test how the UI looks with different scores.
const mockApiResult: AnalysisResults = {
  scores: {
    accuracy: 8.7,
    plot_homogeneity: 7.5,
    comedic_value: 9.2,
    theatrism: 6.1,
    plot_coherence: 8.1,
    overall: 7.9,
  },
  tier: "silver",
  recommendations: [
    "Improve your presentation for better performance (current: 6.1/10.0)",
    "Accuracy looks good! (8.7/10.0)",
    "Entertainment looks good! (9.2/10.0)",
  ],
  earnings: {
    amount: 790,
    breakdown: "Base: 395 • Tier Bonus: +395",
  },
};

function App() {
  const [currentView, setCurrentView] = useState<
    "upload" | "loading" | "results"
  >("upload");
  const [videoSelected, setVideoSelected] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [results, setResults] = useState<AnalysisResults | null>(null);

  // --- NEW: State for animated loading text ---
  const [loadingStep, setLoadingStep] = useState(0);

  const handleSelectVideo = () => {
    setSelectedFileName("mock_video.mp4");
    setVideoSelected(true);
  };

  // --- UPDATED: Simulate a multi-step AI process ---
  const handleAnalyzeContent = async () => {
    if (!videoSelected) return;

    setCurrentView("loading");
    setLoadingStep(0); // Reset loading animation

    const steps = [
      "Contacting analysis server...",
      "Scoring metrics...",
      "Generating recommendations...",
      "Finalizing report...",
    ];

    // An interval to reveal steps one by one
    const interval = setInterval(() => {
      setLoadingStep((prevStep) => {
        if (prevStep < steps.length - 1) {
          return prevStep + 1;
        } else {
          clearInterval(interval); // Stop the animation
          // Set results and switch view after animation completes
          setResults(mockApiResult);
          setCurrentView("results");
          return prevStep;
        }
      });
    }, 800); // 800ms delay between each step
  };

  const getMetricColor = (value: number) => {
    if (value >= 8.5) return "#00f2ea";
    if (value >= 6.5) return "#f2e200";
    return "#fe2c55";
  };

  const getTierEmoji = (tier: string) => {
    switch (tier.toLowerCase()) {
      case "gold":
        return "🥇";
      case "silver":
        return "🥈";
      case "bronze":
        return "🥉";
      default:
        return "🎯";
    }
  };

  const handleReset = () => {
    setCurrentView("upload");
    setVideoSelected(false);
    setSelectedFileName("");
    setResults(null);
    setLoadingStep(0);
  };

  // --- NEW: A simple handler for the feedback icons ---
  const handleFeedbackClick = (e: any) => {
    // Prevent the event from bubbling up if needed
    e.stopPropagation();
    // In a real app, you would log this feedback event
    alert("Thanks for your feedback! The AI is always learning.");
  };

  const loadingLogs = [
    "🤖 Contacting analysis server...",
    "🎯 Scoring metrics...",
    "💡 Generating recommendations...",
    "✨ Finalizing report...",
  ];

  return (
    <view className="screen">
      <view className="phone-container">
        <view className="app-header">
          <text className="app-title">Creator Analytics AI</text>
          <text className="app-subtitle">Your personal content copilot</text>
        </view>

        <scroll-view className="content" scroll-y={true}>
          {currentView === "upload" && (
            <view className="upload-section">
              <view className="upload-btn" bindtap={handleSelectVideo}>
                <image
                  className="upload-icon"
                  src={
                    videoSelected
                      ? "https://lf3-static.bytednsdoc.com/obj/eden-cn/pipieh7nupabozups/check-circle.svg"
                      : "https://lf3-static.bytednsdoc.com/obj/eden-cn/pipieh7nupabozups/upload-cloud.svg"
                  }
                />
                <text className="upload-text-main">
                  {videoSelected ? "Video Ready!" : "Tap to Upload Video"}
                </text>
                <text className="upload-text-sub">
                  {videoSelected
                    ? selectedFileName
                    : "High-quality MP4, MOV recommended"}
                </text>
              </view>
              <view
                className={`analyze-btn ${!videoSelected ? "disabled" : ""}`}
                bindtap={handleAnalyzeContent}
              >
                <text>
                  {videoSelected ? "Analyze Content" : "Select Video First"}
                </text>
              </view>
            </view>
          )}

          {currentView === "loading" && (
            <view className="loading-section">
              <view className="spinner"></view>
              <text className="loading-title">The AI is Analyzing...</text>
              <text className="loading-subtitle">Here's my progress:</text>
              <view className="agent-log">
                {loadingLogs.map((log, index) => (
                  <text
                    key={index}
                    className={`log-item ${
                      index <= loadingStep ? "active" : ""
                    }`}
                  >
                    {log}
                  </text>
                ))}
              </view>
            </view>
          )}

          {currentView === "results" && results && (
            <view className="results-section">
              <view className="overall-score-card">
                <text className="overall-score-value">
                  {results.scores.overall.toFixed(1)}/10
                </text>
                <text className="overall-score-label">
                  Overall Content Score
                </text>
                <view className="tier-badge">
                  <text className="tier-text">
                    {getTierEmoji(results.tier)} {results.tier} Tier
                  </text>
                </view>
              </view>
              // Change the metrics-grid section to use backend metric names
              <view className="metrics-grid">
                {Object.entries(results.scores).map(
                  ([metric, value]) =>
                    metric !== "overall" && (
                      <view className="metric-card" key={metric}>
                        <text className="metric-name">
                          {metric === "plot_homogeneity"
                            ? "Consistency"
                            : metric === "comedic_value"
                            ? "Entertainment"
                            : metric === "theatrism"
                            ? "Presentation"
                            : metric === "plot_coherence"
                            ? "Coherence"
                            : metric.charAt(0).toUpperCase() + metric.slice(1)}
                        </text>
                        <text
                          className="metric-value"
                          style={{
                            color: getMetricColor(value as number), // Remove *10 scaling
                          }}
                        >
                          {(value as number).toFixed(1)}/10
                        </text>
                      </view>
                    )
                )}
              </view>
              <view className="recommendations-card">
                <view className="card-header">
                  <text className="card-title">💡 AI Copilot Suggestions</text>
                </view>
                {/* --- UPDATED: Interactive recommendation items --- */}
                {results.recommendations.map((rec, index) => (
                  <view className="rec-item" key={index}>
                    <text className="rec-text">{rec}</text>
                    <view className="rec-feedback">
                      <text className="feedback-prompt">Helpful?</text>
                      <text
                        className="feedback-icon"
                        bindtap={handleFeedbackClick}
                      >
                        👍
                      </text>
                      <text
                        className="feedback-icon"
                        bindtap={handleFeedbackClick}
                      >
                        👎
                      </text>
                    </view>
                  </view>
                ))}
              </view>
              <view className="earnings-card animate-fade-in-4">
                <view className="earnings-card">
                  <view className="card-header">
                    <text className="card-title">
                      💰 Estimated Creator Rewards
                    </text>
                  </view>
                  <text className="earnings-amount">
                    {results.earnings.amount} Diamonds
                  </text>
                  <text className="earnings-breakdown">
                    {results.earnings.breakdown}
                  </text>
                </view>
              </view>
              <view
                className="analyze-btn animate-fade-in-5"
                bindtap={handleReset}
              >
                <text>Analyze Another Video</text>
              </view>
            </view>
          )}
        </scroll-view>
      </view>
    </view>
  );
}

export default App;
