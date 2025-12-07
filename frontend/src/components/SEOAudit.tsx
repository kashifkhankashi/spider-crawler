'use client';

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';

interface SEOAuditProps {
  data: any;
}

const COLORS = ['#10b981', '#f59e0b', '#ef4444'];

export default function SEOAudit({ data }: SEOAuditProps) {
  if (!data) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">SEO Audit</h2>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const score = data.score || 0;
  const issuesCount = data.summary?.total_issues || 0;
  const warningsCount = data.summary?.total_warnings || 0;

  const scoreColor =
    score >= 80 ? 'text-green-600' : score >= 60 ? 'text-yellow-600' : 'text-red-600';

  const chartData = [
    { name: 'Issues', value: issuesCount },
    { name: 'Warnings', value: warningsCount },
    {
      name: 'OK',
      value: Math.max(0, (data.summary?.total_pages || 0) - issuesCount - warningsCount),
    },
  ];

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">SEO Audit</h2>

      <div className="mb-6">
        <div className="flex items-center justify-center mb-4">
          <div className="relative w-32 h-32">
            <svg className="transform -rotate-90 w-32 h-32">
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                className="text-gray-200"
              />
              <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                strokeDasharray={`${(score / 100) * 351.86} 351.86`}
                className={scoreColor.replace('text-', 'stroke-')}
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={`text-3xl font-bold ${scoreColor}`}>
                {score.toFixed(0)}
              </span>
            </div>
          </div>
        </div>
        <p className="text-center text-gray-600 font-medium">SEO Score</p>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">Issues Overview</h3>
        {chartData.some((d) => d.value > 0) ? (
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-500 text-center">No issues found</p>
        )}
      </div>

      <div className="space-y-2">
        <div className="flex justify-between">
          <span className="text-gray-600">Total Issues:</span>
          <span className="font-semibold text-red-600">{issuesCount}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Total Warnings:</span>
          <span className="font-semibold text-yellow-600">{warningsCount}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Pages Analyzed:</span>
          <span className="font-semibold">{data.summary?.total_pages || 0}</span>
        </div>
      </div>

      {data.issues && data.issues.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-3">Top Issues</h3>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {data.issues.slice(0, 5).map((issue: any, idx: number) => (
              <div
                key={idx}
                className="bg-red-50 border-l-4 border-red-500 p-3 rounded"
              >
                <p className="text-sm font-medium text-red-800">
                  {issue.type?.replace(/_/g, ' ').toUpperCase()}
                </p>
                <p className="text-xs text-red-600 mt-1">{issue.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

