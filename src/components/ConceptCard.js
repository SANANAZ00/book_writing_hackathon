import React from 'react';
import clsx from 'clsx';

import styles from './ConceptCard.module.css';

function ConceptCard({ title, description, icon, children, level, tags }) {
  return (
    <div className={clsx(styles.conceptCard, 'margin-vert--md')}>
      <div className={styles.conceptCardHeader}>
        {icon && <span className={styles.conceptCardIcon}>{icon}</span>}
        <h3 className={styles.conceptCardTitle}>{title}</h3>
        {level && (
          <span className={clsx(styles.conceptCardLevel, styles[`level--${level}`])}>
            {level}
          </span>
        )}
      </div>

      <div className={styles.conceptCardBody}>
        {description && <p className={styles.conceptCardDescription}>{description}</p>}
        {children && <div className={styles.conceptCardContent}>{children}</div>}
      </div>

      {tags && tags.length > 0 && (
        <div className={styles.conceptCardFooter}>
          <div className={styles.conceptCardTags}>
            {tags.map((tag, index) => (
              <span key={index} className={styles.conceptCardTag}>
                {tag}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ConceptCard;