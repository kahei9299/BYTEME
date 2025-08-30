import { useState, useCallback } from '@lynx-js/react';
import type { AnalysisRequest, AnalysisResponse } from './services/api.js';
import { ApiService } from './services/api.js';
import { Header } from './components/Header.js';
import { InputSection } from './components/InputSection.js';
import { LoadingSection } from './components/LoadingSection.js';
import { ResultsSection } from './components/ResultsSection.js';
import { ErrorSection } from './components/ErrorSection.js';
import './App.css';

type AppState = 'input' | 'loading' | 'results' | 'error';

const MIN_LOADING_TIME_MS = 6000;

export function App() {
  const [state, setState] = useState<AppState>('input');
  const [results, setResults] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleAnalyze = useCallback(async (data: AnalysisRequest) => {
    setState('loading');
    setError('');

    try {
      // Create a promise that resolves after the minimum loading time
      const minLoadTimePromise = new Promise((resolve) =>
        setTimeout(resolve, MIN_LOADING_TIME_MS),
      );

      // Run the API call and the minimum load time promise concurrently
      // Wait for BOTH to complete before proceeding
      const [apiResponse] = await Promise.all([
        ApiService.analyzeVideo(data),
        minLoadTimePromise,
      ]);

      setResults(apiResponse);
      setState('results');
    } catch (err) {
      // Even if the API call fails, still wait for the minimum load time
      // This prevents a sudden flash of an error screen
      await new Promise((resolve) => setTimeout(resolve, MIN_LOADING_TIME_MS));
      setError(err instanceof Error ? err.message : 'Analysis failed');
      setState('error');
    }
  }, []);

  const handleNewAnalysis = useCallback(() => {
    setState('input');
    setResults(null);
    setError('');
  }, []);

  const handleRetry = useCallback(() => {
    setState('input');
    setError('');
  }, []);

  return (
    <view className="app-container">
      <Header />

      {state === 'input' && <InputSection onAnalyze={handleAnalyze} />}

      {state === 'loading' && <LoadingSection />}

      {state === 'results' && results && (
        <ResultsSection results={results} onNewAnalysis={handleNewAnalysis} />
      )}

      {state === 'error' && (
        <ErrorSection error={error} onRetry={handleRetry} />
      )}
    </view>
  );
}
