import { useCallback } from '@lynx-js/react';

export function useLynxEvents() {
  const createTapHandler = useCallback((handler: () => void) => {
    return () => {
      try {
        handler();
      } catch (error) {
        console.error('Tap handler error:', error);
      }
    };
  }, []);

  const createInputHandler = useCallback((handler: (value: string) => void) => {
    return (e: any) => {
      try {
        const value = e?.detail?.value || e?.target?.value || '';
        handler(value);
      } catch (error) {
        console.error('Input handler error:', error);
      }
    };
  }, []);

  return {
    createTapHandler,
    createInputHandler,
  };
}