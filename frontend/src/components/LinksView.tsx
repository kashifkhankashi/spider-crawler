'use client';

import { useState } from 'react';

interface LinksViewProps {
  data: any;
}

export default function LinksView({ data }: LinksViewProps) {
  const [activeTab, setActiveTab] = useState<'internal' | 'external' | 'broken' | 'untitled' | 'backlinks'>('internal');

  if (!data) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Links Analysis</h2>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const linkAnalysis = data.link_analysis || {};
  const internalLinks = linkAnalysis.internal_links_detailed || [];
  const externalLinks = linkAnalysis.external_links_detailed || [];
  const brokenLinks = linkAnalysis.broken_links || [];
  const untitledLinks = linkAnalysis.untitled_links || [];
  const backlinksMap = data.backlinks_map || {};
  
  // Convert backlinks map to array for display
  const backlinksList = Object.entries(backlinksMap).map(([url, links]: [string, any]) => ({
    url,
    links: links || [],
    count: links?.length || 0,
  })).sort((a, b) => b.count - a.count);

  const renderLinkTable = (links: any[], type: string) => (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source Page</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Link URL</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Anchor Text</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {links.slice(0, 100).map((link: any, idx: number) => (
            <tr key={idx} className="hover:bg-gray-50">
              <td className="px-4 py-3 text-sm">
                <a
                  href={link.source_page}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline break-all"
                >
                  {new URL(link.source_page).pathname || '/'}
                </a>
              </td>
              <td className="px-4 py-3 text-sm">
                <a
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline break-all"
                >
                  {link.url}
                </a>
              </td>
              <td className="px-4 py-3 text-sm">
                <span className={link.is_untitled ? 'text-red-600 italic' : ''}>
                  {link.anchor_text || '(no text)'}
                </span>
              </td>
              <td className="px-4 py-3 text-sm">
                {link.title || <span className="text-gray-400">No title</span>}
              </td>
              <td className="px-4 py-3 text-sm text-gray-500">
                {link.location || 'Unknown'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {links.length > 100 && (
        <div className="px-4 py-3 text-sm text-gray-500 text-center">
          Showing 100 of {links.length} links
        </div>
      )}
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">Links Analysis</h2>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Internal Links</p>
          <p className="text-2xl font-bold text-blue-600">{internalLinks.length}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">External Links</p>
          <p className="text-2xl font-bold text-green-600">{externalLinks.length}</p>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Broken Links</p>
          <p className="text-2xl font-bold text-red-600">{brokenLinks.length}</p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Untitled Links</p>
          <p className="text-2xl font-bold text-yellow-600">{untitledLinks.length}</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Pages with Backlinks</p>
          <p className="text-2xl font-bold text-purple-600">{backlinksList.length}</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-4">
        <nav className="flex space-x-8">
          {[
            { id: 'internal', label: `Internal (${internalLinks.length})`, color: 'blue' },
            { id: 'external', label: `External (${externalLinks.length})`, color: 'green' },
            { id: 'broken', label: `Broken (${brokenLinks.length})`, color: 'red' },
            { id: 'untitled', label: `Untitled (${untitledLinks.length})`, color: 'yellow' },
            { id: 'backlinks', label: `Backlinks (${backlinksList.length})`, color: 'purple' },
          ].map((tab) => {
            const isActive = activeTab === tab.id;
            const colorClasses: Record<string, { active: string; inactive: string }> = {
              blue: { active: 'border-blue-500 text-blue-600', inactive: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' },
              green: { active: 'border-green-500 text-green-600', inactive: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' },
              red: { active: 'border-red-500 text-red-600', inactive: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' },
              yellow: { active: 'border-yellow-500 text-yellow-600', inactive: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' },
              purple: { active: 'border-purple-500 text-purple-600', inactive: 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300' },
            };
            const classes = isActive ? colorClasses[tab.color].active : colorClasses[tab.color].inactive;
            
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${classes}`}
              >
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-4">
        {activeTab === 'internal' && renderLinkTable(internalLinks, 'internal')}
        {activeTab === 'external' && renderLinkTable(externalLinks, 'external')}
        {activeTab === 'broken' && (
          <div>
            {brokenLinks.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Source Page</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Broken URL</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Issue</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reason</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {brokenLinks.map((link: any, idx: number) => (
                      <tr key={idx} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm">
                          <a
                            href={link.source_page}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            {new URL(link.source_page).pathname}
                          </a>
                        </td>
                        <td className="px-4 py-3 text-sm text-red-600 break-all">{link.url}</td>
                        <td className="px-4 py-3 text-sm font-medium">{link.issue}</td>
                        <td className="px-4 py-3 text-sm text-gray-600">{link.reason}</td>
                        <td className="px-4 py-3 text-sm text-gray-500">{link.location}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No broken links found! 🎉</p>
            )}
          </div>
        )}
        {activeTab === 'untitled' && renderLinkTable(untitledLinks, 'untitled')}
        {activeTab === 'backlinks' && (
          <div>
            {backlinksList.length > 0 ? (
              <div className="space-y-4">
                {backlinksList.map((item: any, idx: number) => (
                  <div
                    key={idx}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg mb-1">
                          <a
                            href={item.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline break-all"
                          >
                            {item.url}
                          </a>
                        </h3>
                        <p className="text-sm text-gray-600">
                          {item.count} page{item.count !== 1 ? 's' : ''} link{item.count !== 1 ? 's' : ''} to this page
                        </p>
                      </div>
                    </div>
                    <div className="overflow-x-auto">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                              Linking Page
                            </th>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                              Anchor Text
                            </th>
                            <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                              Title
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {item.links.map((link: any, linkIdx: number) => (
                            <tr key={linkIdx} className="hover:bg-gray-50">
                              <td className="px-4 py-2 text-sm">
                                <a
                                  href={link.from_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:underline"
                                >
                                  {new URL(link.from_url).pathname || '/'}
                                </a>
                              </td>
                              <td className="px-4 py-2 text-sm">
                                {link.anchor_text || <span className="text-gray-400 italic">(no text)</span>}
                              </td>
                              <td className="px-4 py-2 text-sm">
                                {link.title || <span className="text-gray-400">No title</span>}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">No backlinks data available</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

