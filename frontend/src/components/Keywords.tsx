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

interface KeywordsProps {
  data: any;
}

export default function Keywords({ data }: KeywordsProps) {
  if (!data || !data.keywords) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Keyword Analysis</h2>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const rakeKeywords = data.keywords.rake || [];
  const topRake = rakeKeywords.slice(0, 10);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">Keyword Analysis</h2>

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">Top Keywords (RAKE)</h3>
        {topRake.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topRake} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis
                dataKey="phrase"
                type="category"
                width={200}
                tick={{ fontSize: 12 }}
              />
              <Tooltip />
              <Bar dataKey="score" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-500">No keyword data available</p>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h4 className="font-semibold mb-3">Top RAKE Keywords</h4>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {rakeKeywords.slice(0, 15).map((kw: any, idx: number) => (
              <div
                key={idx}
                className="flex justify-between items-center p-2 bg-gray-50 rounded"
              >
                <span className="text-sm">{kw.phrase}</span>
                <span className="text-xs text-gray-500">{kw.score}</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h4 className="font-semibold mb-3">Top Bigrams</h4>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {(data.keywords.ngrams?.bigrams || []).slice(0, 15).map(
              (ngram: any, idx: number) => (
                <div
                  key={idx}
                  className="flex justify-between items-center p-2 bg-gray-50 rounded"
                >
                  <span className="text-sm">{ngram.term}</span>
                  <span className="text-xs text-gray-500">
                    {ngram.frequency}
                  </span>
                </div>
              )
            )}
          </div>
        </div>

        <div>
          <h4 className="font-semibold mb-3">Top TF-IDF</h4>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {(data.keywords.tfidf || []).slice(0, 15).map(
              (kw: any, idx: number) => (
                <div
                  key={idx}
                  className="flex justify-between items-center p-2 bg-gray-50 rounded"
                >
                  <span className="text-sm">{kw.term}</span>
                  <span className="text-xs text-gray-500">
                    {kw.tfidf_score}
                  </span>
                </div>
              )
            )}
          </div>
        </div>
      </div>

      {data.keyword_clusters && data.keyword_clusters.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-4">Keyword Clusters</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.keyword_clusters.slice(0, 6).map((cluster: any, idx: number) => (
              <div key={idx} className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">
                  {cluster.theme}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {cluster.keywords.slice(0, 5).map((kw: string, kIdx: number) => (
                    <span
                      key={kIdx}
                      className="text-xs bg-blue-200 text-blue-800 px-2 py-1 rounded"
                    >
                      {kw}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

