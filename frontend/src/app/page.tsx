'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import ScanForm from '@/components/ScanForm';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Website Analysis Tool
          </h1>
          <p className="text-xl text-gray-600">
            Real-time SEO audit, keyword analysis, and performance insights
          </p>
        </div>

        <ScanForm />
      </div>
    </main>
  );
}

