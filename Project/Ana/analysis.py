#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北米ビジネスクラスX発話 界隈分析スクリプト
"""

import pandas as pd
import matplotlib.pyplot as plt
import re
import base64
import json
from collections import Counter
from pathlib import Path

# 日本語フォント設定
try:
    import japanize_matplotlib
except ImportError:
    plt.rcParams['font.family'] = ['Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'sans-serif']

# パス設定
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "北米・欧州ビジネスクラスインサイト調査 - 北米X発話.csv"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ========================================
# 界隈定義（キーワードベース）
# ========================================
KAIWAI_DEFINITIONS = {
    "クレーマー界隈": {
        "keywords": [
            r"\bworst\b", r"\bterrible\b", r"\bpathetic\b", r"\bshame\b",
            r"\bunacceptable\b", r"\bboycott\b", r"\bdisgusting\b", r"\bawful\b",
            r"\bhate\b", r"\bangry\b", r"\bfurious\b", r"\bembarrassing\b",
            r"\bhorrible\b", r"\bwon'?t fly\b", r"\bnever again\b", r"\brip off\b",
            r"\bdisappointed\b", r"\bdisrespect\b"
        ],
        "description": "苦情・不満を投稿するユーザー"
    },
    "レビュアー界隈": {
        "keywords": [
            r"\breview\b", r"\bexperience\b", r"\bblog\b", r"\btried\b",
            r"\bcheck out\b", r"\bvia @youtube\b", r"\bflight report\b",
            r"\benjoying\b", r"\bflying solo\b", r"\bflight on\b"
        ],
        "description": "レビュー・体験共有をするユーザー"
    },
    "マイラー界隈": {
        "keywords": [
            r"\bpoints\b", r"\bmiles\b", r"\bupgrade\b", r"\bredemption\b",
            r"\btransfer\b", r"\bpromo\b", r"\bbonus\b", r"\blounge\b",
            r"\bstatus\b", r"\belite\b", r"\breward[s]?\b", r"\bflying blue\b"
        ],
        "description": "マイル・ポイント活用に関心があるユーザー"
    },
    "ニュース拡散界隈": {
        "keywords": [
            r"QT @", r"\breport\b", r"\bbreaking\b", r"\bnews\b",
            r"\balleges?\b", r"\baccording to\b", r"\bdiverted\b"
        ],
        "description": "ニュースのRT・引用をするユーザー"
    },
    "政治界隈": {
        "keywords": [
            r"\btrump\b", r"\bbiden\b", r"\bminister\b", r"\bpolitician\b",
            r"\bgovernment\b", r"\bcongress\b", r"\bsenator\b", r"\bpolitics\b",
            r"\bjagmeet\b", r"\btrudeau\b"
        ],
        "description": "政治的な言及をするユーザー"
    },
    "ユーモア界隈": {
        "keywords": [
            r"😂", r"🤣", r"\blol\b", r"\bhaha\b", r"\bfunny\b",
            r"\bearned the (?:view|sight)\b", r"\bhilarious\b", r"\bjoke\b",
            r"😁", r"😅"
        ],
        "description": "ジョーク・ユーモアを交えて投稿するユーザー"
    },
    "インシデント界隈": {
        "keywords": [
            r"\bchaos\b", r"\btackle[ds]?\b", r"\bthrow[ns]?\b", r"\bfight\b",
            r"\barrest\b", r"\bpolice\b", r"\bdisrupt\b", r"\bincident\b",
            r"\bvaping\b", r"\bdrunk\b", r"\bkick\b", r"\bcockpit\b"
        ],
        "description": "機内でのトラブル・インシデントに言及するユーザー"
    }
}

# 航空会社リスト
AIRLINES = {
    "American Airlines": [r"\bamerican airlines\b", r"\b@americanair\b", r"\baa\b"],
    "United Airlines": [r"\bunited airlines\b", r"\b@united\b"],
    "Delta Air Lines": [r"\bdelta\b", r"\b@delta\b"],
    "Lufthansa": [r"\blufthansa\b", r"\b@lufthansa\b"],
    "British Airways": [r"\bbritish airways\b", r"\b@british_airways\b", r"\bba\b"],
    "Air France": [r"\bair france\b", r"\b@airfrance\b"],
    "Air Canada": [r"\bair canada\b", r"\b@aircanada\b"],
    "Emirates": [r"\bemirates\b", r"\b@emirates\b"],
    "Ryanair": [r"\bryanair\b", r"\b@ryanair\b"],
    "Iberia": [r"\biberia\b", r"\b@iberia\b"],
    "KLM": [r"\bklm\b", r"\b@klm\b"],
    "Swiss": [r"\bswiss\b", r"\b@flyswiss\b"],
    "Air India": [r"\bair india\b", r"\b@airindia\b"],
}

# ========================================
# 界隈別ビジネスインサイト定義
# ========================================
KAIWAI_INSIGHTS = {
    "クレーマー界隈": {
        "meaning": "顧客不満が表面化している領域。サービス品質、対応の遅れ、期待値とのギャップが原因",
        "risk": "ブランドイメージの毀損、口コミによる新規顧客獲得の阻害、既存顧客の離反",
        "opportunity": "改善ポイントの特定、競合との差別化要素の発見",
        "action": "カスタマーサポートの強化、不満の根本原因分析、プロアクティブな顧客対応"
    },
    "レビュアー界隈": {
        "meaning": "インフルエンサーや体験共有者による情報発信。購買意思決定に影響",
        "risk": "ネガティブレビューの拡散、競合他社との比較での劣位",
        "opportunity": "ポジティブな口コミ創出、ブランドアンバサダーの発掘",
        "action": "レビュアーとの関係構築、体験価値の向上、SNS施策との連携"
    },
    "マイラー界隈": {
        "meaning": "ロイヤルティプログラムに高い関心を持つ層。LTV（顧客生涯価値）が高い傾向",
        "risk": "競合のプログラム改善による顧客流出、ポイント価値の希薄化への不満",
        "opportunity": "リピーター育成、アップセル・クロスセルの機会",
        "action": "特典の差別化、エリートステータスの価値向上、パートナーシップ拡大"
    },
    "ニュース拡散界隈": {
        "meaning": "情報の拡散力が高い層。ニュースやトレンドに敏感",
        "risk": "ネガティブニュースの急速な拡散、誤情報の流布",
        "opportunity": "ポジティブニュースの効果的な拡散、メディアリレーションの強化",
        "action": "プレスリリースのタイミング最適化、ファクトチェック体制の整備"
    },
    "政治界隈": {
        "meaning": "政治的文脈での航空会社言及。政策や規制との関連",
        "risk": "政治的論争への巻き込まれ、特定の立場との関連付け",
        "opportunity": "政策提言への参画、業界としての発言力強化",
        "action": "政治的中立性の維持、ステークホルダーとの関係構築"
    },
    "ユーモア界隈": {
        "meaning": "航空会社がミーム・ジョークの題材に。ブランド認知の一形態",
        "risk": "揶揄的な文脈でのブランド消費、イメージのコントロール困難",
        "opportunity": "バイラル効果によるブランド認知向上、親しみやすさの醸成",
        "action": "ユーモアを活かしたSNS運用、適切なトーン&マナーの設定"
    },
    "インシデント界隈": {
        "meaning": "機内トラブル・安全性に関する言及。メディア注目度が高い",
        "risk": "安全性への不安喚起、企業イメージの深刻な毀損",
        "opportunity": "危機管理能力のアピール、安全への取り組みの可視化",
        "action": "迅速な情報開示、クライシスコミュニケーション体制の強化"
    },
    "未分類": {
        "meaning": "特定のパターンに該当しない一般的な言及",
        "risk": "潜在的なトレンドの見落とし",
        "opportunity": "新しい界隈・トピックの発見",
        "action": "定期的な分類ルールの見直し、新キーワードの追加"
    }
}


def load_data():
    """データを読み込む"""
    df = pd.read_csv(DATA_FILE)
    print(f"データ読み込み完了: {len(df)} 件")
    return df


def basic_stats(df):
    """基本統計を計算"""
    stats = {
        "総投稿数": len(df),
        "平均文字数": df["content"].str.len().mean(),
        "最大文字数": df["content"].str.len().max(),
        "最小文字数": df["content"].str.len().min(),
    }
    return stats


def classify_kaiwai(text):
    """テキストを界隈に分類（複数該当可）"""
    text_lower = text.lower()
    matched = []

    for kaiwai_name, definition in KAIWAI_DEFINITIONS.items():
        for pattern in definition["keywords"]:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matched.append(kaiwai_name)
                break

    return matched if matched else ["未分類"]


def count_airlines(df):
    """航空会社の言及数をカウント"""
    counts = {}
    for airline, patterns in AIRLINES.items():
        count = 0
        for _, row in df.iterrows():
            text_lower = row["content"].lower()
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    count += 1
                    break
        counts[airline] = count
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def analyze_kaiwai(df):
    """界隈分析を実行"""
    # 各投稿を分類
    df["kaiwai"] = df["content"].apply(classify_kaiwai)

    # 界隈別カウント
    kaiwai_counts = Counter()
    for kaiwais in df["kaiwai"]:
        for k in kaiwais:
            kaiwai_counts[k] += 1

    return df, dict(kaiwai_counts)


def get_representative_posts(df, kaiwai_name, n=3):
    """各界隈の代表的な投稿を取得"""
    posts = []
    for idx, row in df.iterrows():
        if kaiwai_name in row["kaiwai"]:
            posts.append(row["content"][:200] + "..." if len(row["content"]) > 200 else row["content"])
            if len(posts) >= n:
                break
    return posts


def analyze_airline_kaiwai_cross(df):
    """航空会社×界隈のクロス分析を実行"""
    # 航空会社と界隈のクロス集計
    cross_data = {}

    for airline, patterns in AIRLINES.items():
        cross_data[airline] = {}
        for kaiwai_name in KAIWAI_DEFINITIONS.keys():
            cross_data[airline][kaiwai_name] = 0
        cross_data[airline]["未分類"] = 0

    for _, row in df.iterrows():
        text_lower = row["content"].lower()
        kaiwais = row["kaiwai"]

        # この投稿がどの航空会社に言及しているか
        for airline, patterns in AIRLINES.items():
            mentioned = False
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    mentioned = True
                    break

            if mentioned:
                for k in kaiwais:
                    cross_data[airline][k] += 1

    return cross_data


def detect_viral_topics(df):
    """バイラル・注目トピックを検出"""
    topics = []

    # BA窓付きトイレの検出
    ba_toilet_count = 0
    ba_toilet_posts = []
    for _, row in df.iterrows():
        text_lower = row["content"].lower()
        if ("british airways" in text_lower or "ba" in text_lower) and \
           ("toilet" in text_lower or "window" in text_lower or "loo" in text_lower):
            ba_toilet_count += 1
            if len(ba_toilet_posts) < 2:
                ba_toilet_posts.append(row["content"][:150] + "...")

    if ba_toilet_count > 0:
        topics.append({
            "topic": "BA窓付きトイレ話題",
            "count": ba_toilet_count,
            "type": "バイラル",
            "risk_level": "低",
            "description": "British Airwaysの窓付きトイレがSNSで話題に。ユニークなプロダクトとして注目",
            "sample_posts": ba_toilet_posts
        })

    # インシデント関連のバイラル検出
    incident_keywords = [
        (r"\bfight\b.*\b(passenger|crew)\b", "機内トラブル・乗客間トラブル"),
        (r"\barrest\b", "逮捕関連インシデント"),
        (r"\bdiverted\b", "緊急着陸・ダイバート"),
        (r"\bvaping\b", "機内での電子タバコ問題"),
    ]

    for pattern, desc in incident_keywords:
        matches = []
        for _, row in df.iterrows():
            if re.search(pattern, row["content"].lower()):
                matches.append(row["content"][:150] + "...")

        if len(matches) >= 3:
            topics.append({
                "topic": desc,
                "count": len(matches),
                "type": "炎上リスク",
                "risk_level": "高",
                "description": f"'{desc}'に関する投稿が{len(matches)}件検出。メディア注目度が高い可能性",
                "sample_posts": matches[:2]
            })

    # ポジティブバイラルの検出
    positive_patterns = [
        (r"\b(amazing|incredible|best)\b.*\b(business class|first class)\b", "ポジティブ体験共有"),
        (r"\bupgrade[d]?\b.*\bfree\b", "無料アップグレード体験"),
    ]

    for pattern, desc in positive_patterns:
        matches = []
        for _, row in df.iterrows():
            if re.search(pattern, row["content"].lower()):
                matches.append(row["content"][:150] + "...")

        if len(matches) >= 2:
            topics.append({
                "topic": desc,
                "count": len(matches),
                "type": "ポジティブ",
                "risk_level": "なし",
                "description": f"'{desc}'に関するポジティブな投稿が{len(matches)}件。SNS活用の好事例",
                "sample_posts": matches[:2]
            })

    return topics


def generate_executive_summary(df, kaiwai_counts, airline_counts, cross_data):
    """エグゼクティブサマリーを生成"""
    findings = []

    # 1. 最も言及の多い航空会社
    top_airline = list(airline_counts.items())[0] if airline_counts else ("不明", 0)
    findings.append(f"**最多言及航空会社**: {top_airline[0]}（{top_airline[1]}件）が最も多く言及されている")

    # 2. 最も活発な界隈
    kaiwai_sorted = sorted([(k, v) for k, v in kaiwai_counts.items() if k != "未分類"],
                          key=lambda x: x[1], reverse=True)
    if kaiwai_sorted:
        top_kaiwai = kaiwai_sorted[0]
        findings.append(f"**最活発界隈**: {top_kaiwai[0]}（{top_kaiwai[1]}件）が最も活発")

    # 3. インシデント界隈で最も言及される航空会社
    incident_airlines = [(airline, data.get("インシデント界隈", 0))
                        for airline, data in cross_data.items()]
    incident_airlines.sort(key=lambda x: x[1], reverse=True)
    top_incident = incident_airlines[0] if incident_airlines else ("不明", 0)
    if top_incident[1] > 0:
        findings.append(f"**インシデント注意**: {top_incident[0]}はインシデント界隈での言及が最多（{top_incident[1]}件）")

    # 4. クレーマー界隈で最も言及される航空会社
    complainer_airlines = [(airline, data.get("クレーマー界隈", 0))
                          for airline, data in cross_data.items()]
    complainer_airlines.sort(key=lambda x: x[1], reverse=True)
    top_complainer = complainer_airlines[0] if complainer_airlines else ("不明", 0)
    if top_complainer[1] > 0:
        findings.append(f"**顧客不満注意**: {top_complainer[0]}はクレーマー界隈での言及が最多（{top_complainer[1]}件）")

    # 5. 未分類の割合
    unclassified_rate = (kaiwai_counts.get("未分類", 0) / len(df)) * 100
    findings.append(f"**分類カバレッジ**: {100 - unclassified_rate:.1f}%の投稿が界隈に分類済み")

    return findings


def generate_recommendations(df, kaiwai_counts, airline_counts, cross_data, viral_topics):
    """総合提言を生成"""
    recommendations = {
        "航空会社向け": [],
        "SNS戦略": []
    }

    # 航空会社向け提言
    # インシデント対応
    incident_count = kaiwai_counts.get("インシデント界隈", 0)
    if incident_count > 10:
        recommendations["航空会社向け"].append(
            "インシデント関連の投稿が多数検出されています。クライシスコミュニケーション体制を見直し、"
            "迅速な情報開示と顧客対応のプロトコルを確立することを推奨します。"
        )

    # クレーマー対応
    complainer_count = kaiwai_counts.get("クレーマー界隈", 0)
    if complainer_count > 20:
        recommendations["航空会社向け"].append(
            "顧客不満の投稿が目立ちます。カスタマーサポートの応対品質向上と、"
            "SNS上でのプロアクティブな顧客対応（ソーシャルリスニング）を強化することを推奨します。"
        )

    # マイラー対応
    miler_count = kaiwai_counts.get("マイラー界隈", 0)
    if miler_count > 10:
        recommendations["航空会社向け"].append(
            "マイラー層からの関心が高いです。ロイヤルティプログラムの競争力を維持・強化し、"
            "エリート会員向けの差別化されたサービスを提供することでLTV向上が期待できます。"
        )

    # SNS戦略提言
    reviewer_count = kaiwai_counts.get("レビュアー界隈", 0)
    if reviewer_count > 5:
        recommendations["SNS戦略"].append(
            "レビュアー・インフルエンサーの存在が確認されています。ブランドアンバサダー施策や、"
            "体験価値の高いサービスのPR協力依頼を検討してください。"
        )

    humor_count = kaiwai_counts.get("ユーモア界隈", 0)
    if humor_count > 5:
        recommendations["SNS戦略"].append(
            "ユーモア・ミーム文脈での言及があります。公式SNSアカウントで適度なユーモアを交えた"
            "投稿を行うことで、親しみやすさとエンゲージメント向上が期待できます。"
        )

    # バイラルトピック関連
    for topic in viral_topics:
        if topic["type"] == "炎上リスク":
            recommendations["SNS戦略"].append(
                f"「{topic['topic']}」に関する投稿が検出されています。炎上リスクに備え、"
                "想定Q&Aとステートメントを事前準備することを推奨します。"
            )
        elif topic["type"] == "バイラル":
            recommendations["SNS戦略"].append(
                f"「{topic['topic']}」がバイラルしています。ポジティブな話題として"
                "公式アカウントからも発信し、認知拡大に活用することを検討してください。"
            )

    # デフォルト提言
    if not recommendations["航空会社向け"]:
        recommendations["航空会社向け"].append(
            "現時点で大きな問題は検出されていません。継続的なモニタリングを推奨します。"
        )

    if not recommendations["SNS戦略"]:
        recommendations["SNS戦略"].append(
            "各界隈の動向を継続的に監視し、トレンドに合わせた発信を行うことを推奨します。"
        )

    return recommendations


def create_visualizations(kaiwai_counts, airline_counts):
    """可視化グラフを作成"""
    # 界隈別投稿数グラフ
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 界隈別グラフ
    kaiwai_sorted = dict(sorted(kaiwai_counts.items(), key=lambda x: x[1], reverse=True))
    ax1 = axes[0]
    bars1 = ax1.barh(list(kaiwai_sorted.keys()), list(kaiwai_sorted.values()), color='steelblue')
    ax1.set_xlabel('投稿数')
    ax1.set_title('界隈別投稿数')
    ax1.invert_yaxis()
    for bar, val in zip(bars1, kaiwai_sorted.values()):
        ax1.text(val + 5, bar.get_y() + bar.get_height()/2, str(val), va='center')

    # 航空会社別グラフ（上位10社）
    top_airlines = dict(list(airline_counts.items())[:10])
    ax2 = axes[1]
    bars2 = ax2.barh(list(top_airlines.keys()), list(top_airlines.values()), color='coral')
    ax2.set_xlabel('言及数')
    ax2.set_title('航空会社別言及数（上位10社）')
    ax2.invert_yaxis()
    for bar, val in zip(bars2, top_airlines.values()):
        ax2.text(val + 5, bar.get_y() + bar.get_height()/2, str(val), va='center')

    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "kaiwai_analysis.png", dpi=150, bbox_inches='tight')
    plt.close()
    print(f"グラフ保存: {RESULTS_DIR / 'kaiwai_analysis.png'}")


def save_results(df, kaiwai_counts, airline_counts, basic_stats_dict):
    """結果をファイルに保存"""
    # クラスター分類結果（CSV）
    # 各投稿の界隈をカンマ区切りで保存
    df_export = df.copy()
    df_export["kaiwai_str"] = df_export["kaiwai"].apply(lambda x: ", ".join(x))
    df_export[["content", "kaiwai_str"]].to_csv(
        RESULTS_DIR / "clusters.csv", index=False, encoding="utf-8-sig"
    )
    print(f"クラスター結果保存: {RESULTS_DIR / 'clusters.csv'}")

    # サマリーレポート（Markdown）
    summary = f"""# 北米ビジネスクラスX発話 界隈分析レポート

