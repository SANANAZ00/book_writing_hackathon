import React, { useState, useEffect } from 'react';
import clsx from 'clsx';

import styles from './MiniMap.module.css';

function MiniMap({ headings, title = "Chapter Contents" }) {
  const [activeId, setActiveId] = useState('');
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY + window.innerHeight / 3;

      for (let i = headings.length - 1; i >= 0; i--) {
        const heading = headings[i];
        const element = document.getElementById(heading.id);

        if (element && element.offsetTop <= scrollPosition) {
          setActiveId(heading.id);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [headings]);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setActiveId(id);
    }
  };

  if (!headings || headings.length === 0) {
    return null;
  }

  return (
    <div className={clsx(styles.miniMap, isVisible && styles.miniMapVisible)}>
      <div className={styles.miniMapHeader}>
        <h3 className={styles.miniMapTitle}>{title}</h3>
        <button
          className={styles.miniMapToggle}
          onClick={() => setIsVisible(!isVisible)}
          aria-label={isVisible ? "Hide chapter contents" : "Show chapter contents"}
        >
          {isVisible ? '−' : '≡'}
        </button>
      </div>

      {isVisible && (
        <nav className={styles.miniMapNav} aria-label="Chapter navigation">
          <ul className={styles.miniMapList}>
            {headings.map((heading, index) => (
              <li key={heading.id} className={styles.miniMapItem}>
                <a
                  href={`#${heading.id}`}
                  className={clsx(
                    styles.miniMapLink,
                    heading.id === activeId && styles.miniMapLinkActive,
                    styles[`miniMapLinkLevel${heading.level}`]
                  )}
                  onClick={(e) => {
                    e.preventDefault();
                    scrollToSection(heading.id);
                  }}
                >
                  <span className={styles.miniMapBullet}>
                    {heading.level > 2 ? '•' : '○'}
                  </span>
                  <span className={styles.miniMapText}>{heading.text}</span>
                </a>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
}

export default MiniMap;