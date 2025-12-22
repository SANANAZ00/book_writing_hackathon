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

function ModuleCard({title, description, link}) {
  return (
    <div className={clsx('col col--3')}>
      <div className={styles.moduleCard}>
        <div className={styles.cardContent}>
          <h3 className={styles.cardTitle}>{title}</h3>
          <p className={styles.cardDescription}>{description}</p>
          <div className={styles.cardButtonContainer}>
            <Link
              className={clsx('button button--secondary button--block', styles.learnMoreButton)}
              to={link}
            >
              Learn More
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  const moduleCards = [
    {
      title: 'Module 1: The Robotic Nervous System (ROS 2)',
      description: 'Learn about ROS 2, the middleware that enables communication between robotic components.',
      link: '/docs/module-2-ros2',
    },
    {
      title: 'Module 2: The Digital Twin (Gazebo & Unity)',
      description: 'Explore digital twin technologies using Gazebo and Unity for robot simulation.',
      link: '/docs/module-3-digital-twin',
    },
    {
      title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      description: 'Discover NVIDIA Isaac™ platform for developing AI-powered robotic applications.',
      link: '/docs/module-4-ai-brain',
    },
    {
      title: 'Module 4: Vision-Language-Action (VLA)',
      description: 'Understand Vision-Language-Action models that enable robots to perceive and act.',
      link: '/docs/module-5-vla',
    },
  ];

  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Complete course on Physical AI & Humanoid Robotics using ROS 2, Gazebo, Unity, and NVIDIA Isaac">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              {moduleCards.map((card, index) => (
                <ModuleCard key={index} {...card} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}