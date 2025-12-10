import React, { useState, useEffect } from 'react';
import clsx from 'clsx';

import styles from './SelectTextOverlay.module.css';

function SelectTextOverlay({ onTextSelected, onClearSelection }) {
  const [selectedText, setSelectedText] = useState('');
  const [showOverlay, setShowOverlay] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setSelectedText(text);
        setPosition({ x: rect.right, y: rect.top });
        setShowOverlay(true);

        // Notify parent component
        if (onTextSelected) {
          onTextSelected(text);
        }
      } else {
        setShowOverlay(false);
        setSelectedText('');
        if (onClearSelection) {
          onClearSelection();
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, [onTextSelected, onClearSelection]);

  const handleAskAI = () => {
    // This would trigger the chatbot with the selected text context
    if (window.ChatbotWidgetRef) {
      window.ChatbotWidgetRef.askWithSelection(selectedText);
    }
  };

  if (!showOverlay || !selectedText) {
    return null;
  }

  return (
    <div
      className={styles.selectTextOverlay}
      style={{
        left: `${position.x + 10}px`,
        top: `${position.y}px`,
      }}
    >
      <button
        className={styles.askButton}
        onClick={handleAskAI}
        title="Ask AI about selected text"
      >
        💬 Ask AI
      </button>
      <button
        className={styles.clearButton}
        onClick={() => {
          window.getSelection().removeAllRanges();
          setShowOverlay(false);
          setSelectedText('');
          if (onClearSelection) {
            onClearSelection();
          }
        }}
        title="Clear selection"
      >
        ✕
      </button>
    </div>
  );
}

export default SelectTextOverlay;