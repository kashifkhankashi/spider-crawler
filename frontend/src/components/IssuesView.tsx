'use client';

interface IssuesViewProps {
  seoAudit: any;
  crawlResults: any;
}

export default function IssuesView({ seoAudit, crawlResults }: IssuesViewProps) {
  if (!seoAudit) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Issues & Fixes</h2>
        <p className="text-gray-500">No audit data available</p>
      </div>
    );
  }

  const issues = seoAudit.issues || [];
  const warnings = seoAudit.warnings || [];

  const renderIssueCard = (item: any, isIssue: boolean) => (
    <div
      key={`${item.type}-${item.page}`}
      className={`border-l-4 p-4 rounded-lg mb-4 ${
        isIssue
          ? 'bg-red-50 border-red-500'
          : 'bg-yellow-50 border-yellow-500'
      }`}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <h3 className="font-semibold text-lg mb-1">
            {item.type?.replace(/_/g, ' ').toUpperCase()}
          </h3>
          <p className="text-sm text-gray-700 mb-2">{item.message}</p>
          <a
            href={item.page}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline text-sm break-all"
          >
            {item.page}
          </a>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold ${
            isIssue
              ? 'bg-red-100 text-red-800'
              : 'bg-yellow-100 text-yellow-800'
          }`}
        >
          {isIssue ? 'ISSUE' : 'WARNING'}
        </span>
      </div>

      {item.fix && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <h4 className="font-semibold text-sm mb-2">How to Fix:</h4>
          <p className="text-sm text-gray-700 mb-2">{item.fix}</p>
          
          {item.example && (
            <div className="bg-gray-100 p-3 rounded mt-2">
              <p className="text-xs text-gray-600 mb-1">Example:</p>
              <code className="text-xs text-gray-800">{item.example}</code>
            </div>
          )}
          
          {item.location && (
            <p className="text-xs text-gray-600 mt-2">
              <strong>Location:</strong> {item.location}
            </p>
          )}
          
          {item.impact && (
            <p className="text-xs text-gray-600 mt-1">
              <strong>Impact:</strong> {item.impact}
            </p>
          )}
        </div>
      )}
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Issues */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">
          Critical Issues ({issues.length})
        </h2>
        {issues.length > 0 ? (
          <div className="space-y-4">
            {issues.map((issue: any, idx: number) => renderIssueCard(issue, true))}
          </div>
        ) : (
          <p className="text-gray-500">No critical issues found! 🎉</p>
        )}
      </div>

      {/* Warnings */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">
          Warnings ({warnings.length})
        </h2>
        {warnings.length > 0 ? (
          <div className="space-y-4">
            {warnings.map((warning: any, idx: number) => renderIssueCard(warning, false))}
          </div>
        ) : (
          <p className="text-gray-500">No warnings found! 🎉</p>
        )}
      </div>
    </div>
  );
}



