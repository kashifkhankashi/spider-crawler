'use client';

import TabbedDashboard from './TabbedDashboard';

interface ResultsDashboardProps {
  results: any;
}

export default function ResultsDashboard({ results }: ResultsDashboardProps) {
  return <TabbedDashboard results={results} />;
}