## 基本統計

| 項目 | 値 |
|------|-----|
| 総投稿数 | {basic_stats_dict['総投稿数']:,} 件 |
| 平均文字数 | {basic_stats_dict['平均文字数']:.1f} 文字 |
| 最大文字数 | {basic_stats_dict['最大文字数']:,} 文字 |
| 最小文字数 | {basic_stats_dict['最小文字数']:,} 文字 |

---

## 航空会社別言及数

| 順位 | 航空会社 | 言及数 |
|------|----------|--------|
"""
    for i, (airline, count) in enumerate(airline_counts.items(), 1):
        if count > 0:
            summary += f"| {i} | {airline} | {count} |\n"

    summary += f"""
---

## 界隈別分析

### 界隈別投稿数

| 界隈 | 投稿数 | 説明 |
|------|--------|------|
"""
    kaiwai_sorted = dict(sorted(kaiwai_counts.items(), key=lambda x: x[1], reverse=True))
    for kaiwai, count in kaiwai_sorted.items():
        desc = KAIWAI_DEFINITIONS.get(kaiwai, {}).get("description", "-")
        summary += f"| {kaiwai} | {count} | {desc} |\n"

    summary += f"""
---

## 各界隈の代表的な投稿

"""
    for kaiwai_name in kaiwai_sorted.keys():
        if kaiwai_name == "未分類":
            continue
        summary += f"### {kaiwai_name}\n\n"
        posts = get_representative_posts(df, kaiwai_name, n=3)
        for i, post in enumerate(posts, 1):
            # 改行をスペースに置換し、Markdown記法をエスケープ
            clean_post = post.replace("\n", " ").replace("|", "\\|")
            summary += f"{i}. {clean_post}\n\n"

    summary += f"""
