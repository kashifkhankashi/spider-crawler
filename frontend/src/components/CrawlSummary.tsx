'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface CrawlSummaryProps {
  data: any;
}

export default function CrawlSummary({ data }: CrawlSummaryProps) {
  if (!data || !data.stats) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Crawl Summary</h2>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const stats = data.stats;
  const statusCodeData = Object.entries(stats.status_codes || {}).map(
    ([code, count]) => ({
      code: code,
      count: count,
    })
  );

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">Crawl Summary</h2>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Pages</p>
          <p className="text-2xl font-bold text-blue-600">
            {stats.total_pages || 0}
          </p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Words</p>
          <p className="text-2xl font-bold text-green-600">
            {stats.total_words?.toLocaleString() || 0}
          </p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Links</p>
          <p className="text-2xl font-bold text-purple-600">
            {stats.total_links || 0}
          </p>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Images</p>
          <p className="text-2xl font-bold text-orange-600">
            {stats.total_images || 0}
          </p>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">Status Codes</h3>
        {statusCodeData.length > 0 ? (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={statusCodeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="code" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-500">No status code data</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-600">Avg Load Time</p>
          <p className="text-xl font-semibold">
            {stats.avg_load_time?.toFixed(2) || '0'}s
          </p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Avg Word Count</p>
          <p className="text-xl font-semibold">
            {Math.round(stats.avg_word_count || 0)}
          </p>
        </div>
      </div>
    </div>
  );
}

