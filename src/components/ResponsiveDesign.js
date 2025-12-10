import React, { useState, useEffect } from 'react';

const useMediaQuery = (query) => {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }
    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);
    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
};

const ResponsiveDesign = ({ children }) => {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const isTablet = useMediaQuery('(max-width: 996px)');
  const isDesktop = useMediaQuery('(min-width: 997px)');

  const [deviceType, setDeviceType] = useState('desktop');

  useEffect(() => {
    if (isMobile) {
      setDeviceType('mobile');
    } else if (isTablet) {
      setDeviceType('tablet');
    } else {
      setDeviceType('desktop');
    }
  }, [isMobile, isTablet]);

  return (
    <div className={`responsive-container responsive-${deviceType}`}>
      {children}
    </div>
  );
};

export default ResponsiveDesign;