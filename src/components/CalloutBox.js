import React from 'react';
import clsx from 'clsx';

import styles from './CalloutBox.module.css';

function CalloutBox({ type = 'info', title, children, icon }) {
  const calloutClasses = clsx(
    styles.callout,
    styles[`callout--${type}`],
    'margin-vert--md'
  );

  const iconMap = {
    tip: '💡',
    warning: '⚠️',
    info: 'ℹ️',
    example: '📘',
    exercise: '🧪',
    strategy: '🧭',
    concept: '🎯',
    note: '📝'
  };

  const defaultIcons = {
    tip: '💡',
    warning: '⚠️',
    info: 'ℹ️',
    example: '📘',
    exercise: '🧪',
    strategy: '🧭',
    concept: '🎯',
    note: '📝'
  };

  const displayIcon = icon || iconMap[type] || defaultIcons[type] || 'ℹ️';

  return (
    <div className={calloutClasses}>
      <div className={styles.calloutHeader}>
        <span className={styles.calloutIcon}>{displayIcon}</span>
        <span className={styles.calloutTitle}>
          {title || type.charAt(0).toUpperCase() + type.slice(1)}
        </span>
      </div>
      <div className={styles.calloutBody}>
        {children}
      </div>
    </div>
  );
}

export default CalloutBox;