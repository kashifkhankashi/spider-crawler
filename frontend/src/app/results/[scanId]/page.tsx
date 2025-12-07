'use client';

import { useParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import ResultsDashboard from '@/components/ResultsDashboard';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function ResultsPage() {
  const params = useParams();
  const scanId = params.scanId as string;

  const { data: status, isLoading: statusLoading } = useQuery({
    queryKey: ['scan-status', scanId],
    queryFn: async () => {
      const response = await axios.get(`/api/scan/${scanId}/status`);
      return response.data;
    },
    refetchInterval: (query) => {
      const data = query.state.data;
      return data?.status === 'completed' || data?.status === 'error'
        ? false
        : 2000;
    },
  });

  const { data: results, isLoading: resultsLoading, error: fetchError } = useQuery({
    queryKey: ['scan-results', scanId],
    queryFn: async () => {
      try {
        const response = await axios.get(`/api/scan/${scanId}/results`);
        console.log('Scan results fetched:', response.data);
        return response.data;
      } catch (error: any) {
        console.error('Error fetching scan results:', error);
        // If we get a 202 (still processing), return null
        if (error.response?.status === 202) {
          return null;
        }
        // Otherwise return error info
        return {
          error: error.response?.data?.detail || error.message || 'Failed to fetch results',
          error_type: 'FetchError'
        };
      }
    },
    enabled: status?.status === 'completed' || status?.status === 'error',
    retry: false,
  });

  if (statusLoading) {
    return <LoadingSpinner />;
  }

  if (status?.status === 'error') {
    // Wait for error results to load
    if (resultsLoading) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <LoadingSpinner />
        </div>
      );
    }

    // Debug: log what we have
    console.log('Error status - results:', results);
    console.log('Error status - fetchError:', fetchError);
    console.log('Error status - status:', status);
    
    // Get error message with multiple fallbacks
    let errorMessage = 'Unknown error occurred. Check backend terminal for details.';
    if (results?.error && results.error.trim()) {
      errorMessage = results.error;
    } else if (fetchError?.message) {
      errorMessage = fetchError.message;
    } else if (results?.error_type) {
      errorMessage = `An error occurred (Type: ${results.error_type}). Check backend terminal for details.`;
    }
    
    const errorType = results?.error_type || fetchError?.name || 'UnknownError';
    const traceback = results?.traceback;

    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center mb-6">
              <h2 className="text-3xl font-bold text-red-600 mb-2">Scan Error</h2>
              <p className="text-gray-600">An error occurred during the website scan</p>
            </div>
            
            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded mb-4">
              <h3 className="font-semibold text-red-800 mb-2">Error Details:</h3>
              <p className="text-red-700 font-mono text-sm whitespace-pre-wrap break-words">
                {errorMessage}
              </p>
              {errorType && (
                <p className="text-red-600 text-xs mt-2">
                  Error Type: {errorType}
                </p>
              )}
            </div>

            {traceback && (
              <details className="mt-4">
                <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800 font-semibold">
                  Show Technical Details (Traceback)
                </summary>
                <pre className="mt-2 p-4 bg-gray-100 rounded text-xs overflow-auto max-h-96 whitespace-pre-wrap">
                  {traceback}
                </pre>
              </details>
            )}

            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="font-semibold mb-2">Troubleshooting Tips:</h3>
              <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                <li>Make sure the website URL is correct and accessible</li>
                <li>Try with a smaller number of pages (10-20)</li>
                <li>Check if the website blocks automated crawlers</li>
                <li>Try a different website to test</li>
                <li>Check the backend terminal for more detailed error logs</li>
              </ul>
            </div>

            <div className="mt-6">
              <a
                href="/"
                className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                ← Try Another Scan
              </a>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (status?.status === 'pending' || status?.status === 'processing') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner />
          <p className="mt-4 text-lg text-gray-600">
            {status?.status === 'pending'
              ? 'Starting scan...'
              : 'Scanning website...'}
          </p>
          <p className="mt-2 text-sm text-gray-500">
            This may take a few minutes depending on the website size
          </p>
        </div>
      </div>
    );
  }

  if (resultsLoading) {
    return <LoadingSpinner />;
  }

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            No Results Found
          </h2>
          <p className="text-gray-600">The scan results could not be loaded.</p>
        </div>
      </div>
    );
  }

  return <ResultsDashboard results={results} />;
}

