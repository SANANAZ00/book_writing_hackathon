import React from 'react';
import { HtmlClassNameProvider } from '@docusaurus/theme-common';
import { DocProvider } from '@docusaurus/theme-common/internal';
import DocItem from '@theme/DocItem';
import NotFound from '@theme/NotFound';
import Layout from '@theme/Layout';
import { Redirect } from '@docusaurus/router';

function DocPageContent({ route, content: DocContent }) {
  if (route === undefined) {
    return <NotFound />;
  }
  const { content: MDXContent, metadata } = DocContent;
  const { permalink } = metadata;

  // Use DocProvider to provide document context
  return (
    <DocProvider content={DocContent}>
      <HtmlClassNameProvider className={metadata.unversionedId}>
        <Layout
          title={metadata.title}
          description={metadata.description}
          wrapperClassName="hero hero--primary"
        >
          <div className="container margin-vert--lg">
            <div className="row">
              <main className="col col--12">
                <DocItem content={DocContent} />
              </main>
            </div>
          </div>
        </Layout>
      </HtmlClassNameProvider>
    </DocProvider>
  );
}

export default function DocPage(props) {
  const {
    route,
    content: DocContent,
    versionMetadata,
  } = props;

  if (versionMetadata.routePriority === -1) {
    return <Redirect to={versionMetadata.documents[0].permalink} />;
  }
  return <DocPageContent route={route} content={DocContent} />;
}