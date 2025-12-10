import React, { useState } from 'react';
import clsx from 'clsx';

import styles from './StepFlow.module.css';

function StepFlow({ steps, title, description }) {
  const [activeStep, setActiveStep] = useState(0);

  const handleStepClick = (index) => {
    setActiveStep(index);
  };

  return (
    <div className={clsx(styles.stepFlow, 'margin-vert--md')}>
      {title && <h3 className={styles.stepFlowTitle}>{title}</h3>}
      {description && <p className={styles.stepFlowDescription}>{description}</p>}

      <div className={styles.stepFlowContainer}>
        <div className={styles.stepFlowSteps}>
          {steps.map((step, index) => (
            <div
              key={index}
              className={clsx(
                styles.stepFlowStep,
                index === activeStep && styles.stepFlowStepActive,
                index < activeStep && styles.stepFlowStepCompleted
              )}
              onClick={() => handleStepClick(index)}
            >
              <div className={styles.stepFlowStepNumber}>
                {index < activeStep ? '✓' : index + 1}
              </div>
              <div className={styles.stepFlowStepTitle}>{step.title}</div>
            </div>
          ))}
        </div>

        <div className={styles.stepFlowContent}>
          <div className={styles.stepFlowStepHeader}>
            <h4 className={styles.stepFlowStepContentTitle}>
              Step {activeStep + 1}: {steps[activeStep]?.title}
            </h4>
            <div className={styles.stepFlowStepNavigation}>
              <button
                className={clsx(
                  styles.stepFlowNavButton,
                  activeStep === 0 && styles.stepFlowNavButtonDisabled
                )}
                onClick={() => setActiveStep(Math.max(0, activeStep - 1))}
                disabled={activeStep === 0}
                aria-label="Previous step"
              >
                ← Prev
              </button>
              <span className={styles.stepFlowProgress}>
                {activeStep + 1} of {steps.length}
              </span>
              <button
                className={clsx(
                  styles.stepFlowNavButton,
                  activeStep === steps.length - 1 && styles.stepFlowNavButtonDisabled
                )}
                onClick={() => setActiveStep(Math.min(steps.length - 1, activeStep + 1))}
                disabled={activeStep === steps.length - 1}
                aria-label="Next step"
              >
                Next →
              </button>
            </div>
          </div>

          <div className={styles.stepFlowStepContent}>
            {steps[activeStep]?.content && (
              <div dangerouslySetInnerHTML={{ __html: steps[activeStep].content }} />
            )}
            {steps[activeStep]?.description && (
              <p>{steps[activeStep].description}</p>
            )}
            {steps[activeStep]?.code && (
              <pre className={styles.stepFlowCode}>
                <code>{steps[activeStep].code}</code>
              </pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default StepFlow;