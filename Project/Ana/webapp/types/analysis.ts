export interface AnalysisData {
  meta: {
    title: string;
    generated_at: string;
    data_source: string;
  };
  basic_stats: {
    total_posts: number;
    avg_length: number;
    max_length: number;
    min_length: number;
  };
  airline_counts: Array<{
    name: string;
    count: number;
  }>;
  kaiwai_counts: Array<{
    name: string;
    count: number;
    description: string;
  }>;
  cross_data: Record<string, Record<string, number>>;
  viral_topics: Array<{
    topic: string;
    count: number;
    type: string;
    risk_level: string;
    description: string;
    sample_posts: string[];
  }>;
  executive_findings: string[];
  recommendations: {
    航空会社向け: string[];
    SNS戦略: string[];
  };
  kaiwai_insights: Record<string, {
    count: number;
    description: string;
    meaning: string;
    risk: string;
    opportunity: string;
    action: string;
  }>;
  representative_posts: Record<string, string[]>;
}