---

## 分析手法

- **手法**: キーワードベース分類
- **分類ルール**: 各界隈に定義されたキーワード・正規表現パターンにマッチする投稿を該当界隈に分類
- **複数該当**: 1つの投稿が複数の界隈に該当する場合あり
- **未分類**: どの界隈にも該当しなかった投稿

---

## 可視化

![界隈分析グラフ](kaiwai_analysis.png)

"""

    with open(RESULTS_DIR / "summary.md", "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"サマリー保存: {RESULTS_DIR / 'summary.md'}")

    # 統合レポート生成
    generate_integrated_report(df, kaiwai_counts, airline_counts, basic_stats_dict)


def generate_integrated_report(df, kaiwai_counts, airline_counts, basic_stats_dict):
    """統合レポートを生成（画像はBase64埋め込み、CSVはサマリーのみ）"""
    # 画像をBase64エンコード
    image_path = RESULTS_DIR / "kaiwai_analysis.png"
    image_base64 = ""
    if image_path.exists():
        with open(image_path, "rb") as img_file:
            image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    # 追加分析を実行
    cross_data = analyze_airline_kaiwai_cross(df)
    viral_topics = detect_viral_topics(df)
    executive_findings = generate_executive_summary(df, kaiwai_counts, airline_counts, cross_data)
    recommendations = generate_recommendations(df, kaiwai_counts, airline_counts, cross_data, viral_topics)

    # CSVサマリー統計を計算
    kaiwai_sorted = dict(sorted(kaiwai_counts.items(), key=lambda x: x[1], reverse=True))
    total_classified = sum(count for k, count in kaiwai_counts.items() if k != "未分類")
    unclassified = kaiwai_counts.get("未分類", 0)

    report = f"""# 北米ビジネスクラスX発話 界隈分析レポート（統合版）

