import React from 'react';
import OriginalDocItem from '@theme-original/DocItem';

// Wrap the original DocItem to add custom styling/enhancements
// This avoids context issues by delegating to the original implementation
export default function DocItem(props) {
  return <OriginalDocItem {...props} />;
}