"""メディアプラン計算ロジック"""
from typing import Optional

# 日本人口データ（年齢層別・万人）
POPULATION_DATA = {
    "10代": 11_000_000,
    "20代": 12_500_000,
    "30代": 13_800_000,
    "40代": 17_500_000,
    "50代": 16_800_000,
    "60代以上": 44_000_000,
}

# 性別比率
GENDER_RATIO = {
    "男性": 0.49,
    "女性": 0.51,
    "全体": 1.0,
}

# 媒体利用率（年齢層 × 性別 → 媒体利用率）
MEDIA_USAGE_RATE = {
    "X": {
        "10代": {"男性": 0.54, "女性": 0.58, "全体": 0.56},
        "20代": {"男性": 0.68, "女性": 0.72, "全体": 0.70},
        "30代": {"男性": 0.42, "女性": 0.45, "全体": 0.44},
        "40代": {"男性": 0.32, "女性": 0.30, "全体": 0.31},
        "50代": {"男性": 0.22, "女性": 0.20, "全体": 0.21},
        "60代以上": {"男性": 0.10, "女性": 0.08, "全体": 0.09},
    },
    "Instagram": {
        "10代": {"男性": 0.62, "女性": 0.78, "全体": 0.70},
        "20代": {"男性": 0.55, "女性": 0.75, "全体": 0.65},
        "30代": {"男性": 0.42, "女性": 0.58, "全体": 0.50},
        "40代": {"男性": 0.38, "女性": 0.48, "全体": 0.43},
        "50代": {"男性": 0.25, "女性": 0.35, "全体": 0.30},
        "60代以上": {"男性": 0.12, "女性": 0.18, "全体": 0.15},
    },
    "TikTok": {
        "10代": {"男性": 0.55, "女性": 0.65, "全体": 0.60},
        "20代": {"男性": 0.40, "女性": 0.50, "全体": 0.45},
        "30代": {"男性": 0.25, "女性": 0.32, "全体": 0.28},
        "40代": {"男性": 0.18, "女性": 0.22, "全体": 0.20},
        "50代": {"男性": 0.10, "女性": 0.12, "全体": 0.11},
        "60代以上": {"男性": 0.05, "女性": 0.06, "全体": 0.055},
    },
    "YouTube": {
        "10代": {"男性": 0.92, "女性": 0.88, "全体": 0.90},
        "20代": {"男性": 0.90, "女性": 0.85, "全体": 0.87},
        "30代": {"男性": 0.85, "女性": 0.78, "全体": 0.81},
        "40代": {"男性": 0.78, "女性": 0.70, "全体": 0.74},
        "50代": {"男性": 0.65, "女性": 0.55, "全体": 0.60},
        "60代以上": {"男性": 0.40, "女性": 0.30, "全体": 0.35},
    },
    "LINE": {
        "10代": {"男性": 0.90, "女性": 0.95, "全体": 0.92},
        "20代": {"男性": 0.95, "女性": 0.97, "全体": 0.96},
        "30代": {"男性": 0.92, "女性": 0.95, "全体": 0.93},
        "40代": {"男性": 0.88, "女性": 0.92, "全体": 0.90},
        "50代": {"男性": 0.80, "女性": 0.85, "全体": 0.82},
        "60代以上": {"男性": 0.55, "女性": 0.60, "全体": 0.57},
    },
    "Facebook": {
        "10代": {"男性": 0.08, "女性": 0.06, "全体": 0.07},
        "20代": {"男性": 0.18, "女性": 0.15, "全体": 0.16},
        "30代": {"男性": 0.28, "女性": 0.25, "全体": 0.26},
        "40代": {"男性": 0.32, "女性": 0.28, "全体": 0.30},
        "50代": {"男性": 0.28, "女性": 0.25, "全体": 0.26},
        "60代以上": {"男性": 0.18, "女性": 0.15, "全体": 0.16},
    },
}