> このレポートはすべての分析結果を単一ファイルにまとめた統合版です。

---

## エグゼクティブサマリー

### 主要な発見事項

"""
    for i, finding in enumerate(executive_findings, 1):
        report += f"{i}. {finding}\n"

    report += f"""

### キーインサイト

| 指標 | 値 | 示唆 |
|------|-----|------|
| 総投稿数 | {basic_stats_dict['総投稿数']:,} 件 | 分析対象のデータ量 |
| 分類成功率 | {((len(df) - unclassified) / len(df) * 100):.1f}% | 界隈分類の精度 |
| 主要航空会社数 | {len([a for a, c in airline_counts.items() if c > 0])} 社 | 言及された航空会社数 |
| 活発な界隈数 | {len([k for k, v in kaiwai_counts.items() if v > 10 and k != "未分類"])} | 投稿10件以上の界隈 |

---

## 基本統計

| 項目 | 値 |
|------|-----|
| 総投稿数 | {basic_stats_dict['総投稿数']:,} 件 |
| 平均文字数 | {basic_stats_dict['平均文字数']:.1f} 文字 |
| 最大文字数 | {basic_stats_dict['最大文字数']:,} 文字 |
| 最小文字数 | {basic_stats_dict['最小文字数']:,} 文字 |

---

