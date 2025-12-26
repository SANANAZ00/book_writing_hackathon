import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={clsx(styles.heroContent, isVisible ? styles.heroVisible : '')}>
          <h1 className={clsx('hero__title', styles.heroTitle)}>
            {siteConfig.title}
          </h1>
          <p className={clsx('hero__subtitle', styles.heroSubtitle)}>
            {siteConfig.tagline}
          </p>
          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro">
              Start Learning Now
            </Link>
            <Link
              className="button button--primary button--lg"
              to="/docs/module-1-ros2">
              Explore Modules
            </Link>
          </div>
        </div>
        <div className={styles.heroAnimation}>
          <div className={styles.robotIcon}>
            <svg viewBox="0 0 100 100" className={styles.robotSvg}>
              <circle cx="50" cy="30" r="15" fill="var(--ifm-color-primary)" />
              <rect x="35" y="45" width="30" height="40" rx="5" fill="var(--ifm-color-primary-light)" />
              <circle cx="42" cy="28" r="2" fill="white" />
              <circle cx="58" cy="28" r="2" fill="white" />
              <rect x="40" y="65" width="5" height="15" fill="var(--ifm-color-primary-dark)" />
              <rect x="55" y="65" width="5" height="15" fill="var(--ifm-color-primary-dark)" />
            </svg>
          </div>
        </div>
      </div>
    </header>
  );
}

function FeatureCard({ icon, title, description, delay = 0 }) {
  const [isVisible, setIsVisible] = useState(false);
  const [ref, setRef] = useState(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(() => setIsVisible(true), delay);
        }
      },
      { threshold: 0.1 }
    );

    if (ref) {
      observer.observe(ref);
    }

    return () => {
      if (ref) {
        observer.unobserve(ref);
      }
    };
  }, [ref, delay]);

  return (
    <div
      ref={setRef}
      className={clsx(
        styles.featureCard,
        isVisible ? styles.featureVisible : ''
      )}
      style={{ transitionDelay: `${delay}ms` }}
    >
      <div className={styles.featureIcon}>
        {icon}
      </div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

function ModuleCard({ title, description, link, index }) {
  const [isHovered, setIsHovered] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const [ref, setRef] = useState(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(() => setIsVisible(true), index * 100);
        }
      },
      { threshold: 0.1 }
    );

    if (ref) {
      observer.observe(ref);
    }

    return () => {
      if (ref) {
        observer.unobserve(ref);
      }
    };
  }, [ref, index]);

  return (
    <div
      ref={setRef}
      className={clsx(
        'col col--3',
        styles.moduleCardWrapper,
        isVisible ? styles.moduleCardVisible : ''
      )}
      style={{ transitionDelay: `${index * 100}ms` }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={clsx(styles.moduleCard, isHovered && styles.moduleCardHovered)}>
        <div className={styles.cardContent}>
          <h3 className={styles.cardTitle}>{title}</h3>
          <p className={styles.cardDescription}>{description}</p>
          <div className={styles.cardButtonContainer}>
            <Link
              className={clsx('button button--secondary', styles.learnMoreButton)}
              to={link}
            >
              Explore Module
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatsSection() {
  const [stats, setStats] = useState([
    { number: '5', label: 'Learning Modules', icon: '📚' },
    { number: '50+', label: 'Hands-on Projects', icon: '🔧' },
    { number: '24/7', label: 'AI Support', icon: '🤖' },
    { number: '100%', label: 'Practical Focus', icon: '🎯' }
  ]);

  return (
    <section className={styles.statsSection}>
      <div className="container">
        <div className="row">
          {stats.map((stat, index) => (
            <div key={index} className="col col--3">
              <div className={styles.statCard}>
                <div className={styles.statIcon}>{stat.icon}</div>
                <div className={styles.statNumber}>{stat.number}</div>
                <div className={styles.statLabel}>{stat.label}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  const features = [
    {
      icon: '🤖',
      title: 'AI-Powered Learning',
      description: 'Intelligent system that adapts to your learning style and provides personalized guidance throughout your journey.'
    },
    {
      icon: '🌐',
      title: 'Real-World Applications',
      description: 'Build and deploy actual humanoid robots using industry-standard tools like ROS 2, Gazebo, Unity, and NVIDIA Isaac.'
    },
    {
      icon: '⚡',
      title: 'Interactive Experience',
      description: 'Engage with our AI assistant, get instant answers to your questions, and participate in hands-on learning activities.'
    },
    {
      icon: '🎓',
      title: 'Comprehensive Curriculum',
      description: 'Complete end-to-end learning path from basic robotics concepts to advanced AI integration in physical systems.'
    }
  ];

  const moduleCards = [
    {
      title: 'Module 1: The Robotic Nervous System (ROS 2)',
      description: 'Learn about ROS 2, the middleware that enables communication between robotic components.',
      link: '/docs/module-1-ros2',
    },
    {
      title: 'Module 2: The Digital Twin (Gazebo & Unity)',
      description: 'Explore digital twin technologies using Gazebo and Unity for robot simulation.',
      link: '/docs/module-2-digital-twin',
    },
    {
      title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      description: 'Discover NVIDIA Isaac™ platform for developing AI-powered robotic applications.',
      link: '/docs/module-3-ai-brain',
    },
    {
      title: 'Module 4: Vision-Language-Action (VLA)',
      description: 'Understand Vision-Language-Action models that enable robots to perceive and act.',
      link: '/docs/module-4-vla',
    },
  ];

  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Complete course on Physical AI & Humanoid Robotics using ROS 2, Gazebo, Unity, and NVIDIA Isaac">
      <HomepageHeader />
      <main>
        <StatsSection />

        <section className={styles.featuresSection}>
          <div className="container">
            <div className="row">
              <div className="col col--12">
                <h2 className={styles.sectionTitle}>Why Choose This Course?</h2>
                <p className={styles.sectionSubtitle}>Designed for the future of robotics and AI integration</p>
              </div>
            </div>
            <div className="row">
              {features.map((feature, index) => (
                <div key={index} className="col col--3">
                  <FeatureCard
                    icon={feature.icon}
                    title={feature.title}
                    description={feature.description}
                    delay={index * 150}
                  />
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className={styles.modulesSection}>
          <div className="container">
            <div className="row">
              <div className="col col--12">
                <h2 className={styles.sectionTitle}>Learning Modules</h2>
                <p className={styles.sectionSubtitle}>Progressive learning path designed by industry experts</p>
              </div>
            </div>
            <div className="row">
              {moduleCards.map((card, index) => (
                <ModuleCard key={index} {...card} index={index} />
              ))}
            </div>
          </div>
        </section>

        <section className={styles.ctaSection}>
          <div className="container">
            <div className="row">
              <div className="col col--12">
                <div className={styles.ctaContent}>
                  <h2 className={styles.ctaTitle}>Ready to Build the Future?</h2>
                  <p className={styles.ctaSubtitle}>Join thousands of learners who are already building the next generation of intelligent robots</p>
                  <div className={styles.ctaButtons}>
                    <Link
                      className="button button--primary button--lg"
                      to="/docs/intro">
                      Start Learning Today
                    </Link>
                    <Link
                      className="button button--secondary button--lg"
                      to="/docs/module-1-ros2">
                      Explore Curriculum
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}