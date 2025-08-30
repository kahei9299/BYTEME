declare module '@lynx-js/react' {
  export * from 'react';

  export interface LynxViewProps {
    className?: string;
    style?: React.CSSProperties;
    bindtap?: (e?: any) => void;
    children?: React.ReactNode;
  }
  
  export interface LynxTextProps {
    className?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
  }
  
  export interface LynxImageProps {
    className?: string;
    style?: React.CSSProperties;
    src: string;
    alt?: string;
  }
  
  export interface LynxScrollViewProps {
    className?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
  }
  
  export interface LynxListProps {
    className?: string;
    style?: React.CSSProperties;
    children?: React.ReactNode;
  }
}

declare global {
  namespace JSX {
    interface IntrinsicElements {
      // Official Lynx built-in elements
      'view': import('@lynx-js/react').LynxViewProps;
      'text': import('@lynx-js/react').LynxTextProps;
      'image': import('@lynx-js/react').LynxImageProps;
      'scroll-view': import('@lynx-js/react').LynxScrollViewProps;
      'list': import('@lynx-js/react').LynxListProps;
    }
  }
}

export {};