## 航空会社×界隈クロス分析

### ヒートマップ

どの航空会社がどの界隈で多く言及されているかを示します。

| 航空会社 |"""

    # ヒートマップのヘッダー
    kaiwai_list = [k for k in KAIWAI_DEFINITIONS.keys()]
    for k in kaiwai_list:
        short_name = k.replace("界隈", "")
        report += f" {short_name} |"
    report += "\n|------|"
    for _ in kaiwai_list:
        report += "---:|"
    report += "\n"

    # ヒートマップのデータ行（言及がある航空会社のみ）
    for airline in list(airline_counts.keys())[:10]:  # 上位10社
        if airline_counts[airline] == 0:
            continue
        report += f"| {airline} |"
        for kaiwai in kaiwai_list:
            count = cross_data.get(airline, {}).get(kaiwai, 0)
            if count > 0:
                report += f" **{count}** |"
            else:
                report += " - |"
        report += "\n"

    report += f"""

### クロス分析インサイト

"""
    # 各航空会社の最も多い界隈を特定
    for airline in list(airline_counts.keys())[:5]:
        if airline_counts[airline] == 0:
            continue
        airline_kaiwai = [(k, v) for k, v in cross_data.get(airline, {}).items() if v > 0 and k != "未分類"]
        if airline_kaiwai:
            airline_kaiwai.sort(key=lambda x: x[1], reverse=True)
            top = airline_kaiwai[0]
            report += f"- **{airline}**: {top[0]}での言及が最多（{top[1]}件）\n"

    report += f"""

