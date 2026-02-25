const API_BASE = '/api/media-plan';

let currentMode = 'normal';
let options = null;

// DOM Elements
const normalModeBtn = document.getElementById('normalMode');
const reverseModeBtn = document.getElementById('reverseMode');
const adCostModeBtn = document.getElementById('adCostMode');
const calculatorForm = document.getElementById('calculatorForm');
const resultsSection = document.getElementById('results');
const adCostResultsSection = document.getElementById('adCostResults');

const targetDescriptionInput = document.getElementById('targetDescription');
const targetPopulationInput = document.getElementById('targetPopulation');
const mediaSelect = document.getElementById('media');
const mediaAdCostSelect = document.getElementById('mediaAdCost');
const reachRateInput = document.getElementById('reachRate');
const frequencyInput = document.getElementById('frequency');
const cpmInput = document.getElementById('cpm');
const budgetInput = document.getElementById('budget');

const estimateBtn = document.getElementById('estimateBtn');
const estimateResult = document.getElementById('estimateResult');
const estimateAdCostBtn = document.getElementById('estimateAdCostBtn');

// 初期化
async function init() {
    await loadOptions();
    setupEventListeners();
}

// オプション読み込み
async function loadOptions() {
    try {
        const response = await fetch(`${API_BASE}/options`);
        options = await response.json();

        populateSelect(mediaSelect, options.media_types);
        options.media_types.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m;
            opt.textContent = m;
            mediaAdCostSelect.appendChild(opt);
        });

        // 媒体選択時にデフォルトCPMを設定
        mediaSelect.addEventListener('change', () => {
            const selectedMedia = mediaSelect.value;
            if (selectedMedia && options.default_cpm[selectedMedia]) {
                cpmInput.placeholder = options.default_cpm[selectedMedia] + '円（デフォルト）';
            }
        });
    } catch (error) {
        console.error('Failed to load options:', error);
        alert('オプションの読み込みに失敗しました');
    }
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
    adCostModeBtn.addEventListener('click', () => setMode('adcost'));
    calculatorForm.addEventListener('submit', handleSubmit);
    estimateBtn.addEventListener('click', handleEstimate);
    estimateAdCostBtn.addEventListener('click', handleEstimateAdCost);
}

// モード切替
function setMode(mode) {
    currentMode = mode;

    // ボタンのアクティブ状態
    normalModeBtn.classList.toggle('active', mode === 'normal');
    reverseModeBtn.classList.toggle('active', mode === 'reverse');
    adCostModeBtn.classList.toggle('active', mode === 'adcost');

    // フィールドの表示切替
    document.querySelectorAll('.normal-only').forEach(el => {
        el.style.display = mode === 'normal' ? 'block' : 'none';
    });
    document.querySelectorAll('.reverse-only').forEach(el => {
        el.style.display = mode === 'reverse' ? 'block' : 'none';
    });
    document.querySelectorAll('.form-group-normal-reverse').forEach(el => {
        el.style.display = (mode === 'normal' || mode === 'reverse') ? 'block' : 'none';
    });
    document.querySelectorAll('.form-group-adcost').forEach(el => {
        el.style.display = mode === 'adcost' ? 'block' : 'none';
    });
    // リーチ率は「通常」と「広告費見積」の両方で表示
    document.querySelectorAll('.adcost-only').forEach(el => {
        el.style.display = (mode === 'normal' || mode === 'adcost') ? 'block' : 'none';
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
    adCostResultsSection.style.display = 'none';
}

// AI推定
async function handleEstimate() {
    const targetDescription = targetDescriptionInput.value.trim();
    const media = mediaSelect.value;

    if (!targetDescription) {
        alert('ターゲットを入力してください');
        return;
    }

    if (!media) {
        alert('媒体を選択してください');
        return;
    }

    estimateBtn.disabled = true;
    estimateBtn.textContent = '推定中...';

    try {
        const response = await fetch(`${API_BASE}/estimate-target`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                target_description: targetDescription,
                media: media,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'AI推定に失敗しました');
        }

        const result = await response.json();

        // 推定人口を入力欄に設定
        targetPopulationInput.value = result.estimated_population;

        // 推定結果を表示
        estimateResult.style.display = 'block';
        estimateResult.querySelector('.estimate-reasoning').textContent = result.reasoning;

        const confidenceEl = estimateResult.querySelector('.estimate-confidence');
        confidenceEl.textContent = `信頼度: ${getConfidenceLabel(result.confidence)}`;
        confidenceEl.className = `estimate-confidence ${result.confidence}`;

    } catch (error) {
        console.error('Estimate error:', error);
        alert(error.message);
    } finally {
        estimateBtn.disabled = false;
        estimateBtn.textContent = 'AI推定';
    }
}

function getConfidenceLabel(confidence) {
    switch (confidence) {
        case 'high': return '高';
        case 'medium': return '中';
        case 'low': return '低';
        default: return confidence;
    }
}

// 広告費見積（ターゲット → かかる費用）
async function handleEstimateAdCost() {
    const targetDescription = targetDescriptionInput.value.trim();
    if (!targetDescription) {
        alert('ターゲットを入力してください');
        return;
    }

    const media = mediaAdCostSelect.value || null;
    const reachRate = parseFloat(reachRateInput.value) || 50;
    const frequency = parseInt(frequencyInput.value) || 2;

    estimateAdCostBtn.disabled = true;
    estimateAdCostBtn.textContent = '見積中...';

    try {
        const response = await fetch(`${API_BASE}/estimate-ad-cost`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                target_description: targetDescription,
                media: media,
                reach_rate: reachRate,
                frequency: frequency,
            }),
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || '見積に失敗しました');
        }

        const result = await response.json();

        document.getElementById('adCostSummary').textContent = result.summary_message;
        document.getElementById('adCostReasoning').textContent = result.reasoning;

        const tbody = document.querySelector('#adCostTable tbody');
        tbody.innerHTML = '';
        result.per_media.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.media}</td>
                <td>${formatNumber(p.estimated_cost)}</td>
                <td>${formatNumber(p.reach_count)}</td>
                <td>${formatNumber(p.total_impressions)}</td>
            `;
            tbody.appendChild(tr);
        });

        adCostResultsSection.style.display = 'block';
        adCostResultsSection.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        console.error('Estimate ad cost error:', error);
        alert(error.message);
    } finally {
        estimateAdCostBtn.disabled = false;
        estimateAdCostBtn.textContent = '広告費を見積る';
    }
}

// フォーム送信
async function handleSubmit(e) {
    e.preventDefault();
    if (currentMode === 'adcost') return;

    const endpoint = currentMode === 'normal' ? 'custom-calculate' : 'custom-reverse';
    const payload = buildPayload();

    try {
        const response = await fetch(`${API_BASE}/${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '計算に失敗しました');
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error('Calculation error:', error);
        alert(error.message);
    }
}

// ペイロード構築
function buildPayload() {
    const base = {
        target_description: targetDescriptionInput.value,
        target_population: parseInt(targetPopulationInput.value),
        media: mediaSelect.value,
        frequency: parseInt(frequencyInput.value),
    };

    if (cpmInput.value) {
        base.cpm = parseFloat(cpmInput.value);
    }

    if (currentMode === 'normal') {
        base.reach_rate = parseFloat(reachRateInput.value);
    } else {
        base.budget = parseInt(budgetInput.value);
    }

    return base;
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
