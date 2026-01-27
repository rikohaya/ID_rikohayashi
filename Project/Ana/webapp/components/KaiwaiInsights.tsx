'use client';

import { useState } from 'react';

interface KaiwaiInsight {
  count: number;
  description: string;
  meaning: string;
  risk: string;
  opportunity: string;
  action: string;
}

interface KaiwaiInsightsProps {
  insights: Record<string, KaiwaiInsight>;
  representativePosts: Record<string, string[]>;
}

export default function KaiwaiInsights({
  insights,
  representativePosts,
}: KaiwaiInsightsProps) {
  const [openKaiwai, setOpenKaiwai] = useState<string | null>(null);

  const sortedKaiwais = Object.entries(insights).sort(
    ([, a], [, b]) => b.count - a.count
  );

  const getKaiwaiColor = (name: string) => {
    const colors: Record<string, string> = {
      ニュース拡散界隈: 'border-blue-500 bg-blue-50',
      ユーモア界隈: 'border-yellow-500 bg-yellow-50',
      クレーマー界隈: 'border-red-500 bg-red-50',
      マイラー界隈: 'border-purple-500 bg-purple-50',
      レビュアー界隈: 'border-green-500 bg-green-50',
      政治界隈: 'border-gray-500 bg-gray-50',
      インシデント界隈: 'border-orange-500 bg-orange-50',
    };
    return colors[name] || 'border-gray-300 bg-gray-50';
  };

  return (
    <section className="mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">界隈別インサイト</h2>
      <div className="space-y-4">
        {sortedKaiwais.map(([name, insight]) => (
          <div
            key={name}
            className={`rounded-xl border-l-4 ${getKaiwaiColor(name)} overflow-hidden shadow-sm`}
          >
            <button
              onClick={() => setOpenKaiwai(openKaiwai === name ? null : name)}
              className="w-full px-5 py-4 flex items-center justify-between text-left hover:bg-white/50 transition-colors"
            >
              <div className="flex items-center gap-4">
                <h3 className="text-lg font-semibold text-gray-800">{name}</h3>
                <span className="px-2 py-1 bg-white rounded-full text-sm font-medium text-gray-600">
                  {insight.count.toLocaleString()}件
                </span>
              </div>
              <svg
                className={`w-5 h-5 text-gray-400 transition-transform ${
                  openKaiwai === name ? 'rotate-180' : ''
                }`}
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            {openKaiwai === name && (
              <div className="px-5 pb-5 bg-white/70">
                <p className="text-sm text-gray-600 mb-4">{insight.description}</p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div className="p-3 bg-white rounded-lg">
                    <h4 className="text-sm font-semibold text-gray-700 mb-1">
                      意味するもの
                    </h4>
                    <p className="text-sm text-gray-600">{insight.meaning}</p>
                  </div>
                  <div className="p-3 bg-white rounded-lg">
                    <h4 className="text-sm font-semibold text-gray-700 mb-1">
                      推奨アクション
                    </h4>
                    <p className="text-sm text-gray-600">{insight.action}</p>
                  </div>
                  <div className="p-3 bg-red-50 rounded-lg">
                    <h4 className="text-sm font-semibold text-red-700 mb-1">
                      リスク
                    </h4>
                    <p className="text-sm text-red-600">{insight.risk}</p>
                  </div>
                  <div className="p-3 bg-green-50 rounded-lg">
                    <h4 className="text-sm font-semibold text-green-700 mb-1">
                      機会
                    </h4>
                    <p className="text-sm text-green-600">{insight.opportunity}</p>
                  </div>
                </div>

                {representativePosts[name] && representativePosts[name].length > 0 && (
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">
                      代表的な投稿
                    </h4>
                    <div className="space-y-2">
                      {representativePosts[name].slice(0, 3).map((post, i) => (
                        <div
                          key={i}
                          className="p-3 bg-white rounded-lg text-sm text-gray-600 border border-gray-100"
                        >
                          {post}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
