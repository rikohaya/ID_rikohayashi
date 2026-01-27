'use client';

interface ExecutiveSummaryProps {
  findings: string[];
}

export default function ExecutiveSummary({ findings }: ExecutiveSummaryProps) {
  const getIcon = (index: number) => {
    const icons = ['📊', '🎯', '⚠️', '📢', '✅'];
    return icons[index % icons.length];
  };

  const getGradient = (index: number) => {
    const gradients = [
      'from-blue-500 to-blue-600',
      'from-purple-500 to-purple-600',
      'from-orange-500 to-orange-600',
      'from-red-500 to-red-600',
      'from-green-500 to-green-600',
    ];
    return gradients[index % gradients.length];
  };

  return (
    <section className="mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">エグゼクティブサマリー</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {findings.map((finding, index) => {
          const cleanFinding = finding.replace(/\*\*/g, '');
          const [title, ...rest] = cleanFinding.split(':');
          const content = rest.join(':').trim();

          return (
            <div
              key={index}
              className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow"
            >
              <div className={`h-2 bg-gradient-to-r ${getGradient(index)}`} />
              <div className="p-4">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">{getIcon(index)}</span>
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-1">{title}</h3>
                    <p className="text-sm text-gray-600">{content}</p>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
