'use client';

interface ViralTopic {
  topic: string;
  count: number;
  type: string;
  risk_level: string;
  description: string;
  sample_posts: string[];
}

interface ViralTopicsProps {
  topics: ViralTopic[];
}

export default function ViralTopics({ topics }: ViralTopicsProps) {
  if (!topics || topics.length === 0) {
    return (
      <section className="bg-white rounded-xl shadow-md p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">注目トピック</h2>
        <p className="text-gray-500">特筆すべきバイラルトピックは検出されませんでした。</p>
      </section>
    );
  }

  const getTypeStyle = (type: string) => {
    switch (type) {
      case '炎上リスク':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'バイラル':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'ポジティブ':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getRiskBadge = (level: string) => {
    switch (level) {
      case '高':
        return 'bg-red-500 text-white';
      case '中':
        return 'bg-yellow-500 text-white';
      case '低':
        return 'bg-blue-500 text-white';
      default:
        return 'bg-green-500 text-white';
    }
  };

  const getIcon = (type: string) => {
    switch (type) {
      case '炎上リスク':
        return '🔥';
      case 'バイラル':
        return '📈';
      case 'ポジティブ':
        return '✨';
      default:
        return '📌';
    }
  };

  return (
    <section className="bg-white rounded-xl shadow-md p-6 mb-8">
      <h2 className="text-xl font-bold text-gray-800 mb-4">注目トピック</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {topics.map((topic, index) => (
          <div
            key={index}
            className={`rounded-lg border p-4 ${getTypeStyle(topic.type)}`}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-xl">{getIcon(topic.type)}</span>
                <h3 className="font-semibold">{topic.topic}</h3>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">{topic.count}件</span>
                {topic.risk_level !== 'なし' && (
                  <span
                    className={`px-2 py-0.5 rounded-full text-xs font-medium ${getRiskBadge(
                      topic.risk_level
                    )}`}
                  >
                    リスク:{topic.risk_level}
                  </span>
                )}
              </div>
            </div>
            <p className="text-sm mb-3">{topic.description}</p>
            {topic.sample_posts && topic.sample_posts.length > 0 && (
              <div className="mt-2 pt-2 border-t border-current/10">
                <p className="text-xs font-medium mb-1">サンプル投稿:</p>
                <p className="text-xs opacity-80 line-clamp-2">
                  {topic.sample_posts[0]}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}
