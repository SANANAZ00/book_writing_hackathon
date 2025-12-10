import React from 'react';
import MDXComponents from '@theme-original/MDXComponents';
import CalloutBox from '@site/src/components/CalloutBox';
import ConceptCard from '@site/src/components/ConceptCard';
import StepFlow from '@site/src/components/StepFlow';

const ExtendedMDXComponents = {
  ...MDXComponents,
  // Custom components
  CalloutBox,
  ConceptCard,
  StepFlow,
  // HTML elements overrides if needed
  h1: (props) => <h1 {...props} />,
  h2: (props) => <h2 {...props} />,
  h3: (props) => <h3 {...props} />,
  p: (props) => <p {...props} />,
  ul: (props) => <ul {...props} />,
  ol: (props) => <ol {...props} />,
  li: (props) => <li {...props} />,
  pre: (props) => <pre {...props} />,
  code: (props) => <code {...props} />,
};

export default ExtendedMDXComponents;