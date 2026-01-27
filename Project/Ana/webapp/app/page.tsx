'use client';

import { useEffect, useState } from 'react';
import ExecutiveSummary from '@/components/ExecutiveSummary';
import KaiwaiChart from '@/components/KaiwaiChart';
import AirlineChart from '@/components/AirlineChart';
import CrossAnalysisTable from '@/components/CrossAnalysisTable';
import KaiwaiInsights from '@/components/KaiwaiInsights';
import ViralTopics from '@/components/ViralTopics';
import Recommendations from '@/components/Recommendations';
import type { AnalysisData } from '@/types/analysis';

export default function Dashboard() {
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/data/analysis.json')
      .then((res) => {
        if (!res.ok) throw new Error('データの読み込みに失敗しました');
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">データを読み込み中...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center p-8 bg-red-50 rounded-xl">
          <p className="text-red-600 font-medium mb-2">エラーが発生しました</p>
          <p className="text-red-500 text-sm">{error}</p>
          <p className="text-gray-500 text-sm mt-4">
            analysis.jsonが存在することを確認してください。
            <br />
            <code className="bg-gray-100 px-2 py-1 rounded">python analysis.py</code> を実行してJSONを生成してください。
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold mb-2">{data.meta.title}</h1>
          <p className="text-indigo-100">界隈分析ダッシュボード</p>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex flex-wrap gap-6 justify-center md:justify-start">
            <div className="text-center">
              <p className="text-2xl font-bold text-indigo-600">
                {data.basic_stats.total_posts.toLocaleString()}
              </p>
              <p className="text-xs text-gray-500">総投稿数</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600">
                {data.airline_counts.filter((a) => a.count > 0).length}
              </p>
              <p className="text-xs text-gray-500">言及航空会社</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-pink-600">
                {data.kaiwai_counts.filter((k) => k.name !== '未分類').length}
              </p>
              <p className="text-xs text-gray-500">界隈カテゴリ</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-amber-600">
                {data.basic_stats.avg_length}
              </p>
              <p className="text-xs text-gray-500">平均文字数</p>
            </div>
            <div className="ml-auto text-right hidden md:block">
              <p className="text-xs text-gray-400">
                データソース: {data.meta.data_source}
              </p>
              <p className="text-xs text-gray-400">
                生成日時: {new Date(data.meta.generated_at).toLocaleString('ja-JP')}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Executive Summary */}
        <ExecutiveSummary findings={data.executive_findings} />

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <KaiwaiChart data={data.kaiwai_counts} />
          <AirlineChart data={data.airline_counts} />
        </div>

        {/* Cross Analysis */}
        <CrossAnalysisTable
          data={data.cross_data}
          airlines={data.airline_counts}
          kaiwais={data.kaiwai_counts}
        />

        {/* Viral Topics */}
        <ViralTopics topics={data.viral_topics} />

        {/* Kaiwai Insights */}
        <KaiwaiInsights
          insights={data.kaiwai_insights}
          representativePosts={data.representative_posts}
        />

        {/* Recommendations */}
        <Recommendations recommendations={data.recommendations} />
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-400 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm">
          <p>界隈分析ダッシュボード - 北米ビジネスクラスX発話分析</p>
          <p className="mt-1">自動生成レポート by analysis.py</p>
        </div>
      </footer>
    </div>
  );
}