---

## 航空会社別言及数

| 順位 | 航空会社 | 言及数 |
|------|----------|--------|
"""
    for i, (airline, count) in enumerate(airline_counts.items(), 1):
        if count > 0:
            report += f"| {i} | {airline} | {count} |\n"

    report += f"""
---

## 界隈別分析

### 界隈別投稿数

| 界隈 | 投稿数 | 説明 |
|------|--------|------|
"""
    for kaiwai, count in kaiwai_sorted.items():
        desc = KAIWAI_DEFINITIONS.get(kaiwai, {}).get("description", "-")
        report += f"| {kaiwai} | {count} | {desc} |\n"

    report += f"""

---

## 界隈別ビジネスインサイト

"""
    for kaiwai_name, count in kaiwai_sorted.items():
        if kaiwai_name == "未分類" or count == 0:
            continue
        insight = KAIWAI_INSIGHTS.get(kaiwai_name, {})
        if not insight:
            continue

        report += f"""### {kaiwai_name}（{count}件）

| 観点 | 内容 |
|------|------|
| **意味するもの** | {insight.get('meaning', '-')} |
| **リスク/機会** | リスク: {insight.get('risk', '-')} / 機会: {insight.get('opportunity', '-')} |
| **推奨アクション** | {insight.get('action', '-')} |

