import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './ChatbotWidget.module.css';

function ChatbotWidget({ selectedText }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('checking'); // 'connected', 'disconnected', 'checking'
  const messagesEndRef = useRef(null);
  const [conversationId, setConversationId] = useState(null);
  const [currentModule, setCurrentModule] = useState(null);
  const [isBookMode, setIsBookMode] = useState(false);
  const [showModuleButtons, setShowModuleButtons] = useState(false);

  const { siteConfig } = useDocusaurusContext();

  const BACKEND_URL =
    siteConfig.customFields?.BACKEND_URL ||
    'https://snazyaseen-book-publish.hf.space';


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check backend connection when chat opens
  useEffect(() => {
    if (isOpen) {
      checkBackendConnection();
    }
  }, [isOpen]);

  // Initialize with Lucy's welcome message
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setTimeout(() => {
        setMessages([
          {
            role: 'assistant',
            content: "Hello! I'm Lucy, your AI learning companion. I'm here to help you explore the fascinating world of Physical AI & Humanoid Robotics. Would you like to start with the book modules or ask me anything about the content?",
            timestamp: new Date().toISOString(),
            sources: [],
            id: 'welcome-message'
          }
        ]);
      }, 500);
    }
  }, [isOpen]);

  // Function to check backend connection
  const checkBackendConnection = async () => {
    setConnectionStatus('checking');

    try {
      // Check the main backend health endpoint first
      const response = await fetch(`${BACKEND_URL}/health`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        }
      });

      if (response.ok) {
        setConnectionStatus('connected');
      } else {
        setConnectionStatus('disconnected');
      }
    } catch (error) {
      console.error('Backend connection check failed:', error);
      setConnectionStatus('disconnected');
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
      sources: [],
      id: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use the main backend URL variable that was already configured
      const backendUrl = BACKEND_URL;

      // Log the backend URL for debugging (only in development)
      const DEBUG = window.DEBUG_CHATBOT || false;
      if (DEBUG) {
        console.log('Attempting to connect to backend:', backendUrl);
        console.log('Sending request to:', `${backendUrl}/api/book-chat/`);
      }

      // Use the book chat endpoint which supports history and book-specific features
      const response = await fetch(`${backendUrl}/api/book-chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          selected_text: selectedText || null,
          mode: selectedText ? 'selected_text' : 'full_book', // Use appropriate mode based on selected text
          history: messages.filter(msg => msg.role !== 'assistant' || msg.id !== 'welcome-message').map(msg => ({
            role: msg.role,
            content: msg.content
          })),
          provider: 'cohere', // Use Cohere as default provider
          model: 'command-r-plus-08-2024', // Use the available model
          temperature: 0.7,
          max_tokens: 500,
          search_limit: 5,
          score_threshold: 0.3
        })
      });


     if (DEBUG) {
       console.log('Response status:', response.status);
       console.log('Response ok:', response.ok);
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Backend error response:', errorData);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail || errorData.message || 'Unknown error'}`);
      }

      const data = await response.json();

      if (DEBUG) {
        console.log('Backend response data:', data);
      }


      // Create the AI message with proper response structure
      const aiMessage = {
        role: 'assistant',
        content: data.response || data.answer || 'No response received',
        sources: data.sources || data.references || [],
        timestamp: new Date().toISOString(),
        id: Date.now() + 1
      };

      setMessages(prev => [...prev, aiMessage]);
      setConversationId(data.session_id || data.conversation_id || conversationId);
    } catch (error) {
      console.error('Error sending message:', error);

      // Check if it's a network error vs API error
      let errorMessageContent = "I'm having trouble connecting to my brain right now. Please try again in a moment! The backend might be temporarily unavailable or still starting up.";

      if (error.message.includes('fetch')) {
        errorMessageContent = "Network error: Unable to connect to the backend. Please check your internet connection and make sure the backend URL is correct.";
      } else if (error.message.includes('HTTP error')) {
        errorMessageContent = `API error: ${error.message}. Please check if your backend is running and accessible.`;
      }

      // Add error message to chat
      const errorMessage = {
        role: 'assistant',
        content: errorMessageContent,
        sources: [],
        timestamp: new Date().toISOString(),
        id: Date.now() + 1
      };
      setMessages(prev => [...prev, errorMessage]);
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

  const handleBookClick = () => {
    setIsBookMode(true);
    setShowModuleButtons(true);
    const bookMessage = {
      role: 'assistant',
      content: "Great! Let's start your journey through the Physical AI & Humanoid Robotics course. I'll guide you through each module in sequence. Which module would you like to start with?",
      timestamp: new Date().toISOString(),
      sources: [],
      id: Date.now()
    };
    setMessages(prev => [...prev, bookMessage]);
  };

  const handleModuleSelect = (moduleNumber) => {
    const moduleTitles = {
      1: 'The Robotic Nervous System (ROS 2)',
      2: 'The Digital Twin (Gazebo & Unity)',
      3: 'The AI-Robot Brain (NVIDIA Isaac™)',
      4: 'Vision-Language-Action (VLA)',
      5: 'Capstone Project',
      6: 'Weekly Breakdown'
    };

    const moduleMessage = {
      role: 'assistant',
      content: `Excellent! Let's dive into Module ${moduleNumber}: ${moduleTitles[moduleNumber]}. This module covers the fundamentals and key concepts. What would you like to know about this module?`,
      timestamp: new Date().toISOString(),
      sources: [],
      id: Date.now()
    };
    setMessages(prev => [...prev, moduleMessage]);
    setCurrentModule(moduleNumber);
    setShowModuleButtons(false);
  };

  const handleTextSelection = () => {
    const selection = window.getSelection();
    if (selection.toString().trim()) {
      // This would be handled by the parent component
      // For now, we'll just show a message
      alert('Text selection detected. This would trigger the "answer from selection" mode.');
    }
  };

  const handleRestartBook = () => {
    setIsBookMode(false);
    setCurrentModule(null);
    setShowModuleButtons(false);
    const restartMessage = {
      role: 'assistant',
      content: "I've reset the book mode. Would you like to start over or ask me something else?",
      timestamp: new Date().toISOString(),
      sources: [],
      id: Date.now()
    };
    setMessages(prev => [...prev, restartMessage]);
  };

  return (
    <div className={clsx(styles.chatbotWidget, isOpen && styles.chatbotWidgetOpen)}>
      <button
        className={clsx(styles.chatToggle, isOpen && styles.chatToggleOpen)}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? (
          <div className={styles.lucyHeader}>
            <div className={styles.lucyAvatar}>
              <span className={styles.lucyIcon}>👩‍🏫</span>
            </div>
            <span className={styles.lucyName}>Lucy</span>
          </div>
        ) : (
          <div className={styles.lucyClosed}>
            <span className={styles.lucyIcon}>👩‍🏫</span>
          </div>
        )}
      </button>

      {isOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.chatHeader}>
            <div className={styles.lucyHeaderFull}>
              <div className={styles.lucyAvatarLarge}>
                <span className={styles.lucyIcon}>👩‍🏫</span>
              </div>
              <div className={styles.lucyInfo}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <h3 className={styles.lucyTitle}>Lucy - AI Learning Companion</h3>
                  <div className={styles.connectionStatus}>
                    <div className={clsx(
                      styles.connectionIndicator,
                      styles[connectionStatus],
                      connectionStatus === 'checking' && styles.connecting
                    )}></div>
                    <span className={styles.connectionText}>
                      {connectionStatus === 'connected' ? 'Online' :
                       connectionStatus === 'checking' ? 'Connecting...' : 'Offline'}
                    </span>
                    <button
                      className={styles.refreshButton}
                      onClick={checkBackendConnection}
                      title="Refresh connection"
                      aria-label="Refresh connection"
                    >
                      🔄
                    </button>
                  </div>
                </div>
                <p className={styles.lucySubtitle}>Always here to help you learn</p>
              </div>
            </div>
            <div className={styles.chatControls}>
              {isBookMode && (
                <button
                  className={clsx(styles.chatControlButton, styles.restartButton)}
                  onClick={handleRestartBook}
                  aria-label="Restart book mode"
                  title="Restart Book Mode"
                >
                  🔄
                </button>
              )}
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
                <div className={styles.lucyWelcome}>
                  <div className={styles.lucyWelcomeAvatar}>
                    <span className={styles.lucyIcon}>👩‍🏫</span>
                  </div>
                  <div className={styles.lucyWelcomeText}>
                    <h4>Hello! I'm Lucy 🌟</h4>
                    <p>Your AI learning companion for Physical AI & Humanoid Robotics</p>
                  </div>
                </div>
                <div className={styles.welcomeActions}>
                  <button
                    className={clsx(styles.welcomeButton, styles.bookButton)}
                    onClick={handleBookClick}
                  >
                    📚 Start Learning Modules
                  </button>
                  <p className={styles.welcomePrompt}>or ask me anything about the content!</p>
                </div>
              </div>
            )}

            {showModuleButtons && (
              <div className={styles.moduleSelector}>
                <h4 className={styles.moduleSelectorTitle}>Choose Your Module Journey</h4>
                <div className={styles.moduleGrid}>
                  {[1, 2, 3, 4, 5, 6].map(moduleNumber => (
                    <button
                      key={moduleNumber}
                      className={clsx(styles.moduleButton, styles[`module${moduleNumber}`])}
                      onClick={() => handleModuleSelect(moduleNumber)}
                    >
                      <span className={styles.moduleNumber}>Module {moduleNumber}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {messages.filter(msg => msg.id !== 'welcome-message' || messages.length > 1).map((msg, index) => (
              <div
                key={msg.id || index}
                className={clsx(
                  styles.message,
                  styles[`message--${msg.role}`],
                  msg.role === 'assistant' && styles.messageAssistant
                )}
              >
                <div className={styles.messageHeader}>
                  {msg.role === 'assistant' && (
                    <span className={styles.assistantAvatar}>👩‍🏫</span>
                  )}
                  <span className={styles.messageRole}>
                    {msg.role === 'assistant' ? 'Lucy' : 'You'}
                  </span>
                </div>
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
                <div className={styles.messageHeader}>
                  <span className={styles.assistantAvatar}>👩‍🏫</span>
                  <span className={styles.messageRole}>Lucy</span>
                </div>
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
                placeholder={selectedText ? "Ask Lucy about the selected text..." : "Ask Lucy anything..."}
                rows="2"
                className={styles.chatTextarea}
                aria-label="Type your message to Lucy"
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputValue.trim()}
                className={clsx(
                  styles.sendButton,
                  (isLoading || !inputValue.trim()) && styles.sendButtonDisabled
                )}
                aria-label="Send message to Lucy"
              >
                {isLoading ? '...' : '➤'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatbotWidget;