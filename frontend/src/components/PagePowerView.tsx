'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

interface PagePowerViewProps {
  data: any;
}

const COLORS = {
  'Very High': '#10b981',
  'High': '#3b82f6',
  'Medium': '#f59e0b',
  'Low': '#ef4444',
  'Very Low': '#9ca3af',
};

export default function PagePowerView({ data }: PagePowerViewProps) {
  if (!data || !data.top_pages) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Page Power</h2>
        <p className="text-gray-500">No page power data available</p>
      </div>
    );
  }

  const topPages = data.top_pages || [];
  const avgPower = data.average_power || 0;

  const chartData = topPages.slice(0, 15).map((page: any) => ({
    page: new URL(page.url).pathname.slice(0, 30) || 'Home',
    score: page.total_score,
    level: page.power_level,
  }));

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">Page Power Analysis</h2>

      <div className="mb-6">
        <div className="bg-blue-50 p-4 rounded-lg text-center">
          <p className="text-sm text-gray-600">Average Page Power</p>
          <p className="text-4xl font-bold text-blue-600">{avgPower.toFixed(1)}</p>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">Top Pages by Power Score</h3>
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="page"
                angle={-45}
                textAnchor="end"
                height={100}
                tick={{ fontSize: 12 }}
              />
              <YAxis />
              <Tooltip />
              <Bar dataKey="score">
                {chartData.map((entry: any, index: number) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[entry.level as keyof typeof COLORS] || '#9ca3af'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-500">No data available</p>
        )}
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-semibold">Page Power Details</h3>
        {topPages.slice(0, 20).map((page: any, idx: number) => (
          <div
            key={idx}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <h4 className="font-semibold mb-1">
                  <a
                    href={page.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {new URL(page.url).pathname || page.url}
                  </a>
                </h4>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold">{page.total_score}</div>
                <div
                  className="text-sm font-semibold"
                  style={{
                    color:
                      COLORS[page.power_level as keyof typeof COLORS] || '#9ca3af',
                  }}
                >
                  {page.power_level}
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-3 text-sm">
              {Object.entries(page.factors || {}).map(([key, factor]: [string, any]) => (
                <div key={key} className="bg-gray-50 p-2 rounded">
                  <p className="font-semibold text-xs text-gray-600 uppercase mb-1">
                    {key.replace(/_/g, ' ')}
                  </p>
                  <p className="text-lg font-bold">{factor.score || 0} pts</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {factor.count !== undefined && `Count: ${factor.count}`}
                    {factor.word_count !== undefined && `Words: ${factor.word_count}`}
                    {factor.depth !== undefined && `Depth: ${factor.depth}`}
                  </p>
                </div>
              ))}
            </div>

            {page.recommendations && page.recommendations.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <h5 className="font-semibold text-sm mb-2">Recommendations:</h5>
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  {page.recommendations.map((rec: string, recIdx: number) => (
                    <li key={recIdx}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}