"""

    report += f"""
---

## 注目トピック分析

"""
    if viral_topics:
        report += """### バイラル・炎上リスクトピック

| トピック | 件数 | タイプ | リスク | 説明 |
|----------|------|--------|--------|------|
"""
        for topic in viral_topics:
            report += f"| {topic['topic']} | {topic['count']} | {topic['type']} | {topic['risk_level']} | {topic['description']} |\n"

        report += "\n### トピック別サンプル投稿\n\n"
        for topic in viral_topics:
            report += f"#### {topic['topic']}\n\n"
            for i, post in enumerate(topic.get('sample_posts', []), 1):
                clean_post = post.replace("\n", " ").replace("|", "\\|")
                report += f"{i}. {clean_post}\n\n"
    else:
        report += "> 特筆すべきバイラルトピックは検出されませんでした。\n\n"

    report += f"""
---

## 総合提言

### 航空会社向け推奨事項

"""
    for i, rec in enumerate(recommendations["航空会社向け"], 1):
        report += f"{i}. {rec}\n\n"

    report += f"""
### SNS戦略への示唆

"""
    for i, rec in enumerate(recommendations["SNS戦略"], 1):
        report += f"{i}. {rec}\n\n"

    report += f"""
---

## 各界隈の代表的な投稿

"""
    for kaiwai_name in kaiwai_sorted.keys():
        if kaiwai_name == "未分類":
            continue
        report += f"### {kaiwai_name}\n\n"
        posts = get_representative_posts(df, kaiwai_name, n=3)
        for i, post in enumerate(posts, 1):
            clean_post = post.replace("\n", " ").replace("|", "\\|")
            report += f"{i}. {clean_post}\n\n"

    report += f"""
---

## 分析手法

- **手法**: キーワードベース分類
- **分類ルール**: 各界隈に定義されたキーワード・正規表現パターンにマッチする投稿を該当界隈に分類
- **複数該当**: 1つの投稿が複数の界隈に該当する場合あり
- **未分類**: どの界隈にも該当しなかった投稿

---

## 可視化

"""
    if image_base64:
        report += f"![界隈分析グラフ](data:image/png;base64,{image_base64})\n\n"
    else:
        report += "![界隈分析グラフ](kaiwai_analysis.png)\n\n"

    report += f"""
---

## クラスター分類結果サマリー

### 統計情報

| 項目 | 値 |
|------|-----|
| 総レコード数 | {len(df):,} 件 |
| 分類済み（1つ以上の界隈に属する） | {total_classified:,} 件 |
| 未分類 | {unclassified:,} 件 |
| 界隈数（未分類除く） | {len([k for k in kaiwai_counts.keys() if k != "未分類"])} |

### 界隈別分布

"""
    for kaiwai, count in kaiwai_sorted.items():
        percentage = (count / len(df)) * 100
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        report += f"- **{kaiwai}**: {count:,} 件 ({percentage:.1f}%) {bar}\n"

    report += f"""
---

## 付録: データファイル

分析に使用したデータファイル一覧:

| ファイル | 説明 | サイズ |
|----------|------|--------|
| `clusters.csv` | 全投稿の界隈分類結果 | {len(df):,} 件 |
| `kaiwai_analysis.png` | 可視化グラフ | （本レポートに埋め込み済み） |
| `summary.md` | 分析サマリー | （本レポートに統合済み） |

> **注**: `clusters.csv`の詳細データが必要な場合は、同ディレクトリ内のファイルを参照してください。

---

