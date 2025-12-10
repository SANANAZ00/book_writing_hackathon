import React, { useEffect } from 'react';

const SmoothScroll = ({ children }) => {
  useEffect(() => {
    // Set smooth scrolling for the entire document
    document.documentElement.style.scrollBehavior = 'smooth';

    // Clean up on unmount
    return () => {
      document.documentElement.style.scrollBehavior = 'auto';
    };
  }, []);

  return <>{children}</>;
};

export default SmoothScroll;