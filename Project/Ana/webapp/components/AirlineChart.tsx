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

interface AirlineChartProps {
  data: Array<{
    name: string;
    count: number;
  }>;
}

const COLORS = [
  '#F97316', // orange
  '#EAB308', // yellow
  '#22C55E', // green
  '#14B8A6', // teal
  '#0EA5E9', // sky
  '#6366F1', // indigo
  '#A855F7', // purple
  '#EC4899', // pink
  '#F43F5E', // rose
  '#78716C', // stone
];

export default function AirlineChart({ data }: AirlineChartProps) {
  const top10 = data.slice(0, 10);

  return (
    <section className="bg-white rounded-xl shadow-md p-6 mb-8">
      <h2 className="text-xl font-bold text-gray-800 mb-4">航空会社別言及数（上位10社）</h2>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={top10}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis type="number" stroke="#6B7280" />
            <YAxis
              type="category"
              dataKey="name"
              stroke="#6B7280"
              width={90}
              tick={{ fontSize: 12 }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #E5E7EB',
                borderRadius: '8px',
              }}
              formatter={(value: number) => [`${value.toLocaleString()}件`, '言及数']}
            />
            <Bar dataKey="count" radius={[0, 4, 4, 0]}>
              {top10.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
