'use client';

import { useState } from 'react';

interface PagesViewProps {
  data: any;
  seoAudit: any;
}

export default function PagesView({ data, seoAudit }: PagesViewProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'word_count' | 'depth' | 'url'>('word_count');

  if (!data || !data.pages) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Pages</h2>
        <p className="text-gray-500">No page data available</p>
      </div>
    );
  }

  const pages = data.pages || [];
  
  // Get issues per page
  const issuesByPage: Record<string, any[]> = {};
  const warningsByPage: Record<string, any[]> = {};
  
  if (seoAudit) {
    seoAudit.issues?.forEach((issue: any) => {
      const page = issue.page;
      if (!issuesByPage[page]) issuesByPage[page] = [];
      issuesByPage[page].push(issue);
    });
    
    seoAudit.warnings?.forEach((warning: any) => {
      const page = warning.page;
      if (!warningsByPage[page]) warningsByPage[page] = [];
      warningsByPage[page].push(warning);
    });
  }

  // Filter and sort pages
  const filteredPages = pages
    .filter((page: any) =>
      page.url?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      page.title?.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a: any, b: any) => {
      if (sortBy === 'word_count') {
        return (b.word_count || 0) - (a.word_count || 0);
      } else if (sortBy === 'depth') {
        return (a.crawl_depth || 0) - (b.crawl_depth || 0);
      } else {
        return a.url.localeCompare(b.url);
      }
    });

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-4">All Pages</h2>
        
        <div className="flex gap-4 mb-4">
          <input
            type="text"
            placeholder="Search pages..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="word_count">Sort by Word Count</option>
            <option value="depth">Sort by Depth</option>
            <option value="url">Sort by URL</option>
          </select>
        </div>

        <div className="text-sm text-gray-600 mb-4">
          Showing {filteredPages.length} of {pages.length} pages
        </div>
      </div>

      <div className="space-y-4 max-h-[600px] overflow-y-auto">
        {filteredPages.map((page: any, idx: number) => {
          const issues = issuesByPage[page.url] || [];
          const warnings = warningsByPage[page.url] || [];
          
          return (
            <div
              key={idx}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg mb-1">
                    <a
                      href={page.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {page.title || page.url}
                    </a>
                  </h3>
                  <p className="text-sm text-gray-500 break-all">{page.url}</p>
                </div>
                <div className="ml-4 text-right">
                  <div className="text-sm text-gray-600">
                    Depth: <span className="font-semibold">{page.crawl_depth || 0}</span>
                  </div>
                  <div className="text-sm text-gray-600">
                    Status: <span className={`font-semibold ${
                      page.status_code === 200 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {page.status_code}
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                <div>
                  <p className="text-xs text-gray-500">Word Count</p>
                  <p className="text-lg font-semibold">{page.word_count?.toLocaleString() || 0}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Internal Links</p>
                  <p className="text-lg font-semibold">{page.internal_links?.length || 0}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">External Links</p>
                  <p className="text-lg font-semibold">{page.external_links?.length || 0}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Backlinks</p>
                  <p className="text-lg font-semibold">{page.backlinks_count || 0}</p>
                </div>
              </div>

              {(issues.length > 0 || warnings.length > 0) && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  {issues.length > 0 && (
                    <div className="mb-2">
                      <span className="text-xs font-semibold text-red-600">
                        {issues.length} Issue{issues.length > 1 ? 's' : ''}
                      </span>
                    </div>
                  )}
                  {warnings.length > 0 && (
                    <div>
                      <span className="text-xs font-semibold text-yellow-600">
                        {warnings.length} Warning{warnings.length > 1 ? 's' : ''}
                      </span>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}



