import React, { useState, useEffect } from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatbotWidget from '@site/src/components/ChatbotWidget';
import SelectTextOverlay from '@site/src/components/SelectTextOverlay';

export default function Layout(props) {
  const [selectedText, setSelectedText] = useState('');

  // Function to handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection.toString().trim()) {
        setSelectedText(selection.toString().trim());
      } else {
        setSelectedText('');
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  return (
    <>
      <OriginalLayout {...props} />
      <ChatbotWidget selectedText={selectedText} />
      <SelectTextOverlay
        onTextSelected={setSelectedText}
        onClearSelection={() => setSelectedText('')}
      />
    </>
  );
}