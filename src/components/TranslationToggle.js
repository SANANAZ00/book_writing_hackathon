import React, { useMemo } from 'react';
import clsx from 'clsx';
import styles from './TranslationToggle.module.css';
import { useTranslation } from '../contexts/TranslationContext';

const TranslationToggle = ({ children, contentId }) => {
  const {
    isUrdu,
    toggleTranslation,
    translateContent,
    getTranslation,
    getTitleTranslation,
    isTranslationActive,
    translateText,
    translateMdxContent
  } = useTranslation();

  // Process the children content to translate text elements
  const translatedContent = useMemo(() => {
    if (!isUrdu) {
      return children;
    }

    // If we have a specific translation for this contentId, use it for the main content
    const translation = translateContent(contentId);
    if (translation && translation.content) {
      // If we have a complete translation for this contentId, show it
      return (
        <div className={styles.translatedContent}>
          <div className={styles.translationPlaceholder}>
            <div className={styles.translationHeader}>
              <span className={styles.languageTag}>🇺🇸 English Original</span>
              <span className={styles.languageTag}>🇵🇰 Urdu Translation</span>
            </div>
            <div className={styles.originalContent}>
              {children}
            </div>
            <div className={styles.urduContent}>
              <h2 className={styles.urduTextDirection}>{translation.title}</h2>
              <div className={styles.urduTextDirection}>
                {translation.content}
              </div>
            </div>
          </div>
        </div>
      );
    } else {
      // When there's no specific translation available, show a message indicating
      // that translation is in progress and apply styling to all content
      return (
        <div>
          <div className={styles.translationNotice}>
            <span className={styles.noticeIcon}>⚠️</span>
            <span>Urdu translation in progress for this section...</span>
          </div>
          <div className={styles.urduTextDirection}>
            {children}
          </div>
        </div>
      );
    }
  }, [children, isUrdu, contentId, translateContent]);

  const getButtonText = () => {
    return isUrdu ? 'انگریزی' : 'اردو';
  };

  const getButtonIcon = () => {
    return isUrdu ? '🇺🇸' : '🇵🇰';
  };

  return (
    <div className={styles.translationContainer}>
      <div className={styles.translationControls}>
        <button
          className={clsx(
            styles.translationButton,
            isUrdu && styles.urduActive
          )}
          onClick={toggleTranslation}
          aria-label={`Switch to ${isUrdu ? 'English' : 'Urdu'}`}
        >
          <span className={styles.buttonIcon}>{getButtonIcon()}</span>
          <span className={styles.buttonText}>{getButtonText()}</span>
          <span className={styles.toggleSlider}></span>
        </button>

        {isUrdu && (
          <div className={styles.translationNotice}>
            <span className={styles.noticeIcon}>⚠️</span>
            <span>Urdu translation in progress...</span>
          </div>
        )}
      </div>

      <div className={styles.contentWrapper}>
        {translatedContent}
      </div>
    </div>
  );
};

export default TranslationToggle;