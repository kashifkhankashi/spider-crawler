'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

export default function ScanForm() {
  const [url, setUrl] = useState('');
  const [maxPages, setMaxPages] = useState(50);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/api/scan', {
        url,
        max_pages: maxPages,
        include_external: false,
      });

      if (response.data.scan_id) {
        router.push(`/results/${response.data.scan_id}`);
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Failed to start scan. Please try again.'
      );
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-xl p-8">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label
            htmlFor="url"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Website URL
          </label>
          <input
            type="url"
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label
            htmlFor="maxPages"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Maximum Pages to Scan
          </label>
          <input
            type="number"
            id="maxPages"
            value={maxPages}
            onChange={(e) => setMaxPages(parseInt(e.target.value) || 50)}
            min="1"
            max="200"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="mt-1 text-sm text-gray-500">
            Recommended: 50-100 pages for faster results
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !url}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Starting Scan...' : 'Start Analysis'}
        </button>
      </form>
    </div>
  );
}

