import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';

import styles from './PageHeader.module.css';

function PageHeader({ title, subtitle, breadcrumb }) {
  const location = useLocation();
  const { siteConfig } = useDocusaurusContext();

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{title}</h1>
        {subtitle && <p className="hero__subtitle">{subtitle}</p>}

        {breadcrumb && (
          <nav aria-label="Breadcrumb" className={styles.breadcrumb}>
            <ul className={styles.breadcrumbList}>
              {breadcrumb.map((item, index) => (
                <li key={index} className={styles.breadcrumbItem}>
                  {item.url ? (
                    <Link to={item.url} className={styles.breadcrumbLink}>
                      {item.label}
                    </Link>
                  ) : (
                    <span className={styles.breadcrumbCurrent}>{item.label}</span>
                  )}
                  {index < breadcrumb.length - 1 && (
                    <span className={styles.breadcrumbSeparator}>/</span>
                  )}
                </li>
              ))}
            </ul>
          </nav>
        )}
      </div>
    </header>
  );
}

export default PageHeader;