# デフォルトCPM（円）
DEFAULT_CPM = {
    "X": 400,
    "Instagram": 500,
    "TikTok": 600,
    "YouTube": 700,
    "LINE": 350,
    "Facebook": 450,
}


def get_target_population(age_group: str, gender: str, media: str) -> int:
    """ターゲット人口を計算"""
    base_population = POPULATION_DATA.get(age_group, 0)
    gender_ratio = GENDER_RATIO.get(gender, 1.0)
    media_usage = MEDIA_USAGE_RATE.get(media, {}).get(age_group, {}).get(gender, 0)

    return int(base_population * gender_ratio * media_usage)


def calculate_normal(
    age_group: str,
    gender: str,
    media: str,
    reach_rate: float,
    frequency: int,
    cpm: Optional[float] = None,
) -> dict:
    """通常計算: ターゲット × 媒体 → 費用算出"""
    if cpm is None:
        cpm = DEFAULT_CPM.get(media, 400)

    target_population = get_target_population(age_group, gender, media)
    reach_count = int(target_population * (reach_rate / 100))
    total_impressions = reach_count * frequency
    estimated_cost = int(total_impressions / 1000 * cpm)

    return {
        "target_population": target_population,
        "reach_count": reach_count,
        "total_impressions": total_impressions,
        "estimated_cost": estimated_cost,
        "cpm_used": cpm,
    }


def calculate_reverse(
    age_group: str,
    gender: str,
    media: str,
    budget: int,
    frequency: int,
    cpm: Optional[float] = None,
) -> dict:
    """予算逆算: 予算 → リーチ可能人数算出"""
    if cpm is None:
        cpm = DEFAULT_CPM.get(media, 400)

    target_population = get_target_population(age_group, gender, media)

    # 予算からインプレッション数を計算
    max_impressions = int(budget / cpm * 1000)

    # フリークエンシーで割ってリーチ人数を算出
    max_reach = int(max_impressions / frequency)

    # リーチ率を計算（ターゲット人口に対する割合）
    reach_rate_achievable = (max_reach / target_population * 100) if target_population > 0 else 0

    return {
        "target_population": target_population,
        "max_reach": max_reach,
        "max_impressions": max_impressions,
        "reach_rate_achievable": round(reach_rate_achievable, 2),
        "cpm_used": cpm,
    }


def get_available_options() -> dict:
    """利用可能なオプションを取得"""
    return {
        "age_groups": list(POPULATION_DATA.keys()),
        "genders": list(GENDER_RATIO.keys()),
        "media_types": list(MEDIA_USAGE_RATE.keys()),
        "default_cpm": DEFAULT_CPM,
    }


def calculate_with_custom_population(
    target_population: int,
    media: str,
    reach_rate: float,
    frequency: int,
    cpm: Optional[float] = None,
) -> dict:
    """カスタム人口での通常計算"""
    if cpm is None:
        cpm = DEFAULT_CPM.get(media, 400)

    reach_count = int(target_population * (reach_rate / 100))
    total_impressions = reach_count * frequency
    estimated_cost = int(total_impressions / 1000 * cpm)

    return {
        "target_population": target_population,
        "reach_count": reach_count,
        "total_impressions": total_impressions,
        "estimated_cost": estimated_cost,
        "cpm_used": cpm,
    }


def reverse_with_custom_population(
    target_population: int,
    media: str,
    budget: int,
    frequency: int,
    cpm: Optional[float] = None,
) -> dict:
    """カスタム人口での予算逆算"""
    if cpm is None:
        cpm = DEFAULT_CPM.get(media, 400)

    max_impressions = int(budget / cpm * 1000)
    max_reach = int(max_impressions / frequency)
    reach_rate_achievable = (max_reach / target_population * 100) if target_population > 0 else 0

    return {
        "target_population": target_population,
        "max_reach": max_reach,
        "max_impressions": max_impressions,
        "reach_rate_achievable": round(reach_rate_achievable, 2),
        "cpm_used": cpm,
    }
