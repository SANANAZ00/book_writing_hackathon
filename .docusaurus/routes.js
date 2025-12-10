import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/book_writing_hackathon/__docusaurus/debug',
    component: ComponentCreator('/book_writing_hackathon/__docusaurus/debug', 'd43'),
    exact: true
  },
  {
    path: '/book_writing_hackathon/__docusaurus/debug/config',
    component: ComponentCreator('/book_writing_hackathon/__docusaurus/debug/config', '90a'),
    exact: true
  },
  {
    path: '/book_writing_hackathon/__docusaurus/debug/content',
    component: ComponentCreator('/book_writing_hackathon/__docusaurus/debug/content', 'd87'),
    exact: true
  },
  {
    path: '/book_writing_hackathon/__docusaurus/debug/globalData',
    component: ComponentCreator('/book_writing_hackathon/__docusaurus/debug/globalData', '741'),
    exact: true
  },
  {
    path: '/book_writing_hackathon/__docusaurus/debug/metadata',
    component: ComponentCreator('/book_writing_hackathon/__docusaurus/debug/metadata', '92a'),
    exact: true
  },
  {
    path: '/book_writing_hackathon/__docusaurus/debug/registry',
    component: ComponentCreator('/book_writing_hackathon/__docusaurus/debug/registry', 'd22'),
    exact: true
  },
  {
    path: '/book_writing_hackathon/__docusaurus/debug/routes',
    component: ComponentCreator('/book_writing_hackathon/__docusaurus/debug/routes', '0a5'),
    exact: true
  },
  {
    path: '/book_writing_hackathon/docs',
    component: ComponentCreator('/book_writing_hackathon/docs', '64f'),
    routes: [
      {
        path: '/book_writing_hackathon/docs',
        component: ComponentCreator('/book_writing_hackathon/docs', '075'),
        routes: [
          {
            path: '/book_writing_hackathon/docs',
            component: ComponentCreator('/book_writing_hackathon/docs', 'af8'),
            routes: [
              {
                path: '/book_writing_hackathon/docs/foundations/ai-powered-documentation',
                component: ComponentCreator('/book_writing_hackathon/docs/foundations/ai-powered-documentation', '7f1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/foundations/claude-code',
                component: ComponentCreator('/book_writing_hackathon/docs/foundations/claude-code', '621'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/foundations/docusaurus-fundamentals',
                component: ComponentCreator('/book_writing_hackathon/docs/foundations/docusaurus-fundamentals', '103'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/foundations/openai-integration',
                component: ComponentCreator('/book_writing_hackathon/docs/foundations/openai-integration', '6b4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/foundations/qdrant-cloud',
                component: ComponentCreator('/book_writing_hackathon/docs/foundations/qdrant-cloud', 'f0e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/foundations/rag-systems',
                component: ComponentCreator('/book_writing_hackathon/docs/foundations/rag-systems', 'b50'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/foundations/spec-driven-development',
                component: ComponentCreator('/book_writing_hackathon/docs/foundations/spec-driven-development', '819'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/intro',
                component: ComponentCreator('/book_writing_hackathon/docs/intro', 'a20'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/systems/building-rag-chatbot',
                component: ComponentCreator('/book_writing_hackathon/docs/systems/building-rag-chatbot', '8d2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/systems/content-generation',
                component: ComponentCreator('/book_writing_hackathon/docs/systems/content-generation', '183'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/systems/environment-setup',
                component: ComponentCreator('/book_writing_hackathon/docs/systems/environment-setup', '368'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book_writing_hackathon/docs/systems/fastapi-backend',
                component: ComponentCreator('/book_writing_hackathon/docs/systems/fastapi-backend', '484'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
