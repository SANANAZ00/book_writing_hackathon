import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';

import styles from './ChatbotWidget.module.css';

function ChatbotWidget({ selectedText }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const messagesEndRef = useRef(null);
  const [conversationId, setConversationId] = useState(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
      sources: []
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          selected_text: selectedText || null,
          conversation_history: messages.map(msg => ({
            role: msg.role,
            content: msg.content
          })),
          context_only: !!selectedText
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const aiMessage = {
        role: 'assistant',
        content: data.response,
        sources: data.sources || [],
        timestamp: new Date().toISOString(),
        query: data.query
      };

      setMessages(prev => [...prev, aiMessage]);
      setConversationId(data.conversation_id || conversationId);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        sources: [],
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection.toString().trim()) {
      // This would be handled by the parent component
      // For now, we'll just show a message
      alert('Text selection detected. This would trigger the "answer from selection" mode.');
    }
  };

  return (
    <div className={clsx(styles.chatbotWidget, isOpen && styles.chatbotWidgetOpen)}>
      <button
        className={clsx(styles.chatToggle, isOpen && styles.chatToggleOpen)}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        💬 AI Assistant
      </button>

      {isOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.chatHeader}>
            <h3>Documentation Assistant</h3>
            <div className={styles.chatControls}>
              <button
                className={clsx(styles.chatControlButton, styles.minimizeButton)}
                onClick={() => setIsOpen(false)}
                aria-label="Minimize chat"
              >
                −
              </button>
            </div>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 && (
              <div className={styles.welcomeMessage}>
                <p>Hello! I'm your AI documentation assistant.</p>
                <p>Ask me anything about the content on this page.</p>
                {selectedText && (
                  <p className={styles.selectionMode}>
                    <strong>Selection Mode Active:</strong> I'll answer only from the selected text.
                  </p>
                )}
              </div>
            )}

            {messages.map((msg, index) => (
              <div
                key={index}
                className={clsx(
                  styles.message,
                  styles[`message--${msg.role}`],
                  msg.role === 'assistant' && styles.messageAssistant
                )}
              >
                <div className={styles.messageContent}>
                  {msg.content}
                  {msg.sources && msg.sources.length > 0 && (
                    <div className={styles.sources}>
                      <details className={styles.sourcesDetails}>
                        <summary className={styles.sourcesSummary}>
                          Sources ({msg.sources.length})
                        </summary>
                        <ul className={styles.sourcesList}>
                          {msg.sources.map((source, srcIndex) => (
                            <li key={srcIndex} className={styles.sourceItem}>
                              {source.title || source.source || `Source ${srcIndex + 1}`}
                            </li>
                          ))}
                        </ul>
                      </details>
                    </div>
                  )}
                </div>
                <div className={styles.messageTimestamp}>
                  {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={clsx(styles.message, styles.messageAssistant)}>
                <div className={styles.messageContent}>
                  <div className={styles.typingIndicator}>
                    <span className={styles.typingDot}></span>
                    <span className={styles.typingDot}></span>
                    <span className={styles.typingDot}></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInput}>
            {selectedText && (
              <div className={styles.selectionIndicator}>
                <span className={styles.selectionIcon}>📋</span>
                <span>Answering from selected text only</span>
                <button
                  className={styles.clearSelection}
                  onClick={() => {/* Clear selection functionality */}}
                >
                  Clear
                </button>
              </div>
            )}
            <div className={styles.inputContainer}>
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={selectedText ? "Ask about the selected text..." : "Ask about this documentation..."}
                rows="2"
                className={styles.chatTextarea}
                aria-label="Type your message"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className={clsx(
                  styles.sendButton,
                  (isLoading || !inputValue.trim()) && styles.sendButtonDisabled
                )}
                aria-label="Send message"
              >
                {isLoading ? '...' : 'Send'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatbotWidget;