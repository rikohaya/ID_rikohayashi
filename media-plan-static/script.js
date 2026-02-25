// ========================================
// データ定義（サーバー不要・静的版）
// ========================================

// 日本人口データ（年齢層別）
const POPULATION_DATA = {
    "10代": 11000000,
    "20代": 12500000,
    "30代": 13800000,
    "40代": 17500000,
    "50代": 16800000,
    "60代以上": 44000000,
};

// 性別比率
const GENDER_RATIO = {
    "男性": 0.49,
    "女性": 0.51,
    "全体": 1.0,
};

// 媒体利用率（年齢層 × 性別 → 媒体利用率）
const MEDIA_USAGE_RATE = {
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
};

// デフォルトCPM（円）
const DEFAULT_CPM = {
    "X": 400,
    "Instagram": 500,
    "TikTok": 600,
    "YouTube": 700,
    "LINE": 350,
    "Facebook": 450,
};

// ========================================
// 計算ロジック
// ========================================

function getTargetPopulation(ageGroup, gender, media) {
    const basePopulation = POPULATION_DATA[ageGroup] || 0;
    const genderRatio = GENDER_RATIO[gender] || 1.0;
    const mediaUsage = MEDIA_USAGE_RATE[media]?.[ageGroup]?.[gender] || 0;
    return Math.floor(basePopulation * genderRatio * mediaUsage);
}

function calculateNormal(ageGroup, gender, media, reachRate, frequency, cpm) {
    if (!cpm) cpm = DEFAULT_CPM[media] || 400;

    const targetPopulation = getTargetPopulation(ageGroup, gender, media);
    const reachCount = Math.floor(targetPopulation * (reachRate / 100));
    const totalImpressions = reachCount * frequency;
    const estimatedCost = Math.floor(totalImpressions / 1000 * cpm);

    return {
        target_population: targetPopulation,
        reach_count: reachCount,
        total_impressions: totalImpressions,
        estimated_cost: estimatedCost,
        cpm_used: cpm,
    };
}

function calculateReverse(ageGroup, gender, media, budget, frequency, cpm) {
    if (!cpm) cpm = DEFAULT_CPM[media] || 400;

    const targetPopulation = getTargetPopulation(ageGroup, gender, media);
    const maxImpressions = Math.floor(budget / cpm * 1000);
    const maxReach = Math.floor(maxImpressions / frequency);
    const reachRateAchievable = targetPopulation > 0
        ? Math.round((maxReach / targetPopulation * 100) * 100) / 100
        : 0;

    return {
        target_population: targetPopulation,
        max_reach: maxReach,
        max_impressions: maxImpressions,
        reach_rate_achievable: reachRateAchievable,
        cpm_used: cpm,
    };
}

// ========================================
// UI ロジック
// ========================================

let currentMode = 'normal';

// DOM Elements
const normalModeBtn = document.getElementById('normalMode');
const reverseModeBtn = document.getElementById('reverseMode');
const calculatorForm = document.getElementById('calculatorForm');
const resultsSection = document.getElementById('results');

const ageGroupSelect = document.getElementById('ageGroup');
const genderSelect = document.getElementById('gender');
const mediaSelect = document.getElementById('media');
const reachRateInput = document.getElementById('reachRate');
const frequencyInput = document.getElementById('frequency');
const cpmInput = document.getElementById('cpm');
const budgetInput = document.getElementById('budget');

// 初期化
function init() {
    loadOptions();
    setupEventListeners();
}

// オプション読み込み（静的データから）
function loadOptions() {
    populateSelect(ageGroupSelect, Object.keys(POPULATION_DATA));
    populateSelect(genderSelect, Object.keys(GENDER_RATIO));
    populateSelect(mediaSelect, Object.keys(MEDIA_USAGE_RATE));

    // 媒体選択時にデフォルトCPMを設定
    mediaSelect.addEventListener('change', () => {
        const selectedMedia = mediaSelect.value;
        if (selectedMedia && DEFAULT_CPM[selectedMedia]) {
            cpmInput.placeholder = DEFAULT_CPM[selectedMedia] + '円（デフォルト）';
        }
    });
}

// セレクトボックスにオプションを追加
function populateSelect(select, items) {
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        select.appendChild(option);
    });
}

// イベントリスナー設定
function setupEventListeners() {
    normalModeBtn.addEventListener('click', () => setMode('normal'));
    reverseModeBtn.addEventListener('click', () => setMode('reverse'));
    calculatorForm.addEventListener('submit', handleSubmit);
}

// モード切替
function setMode(mode) {
    currentMode = mode;

    // ボタンのアクティブ状態
    normalModeBtn.classList.toggle('active', mode === 'normal');
    reverseModeBtn.classList.toggle('active', mode === 'reverse');

    // フィールドの表示切替
    document.querySelectorAll('.normal-only').forEach(el => {
        el.style.display = mode === 'normal' ? 'block' : 'none';
    });
    document.querySelectorAll('.reverse-only').forEach(el => {
        el.style.display = mode === 'reverse' ? 'block' : 'none';
    });

    // 結果カードの表示切替
    document.querySelectorAll('.normal-result').forEach(el => {
        el.style.display = mode === 'normal' ? 'flex' : 'none';
    });
    document.querySelectorAll('.reverse-result').forEach(el => {
        el.style.display = mode === 'reverse' ? 'flex' : 'none';
    });

    // 結果をリセット
    resultsSection.style.display = 'none';
}

// フォーム送信
function handleSubmit(e) {
    e.preventDefault();

    const ageGroup = ageGroupSelect.value;
    const gender = genderSelect.value;
    const media = mediaSelect.value;
    const frequency = parseInt(frequencyInput.value);
    const cpm = cpmInput.value ? parseFloat(cpmInput.value) : null;

    let result;

    if (currentMode === 'normal') {
        const reachRate = parseFloat(reachRateInput.value);
        result = calculateNormal(ageGroup, gender, media, reachRate, frequency, cpm);
    } else {
        const budget = parseInt(budgetInput.value);
        if (!budget) {
            alert('予算を入力してください');
            return;
        }
        result = calculateReverse(ageGroup, gender, media, budget, frequency, cpm);
    }

    displayResults(result);
}

// 結果表示
function displayResults(result) {
    resultsSection.style.display = 'block';

    document.getElementById('targetPopulation').textContent = formatNumber(result.target_population);
    document.getElementById('cpmUsed').textContent = formatNumber(result.cpm_used);

    if (currentMode === 'normal') {
        document.getElementById('reachCount').textContent = formatNumber(result.reach_count);
        document.getElementById('totalImpressions').textContent = formatNumber(result.total_impressions);
        document.getElementById('estimatedCost').textContent = formatNumber(result.estimated_cost);
    } else {
        document.getElementById('maxReach').textContent = formatNumber(result.max_reach);
        document.getElementById('totalImpressions').textContent = formatNumber(result.max_impressions);
        document.getElementById('reachRateAchievable').textContent = result.reach_rate_achievable.toFixed(1);
    }

    // スムーズスクロール
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// 数値フォーマット
function formatNumber(num) {
    return num.toLocaleString('ja-JP');
}

// 初期化実行
init();
