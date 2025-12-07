'use client';

import { useState } from 'react';
import CrawlSummary from './CrawlSummary';
import SEOAudit from './SEOAudit';
import Keywords from './Keywords';
import Duplicates from './Duplicates';
import Performance from './Performance';
import PagesView from './PagesView';
import LinksView from './LinksView';
import IssuesView from './IssuesView';
import PagePowerView from './PagePowerView';
import Link from 'next/link';

interface TabbedDashboardProps {
  results: any;
}

const tabs = [
  { id: 'overview', label: 'Overview', icon: '📊' },
  { id: 'pages', label: 'Pages', icon: '📄' },
  { id: 'links', label: 'Links', icon: '🔗' },
  { id: 'issues', label: 'Issues & Fixes', icon: '⚠️' },
  { id: 'keywords', label: 'Keywords', icon: '🔍' },
  { id: 'power', label: 'Page Power', icon: '⚡' },
  { id: 'duplicates', label: 'Duplicates', icon: '📋' },
  { id: 'performance', label: 'Performance', icon: '⚡' },
];

export default function TabbedDashboard({ results }: TabbedDashboardProps) {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <Link
            href="/"
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            ← Back to Home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Analysis Results
        </h1>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex overflow-x-auto" aria-label="Tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    px-6 py-4 text-sm font-medium whitespace-nowrap border-b-2 transition-colors
                    ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }
                  `}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="mt-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <CrawlSummary data={results.crawl_results} />
              <SEOAudit data={results.seo_audit} />
            </div>
          )}

          {activeTab === 'pages' && (
            <PagesView data={results.crawl_results} seoAudit={results.seo_audit} />
          )}

          {activeTab === 'links' && (
            <LinksView data={results.crawl_results} />
          )}

          {activeTab === 'issues' && (
            <IssuesView seoAudit={results.seo_audit} crawlResults={results.crawl_results} />
          )}

          {activeTab === 'keywords' && (
            <Keywords data={results.keywords} />
          )}

          {activeTab === 'power' && (
            <PagePowerView data={results.page_power} />
          )}

          {activeTab === 'duplicates' && (
            <Duplicates data={results.duplicates} />
          )}

          {activeTab === 'performance' && (
            <Performance data={results.performance} />
          )}
        </div>
      </div>
    </div>
  );
}



