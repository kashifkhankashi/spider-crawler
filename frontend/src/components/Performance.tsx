'use client';

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts';

interface PerformanceProps {
  data: any;
}

export default function Performance({ data }: PerformanceProps) {
  if (!data || !data.results || data.results.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Performance Analysis</h2>
        {data?.error ? (
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 p-4 rounded-lg">
            <p>{data.error}</p>
            {data.note && <p className="text-sm mt-2">{data.note}</p>}
          </div>
        ) : (
          <p className="text-gray-500">No performance data available</p>
        )}
      </div>
    );
  }

  const results = data.results || [];
  const aggregated = data.aggregated || {};

  // Prepare radar chart data
  const radarData = results.map((result: any) => ({
    page: new URL(result.url).pathname.slice(0, 20) || 'Home',
    score: result.score || 0,
    LCP: parseFloat(result.LCP?.replace('s', '') || '0') * 100,
    CLS: (result.CLS || 0) * 100,
  }));

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">Performance Analysis</h2>

      {aggregated.avg_score && (
        <div className="mb-6">
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-blue-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Average Score</p>
              <p className="text-3xl font-bold text-blue-600">
                {aggregated.avg_score}
              </p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Avg LCP</p>
              <p className="text-2xl font-bold text-green-600">
                {aggregated.avg_LCP || 'N/A'}
              </p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600">Avg CLS</p>
              <p className="text-2xl font-bold text-purple-600">
                {aggregated.avg_CLS || 'N/A'}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-4">Page Performance</h3>
        <div className="space-y-4">
          {results.map((result: any, idx: number) => (
            <div
              key={idx}
              className="border border-gray-200 rounded-lg p-4"
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold">
                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {new URL(result.url).pathname || result.url}
                  </a>
                </h4>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    (result.score || 0) >= 90
                      ? 'bg-green-100 text-green-800'
                      : (result.score || 0) >= 50
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  Score: {result.score || 'N/A'}
                </span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 text-sm">
                <div>
                  <p className="text-gray-500">LCP</p>
                  <p className="font-semibold">{result.LCP || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-gray-500">CLS</p>
                  <p className="font-semibold">{result.CLS || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-gray-500">FID</p>
                  <p className="font-semibold">{result.FID || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-gray-500">FCP</p>
                  <p className="font-semibold">{result.FCP || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-gray-500">TTI</p>
                  <p className="font-semibold">{result.TTI || 'N/A'}</p>
                </div>
              </div>

              {result.recommendations &&
                result.recommendations.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-sm font-semibold text-gray-700 mb-2">
                      Recommendations:
                    </p>
                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                      {result.recommendations.slice(0, 3).map(
                        (rec: any, recIdx: number) => (
                          <li key={recIdx}>{rec.title}</li>
                        )
                      )}
                    </ul>
                  </div>
                )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