*このレポートは `analysis.py` により自動生成されました。*
"""

    with open(RESULTS_DIR / "report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"統合レポート保存: {RESULTS_DIR / 'report.md'}")


def main():
    print("=" * 50)
    print("北米ビジネスクラスX発話 界隈分析")
    print("=" * 50)

    # データ読み込み
    df = load_data()

    # 基本統計
    print("\n--- 基本統計 ---")
    stats = basic_stats(df)
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.1f}")
        else:
            print(f"{key}: {value:,}")

    # 航空会社別言及数
    print("\n--- 航空会社別言及数 ---")
    airline_counts = count_airlines(df)
    for airline, count in list(airline_counts.items())[:5]:
        print(f"{airline}: {count}")

    # 界隈分析
    print("\n--- 界隈分析 ---")
    df, kaiwai_counts = analyze_kaiwai(df)
    kaiwai_sorted = dict(sorted(kaiwai_counts.items(), key=lambda x: x[1], reverse=True))
    for kaiwai, count in kaiwai_sorted.items():
        print(f"{kaiwai}: {count}")

    # 可視化
    print("\n--- 可視化 ---")
    create_visualizations(kaiwai_counts, airline_counts)

    # 結果保存
    print("\n--- 結果保存 ---")
    save_results(df, kaiwai_counts, airline_counts, stats)

    print("\n" + "=" * 50)
    print("分析完了!")
    print("=" * 50)


def export_to_json(output_path=None):
    """分析結果をJSON形式でエクスポート（Webアプリ用）"""
    print("\n--- JSON出力 ---")

    # データ読み込みと分析実行
    df = load_data()
    stats = basic_stats(df)
    airline_counts = count_airlines(df)
    df, kaiwai_counts = analyze_kaiwai(df)
    cross_data = analyze_airline_kaiwai_cross(df)
    viral_topics = detect_viral_topics(df)
    executive_findings = generate_executive_summary(df, kaiwai_counts, airline_counts, cross_data)
    recommendations = generate_recommendations(df, kaiwai_counts, airline_counts, cross_data, viral_topics)

    # 代表投稿を収集
    representative_posts = {}
    for kaiwai_name in kaiwai_counts.keys():
        if kaiwai_name != "未分類":
            posts = get_representative_posts(df, kaiwai_name, n=5)
            representative_posts[kaiwai_name] = posts

    # 界隈インサイトを整形
    kaiwai_insights_data = {}
    for kaiwai_name, count in kaiwai_counts.items():
        if kaiwai_name in KAIWAI_INSIGHTS:
            kaiwai_insights_data[kaiwai_name] = {
                "count": count,
                "description": KAIWAI_DEFINITIONS.get(kaiwai_name, {}).get("description", ""),
                **KAIWAI_INSIGHTS[kaiwai_name]
            }

    # JSON構造を作成
    export_data = {
        "meta": {
            "title": "北米ビジネスクラスX発話 界隈分析",
            "generated_at": pd.Timestamp.now().isoformat(),
            "data_source": str(DATA_FILE.name)
        },
        "basic_stats": {
            "total_posts": stats["総投稿数"],
            "avg_length": round(stats["平均文字数"], 1),
            "max_length": stats["最大文字数"],
            "min_length": stats["最小文字数"]
        },
        "airline_counts": [
            {"name": airline, "count": count}
            for airline, count in airline_counts.items()
            if count > 0
        ],
        "kaiwai_counts": [
            {"name": kaiwai, "count": count, "description": KAIWAI_DEFINITIONS.get(kaiwai, {}).get("description", "")}
            for kaiwai, count in sorted(kaiwai_counts.items(), key=lambda x: x[1], reverse=True)
        ],
        "cross_data": {
            airline: {
                kaiwai: count
                for kaiwai, count in data.items()
                if count > 0
            }
            for airline, data in cross_data.items()
            if any(v > 0 for v in data.values())
        },
        "viral_topics": viral_topics,
        "executive_findings": executive_findings,
        "recommendations": recommendations,
        "kaiwai_insights": kaiwai_insights_data,
        "representative_posts": representative_posts
    }

    # 出力先を決定
    if output_path is None:
        output_path = RESULTS_DIR / "analysis.json"
    else:
        output_path = Path(output_path)

    # NumPy型をPython標準型に変換するカスタムエンコーダー
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            import numpy as np
            if isinstance(obj, (np.integer,)):
                return int(obj)
            if isinstance(obj, (np.floating,)):
                return float(obj)
            if isinstance(obj, (np.ndarray,)):
                return obj.tolist()
            return super().default(obj)

    # JSON出力
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2, cls=NumpyEncoder)

    print(f"JSON保存: {output_path}")
    return export_data


if __name__ == "__main__":
    main()
    # Webアプリ用JSONも出力
    export_to_json()
