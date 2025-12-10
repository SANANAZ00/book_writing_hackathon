import React from 'react';

// Custom DocItemContent to ensure proper rendering with our components
export default function DocItemContent({ children }) {
  return <div className="container container--fluid">{children}</div>;
}