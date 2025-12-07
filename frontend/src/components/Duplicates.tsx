'use client';

interface DuplicatesProps {
  data: any;
}

export default function Duplicates({ data }: DuplicatesProps) {
  if (!data || !data.duplicates || data.duplicates.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-4">Duplicate Content</h2>
        <p className="text-gray-500">No duplicate content detected</p>
      </div>
    );
  }

  const duplicates = data.duplicates || [];
  const similarityColor = (similarity: number) => {
    if (similarity >= 0.9) return 'text-red-600';
    if (similarity >= 0.8) return 'text-orange-600';
    return 'text-yellow-600';
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">Duplicate Content</h2>

      <div className="mb-4">
        <p className="text-gray-600">
          Found <span className="font-semibold">{data.total_duplicates}</span>{' '}
          duplicate content pairs
        </p>
        <p className="text-sm text-gray-500 mt-1">
          Methods used: {data.methods_used?.join(', ')}
        </p>
      </div>

      <div className="space-y-4 max-h-96 overflow-y-auto">
        {duplicates.slice(0, 20).map((dup: any, idx: number) => (
          <div
            key={idx}
            className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center justify-between mb-2">
              <span
                className={`font-semibold ${similarityColor(dup.similarity)}`}
              >
                {Math.round(dup.similarity * 100)}% Similar
              </span>
              <span className="text-xs text-gray-500">
                Method: {dup.method}
              </span>
            </div>
            <div className="space-y-1 text-sm">
              <div>
                <span className="text-gray-500">Page 1:</span>{' '}
                <a
                  href={dup.page1}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline break-all"
                >
                  {dup.page1}
                </a>
              </div>
              <div>
                <span className="text-gray-500">Page 2:</span>{' '}
                <a
                  href={dup.page2}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline break-all"
                >
                  {dup.page2}
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

