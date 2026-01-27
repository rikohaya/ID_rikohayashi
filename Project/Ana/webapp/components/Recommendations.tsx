'use client';

interface RecommendationsProps {
  recommendations: {
    航空会社向け: string[];
    SNS戦略: string[];
  };
}

export default function Recommendations({ recommendations }: RecommendationsProps) {
  return (
    <section className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl shadow-md p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">総合提言</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 航空会社向け */}
        <div className="bg-white rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">✈️</span>
            <h3 className="text-lg font-semibold text-gray-800">航空会社向け推奨事項</h3>
          </div>
          <ul className="space-y-3">
            {recommendations.航空会社向け.map((rec, index) => (
              <li key={index} className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-sm font-medium">
                  {index + 1}
                </span>
                <p className="text-sm text-gray-600 leading-relaxed">{rec}</p>
              </li>
            ))}
          </ul>
        </div>

        {/* SNS戦略 */}
        <div className="bg-white rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <span className="text-2xl">📱</span>
            <h3 className="text-lg font-semibold text-gray-800">SNS戦略への示唆</h3>
          </div>
          <ul className="space-y-3">
            {recommendations.SNS戦略.map((rec, index) => (
              <li key={index} className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center text-sm font-medium">
                  {index + 1}
                </span>
                <p className="text-sm text-gray-600 leading-relaxed">{rec}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
