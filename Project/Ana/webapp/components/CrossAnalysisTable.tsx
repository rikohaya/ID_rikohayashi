'use client';

interface CrossAnalysisTableProps {
  data: Record<string, Record<string, number>>;
  airlines: Array<{ name: string; count: number }>;
  kaiwais: Array<{ name: string; count: number }>;
}

export default function CrossAnalysisTable({
  data,
  airlines,
  kaiwais,
}: CrossAnalysisTableProps) {
  const topAirlines = airlines.filter((a) => a.count > 0).slice(0, 8);
  const kaiwaiNames = kaiwais
    .filter((k) => k.name !== '未分類')
    .map((k) => k.name);

  const getHeatColor = (value: number, max: number): string => {
    if (value === 0) return 'bg-gray-50';
    const intensity = Math.min(value / max, 1);
    if (intensity < 0.25) return 'bg-blue-100 text-blue-800';
    if (intensity < 0.5) return 'bg-blue-200 text-blue-900';
    if (intensity < 0.75) return 'bg-blue-400 text-white';
    return 'bg-blue-600 text-white';
  };

  // Find max value for color scaling
  let maxValue = 0;
  topAirlines.forEach((airline) => {
    kaiwaiNames.forEach((kaiwai) => {
      const value = data[airline.name]?.[kaiwai] || 0;
      if (value > maxValue) maxValue = value;
    });
  });

  return (
    <section className="bg-white rounded-xl shadow-md p-6 mb-8 overflow-x-auto">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        航空会社×界隈 クロス分析
      </h2>
      <p className="text-sm text-gray-500 mb-4">
        各航空会社がどの界隈でどれだけ言及されているかをヒートマップで表示
      </p>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr>
              <th className="sticky left-0 bg-white px-3 py-2 text-left font-semibold text-gray-700 border-b">
                航空会社
              </th>
              {kaiwaiNames.map((kaiwai) => (
                <th
                  key={kaiwai}
                  className="px-2 py-2 text-center font-semibold text-gray-700 border-b whitespace-nowrap"
                >
                  {kaiwai.replace('界隈', '')}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {topAirlines.map((airline, i) => (
              <tr key={airline.name} className={i % 2 === 0 ? 'bg-gray-50/50' : ''}>
                <td className="sticky left-0 bg-white px-3 py-2 font-medium text-gray-800 border-b whitespace-nowrap">
                  {airline.name}
                </td>
                {kaiwaiNames.map((kaiwai) => {
                  const value = data[airline.name]?.[kaiwai] || 0;
                  return (
                    <td
                      key={kaiwai}
                      className={`px-2 py-2 text-center border-b ${getHeatColor(
                        value,
                        maxValue
                      )}`}
                    >
                      {value > 0 ? value : '-'}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 flex items-center gap-2 text-xs text-gray-500">
        <span>凡例:</span>
        <span className="px-2 py-1 bg-gray-50 rounded">低</span>
        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">中低</span>
        <span className="px-2 py-1 bg-blue-200 text-blue-900 rounded">中</span>
        <span className="px-2 py-1 bg-blue-400 text-white rounded">中高</span>
        <span className="px-2 py-1 bg-blue-600 text-white rounded">高</span>
      </div>
    </section>
  );
}
