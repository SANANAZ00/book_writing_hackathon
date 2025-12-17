import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Learning - Physical AI & Humanoid Robotics
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Complete course on Physical AI & Humanoid Robotics using ROS 2, Gazebo, Unity, and NVIDIA Isaac">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h3>Embodied Intelligence</h3>
                <p>Learn how physical embodiment influences intelligent behavior in robotic systems.</p>
              </div>
              <div className="col col--4">
                <h3>Complete Toolchain</h3>
                <p>Master ROS 2, Gazebo, Unity, and NVIDIA Isaac for comprehensive robotics development.</p>
              </div>
              <div className="col col--4">
                <h3>Real-World Applications</h3>
                <p>Apply concepts through practical exercises and a comprehensive capstone project.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}