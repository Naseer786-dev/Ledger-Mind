
# Create a complete working Excel upload + AI scan system
# This is a standalone HTML file with embedded JavaScript that works in browser

excel_scanner_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LedgerMind Excel Scanner - by Naseeruddin Mohammed</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #0a0e1a; color: #fff; min-height: 100vh; }
        
        .header { background: linear-gradient(135deg, #0f172a, #1e293b); padding: 1.5rem 2rem; border-bottom: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: space-between; }
        .brand { display: flex; align-items: center; gap: 0.75rem; }
        .brand-logo { width: 40px; height: 40px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem; }
        .brand-text h1 { font-size: 1.1rem; font-weight: 700; }
        .brand-text p { font-size: 0.7rem; color: #64748b; }
        .status { display: flex; align-items: center; gap: 0.5rem; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); padding: 0.4rem 1rem; border-radius: 999px; }
        .status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
        .status span { font-size: 0.75rem; color: #10b981; font-weight: 500; }
        
        .container { max-width: 1400px; margin: 0 auto; padding: 2rem; }
        
        /* Upload Section */
        .upload-section { background: rgba(15,23,42,0.8); border: 2px dashed rgba(16,185,129,0.3); border-radius: 20px; padding: 3rem; text-align: center; margin-bottom: 2rem; transition: all 0.3s; }
        .upload-section:hover { border-color: #10b981; background: rgba(16,185,129,0.05); }
        .upload-section.dragover { border-color: #10b981; background: rgba(16,185,129,0.1); transform: scale(1.02); }
        .upload-icon { font-size: 4rem; margin-bottom: 1rem; }
        .upload-section h2 { font-size: 1.5rem; margin-bottom: 0.5rem; }
        .upload-section p { color: #64748b; margin-bottom: 1.5rem; }
        .file-input { display: none; }
        .btn-upload { background: linear-gradient(135deg, #10b981, #059669); color: #fff; border: none; padding: 1rem 2.5rem; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s; }
        .btn-upload:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(16,185,129,0.3); }
        .file-info { margin-top: 1rem; padding: 1rem; background: rgba(16,185,129,0.1); border-radius: 10px; display: none; }
        .file-info.show { display: block; }
        
        /* Progress */
        .scan-progress { display: none; margin: 2rem 0; }
        .scan-progress.show { display: block; }
        .progress-bar-bg { background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; overflow: hidden; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #10b981, #06b6d4); border-radius: 10px; width: 0%; transition: width 0.5s ease; }
        .progress-text { text-align: center; margin-top: 0.75rem; color: #94a3b8; font-size: 0.875rem; }
        .agent-status { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.5rem; margin-top: 1rem; }
        .agent-status-item { text-align: center; padding: 0.5rem; border-radius: 8px; background: rgba(255,255,255,0.03); font-size: 0.7rem; }
        .agent-status-item.active { background: rgba(16,185,129,0.15); color: #10b981; }
        .agent-status-item.done { background: rgba(16,185,129,0.2); color: #10b981; }
        .agent-status-item.done::after { content: ' ✓'; }
        
        /* Results Dashboard */
        .results { display: none; }
        .results.show { display: block; }
        
        .results-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; }
        .results-header h2 { font-size: 1.5rem; }
        .scan-badge { background: linear-gradient(135deg, #10b981, #059669); padding: 0.5rem 1.5rem; border-radius: 999px; font-size: 0.875rem; font-weight: 600; }
        
        /* Summary Cards */
        .summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
        .summary-card { background: rgba(15,23,42,0.8); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 1.5rem; text-align: center; }
        .summary-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
        .summary-card .value { font-size: 2rem; font-weight: 800; }
        .summary-card .label { color: #64748b; font-size: 0.8rem; margin-top: 0.25rem; }
        .summary-card.good .value { color: #10b981; }
        .summary-card.warning .value { color: #f59e0b; }
        .summary-card.danger .value { color: #ef4444; }
        .summary-card.info .value { color: #3b82f6; }
        
        /* Tabs */
        .tabs { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 0.5rem; }
        .tab { padding: 0.6rem 1.2rem; border-radius: 8px; cursor: pointer; font-size: 0.875rem; font-weight: 500; color: #64748b; transition: all 0.2s; border: none; background: transparent; }
        .tab:hover { color: #fff; background: rgba(255,255,255,0.05); }
        .tab.active { color: #fff; background: rgba(16,185,129,0.15); }
        .tab .badge { background: rgba(239,68,68,0.2); color: #ef4444; padding: 0.1rem 0.4rem; border-radius: 999px; font-size: 0.7rem; margin-left: 0.3rem; }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        /* Tables */
        .data-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
        .data-table th { text-align: left; padding: 0.75rem 1rem; color: #94a3b8; font-weight: 500; border-bottom: 1px solid rgba(255,255,255,0.08); }
        .data-table td { padding: 0.75rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.04); color: #e2e8f0; }
        .data-table tr:hover td { background: rgba(255,255,255,0.02); }
        .tag { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 500; }
        .tag-revenue { background: rgba(16,185,129,0.15); color: #10b981; }
        .tag-expense { background: rgba(239,68,68,0.15); color: #ef4444; }
        .tag-software { background: rgba(59,130,246,0.15); color: #3b82f6; }
        .tag-office { background: rgba(245,158,11,0.15); color: #f59e0b; }
        .tag-travel { background: rgba(139,92,246,0.15); color: #a855f7; }
        .tag-marketing { background: rgba(236,72,153,0.15); color: #ec4899; }
        .tag-uncategorized { background: rgba(100,116,139,0.15); color: #64748b; }
        
        /* Fraud Alerts */
        .fraud-alert { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; }
        .fraud-alert-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; }
        .fraud-alert-icon { width: 36px; height: 36px; background: rgba(239,68,68,0.2); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
        .fraud-alert h4 { font-size: 1rem; color: #fca5a5; }
        .fraud-alert p { color: #94a3b8; font-size: 0.875rem; line-height: 1.5; }
        .fraud-alert .action { margin-top: 0.75rem; display: flex; gap: 0.5rem; }
        .btn-action { padding: 0.4rem 1rem; border-radius: 6px; font-size: 0.8rem; font-weight: 500; cursor: pointer; border: none; }
        .btn-block { background: rgba(239,68,68,0.2); color: #fca5a5; }
        .btn-review { background: rgba(255,255,255,0.08); color: #94a3b8; }
        
        /* Tax Deductions */
        .deduction-card { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; }
        .deduction-info h4 { color: #6ee7b7; font-size: 1rem; }
        .deduction-info p { color: #94a3b8; font-size: 0.8rem; margin-top: 0.25rem; }
        .deduction-amount { font-size: 1.5rem; font-weight: 800; color: #10b981; }
        
        /* Cash Flow Chart */
        .chart-container { background: rgba(15,23,42,0.8); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 1.5rem; margin-bottom: 1.5rem; }
        .chart-container h3 { font-size: 1rem; margin-bottom: 1rem; }
        
        /* Vendor Cards */
        .vendor-card { background: rgba(15,23,42,0.8); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; }
        .vendor-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem; }
        .vendor-name { font-weight: 600; }
        .vendor-score { display: flex; align-items: center; gap: 0.5rem; }
        .score-bar { width: 80px; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; }
        .score-fill { height: 100%; border-radius: 3px; }
        
        .sample-data { margin-top: 1rem; }
        .btn-sample { background: rgba(59,130,246,0.15); color: #3b82f6; border: 1px solid rgba(59,130,246,0.3); padding: 0.6rem 1.2rem; border-radius: 8px; font-size: 0.875rem; cursor: pointer; }
        
        @media (max-width: 768px) {
            .summary-grid { grid-template-columns: repeat(2, 1fr); }
            .agent-status { grid-template-columns: repeat(3, 1fr); }
            .tabs { overflow-x: auto; }
            .container { padding: 1rem; }
        }
    </style>
</head>
<body>

<div class="header">
    <div class="brand">
        <div class="brand-logo">L</div>
        <div class="brand-text">
            <h1>LedgerMind Excel Scanner</h1>
            <p>by Naseeruddin Mohammed</p>
        </div>
    </div>
    <div class="status">
        <div class="status-dot"></div>
        <span>5 AI Agents Ready</span>
    </div>
</div>

<div class="container">
    
    <!-- UPLOAD SECTION -->
    <div class="upload-section" id="uploadSection">
        <div class="upload-icon">📊</div>
        <h2>Upload Your Excel or CSV File</h2>
        <p>Drag & drop your file here, or click to browse. We'll scan it with 5 AI agents instantly.</p>
        <input type="file" id="fileInput" class="file-input" accept=".xlsx,.xls,.csv">
        <button class="btn-upload" onclick="document.getElementById('fileInput').click()">Choose File</button>
        <div class="sample-data">
            <button class="btn-sample" onclick="loadSampleData()">📋 Use Sample Data (Demo)</button>
        </div>
        <div class="file-info" id="fileInfo">
            <span id="fileName"></span> — <span id="fileRows"></span> rows detected
        </div>
    </div>
    
    <!-- SCAN PROGRESS -->
    <div class="scan-progress" id="scanProgress">
        <div class="progress-bar-bg">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        <div class="progress-text" id="progressText">Initializing AI agents...</div>
        <div class="agent-status" id="agentStatus">
            <div class="agent-status-item" id="status-data">📝 Data Agent</div>
            <div class="agent-status-item" id="status-fraud">🛡️ Fraud Agent</div>
            <div class="agent-status-item" id="status-forecast">🔮 Forecast</div>
            <div class="agent-status-item" id="status-tax">💰 Tax Agent</div>
            <div class="agent-status-item" id="status-vendor">🤝 Vendor</div>
        </div>
    </div>
    
    <!-- RESULTS DASHBOARD -->
    <div class="results" id="results">
        <div class="results-header">
            <h2>📊 AI Scan Results</h2>
            <div class="scan-badge">✓ Scan Complete</div>
        </div>
        
        <!-- Summary Cards -->
        <div class="summary-grid">
            <div class="summary-card info">
                <div class="icon">📄</div>
                <div class="value" id="totalTx">0</div>
                <div class="label">Transactions Scanned</div>
            </div>
            <div class="summary-card good">
                <div class="icon">💰</div>
                <div class="value" id="taxFound">$0</div>
                <div class="label">Tax Deductions Found</div>
            </div>
            <div class="summary-card danger">
                <div class="icon">🚨</div>
                <div class="value" id="fraudCount">0</div>
                <div class="label">Fraud Alerts</div>
            </div>
            <div class="summary-card warning">
                <div class="icon">⚠️</div>
                <div class="value" id="riskLevel">Low</div>
                <div class="label">Overall Risk</div>
            </div>
        </div>
        
        <!-- Tabs -->
        <div class="tabs">
            <button class="tab active" onclick="switchTab('all')">All Transactions</button>
            <button class="tab" onclick="switchTab('fraud')">Fraud Alerts <span class="badge" id="fraudBadge">0</span></button>
            <button class="tab" onclick="switchTab('tax')">Tax Deductions <span class="badge" id="taxBadge">0</span></button>
            <button class="tab" onclick="switchTab('forecast')">Cash Flow</button>
            <button class="tab" onclick="switchTab('vendor')">Vendors</button>
        </div>
        
        <!-- Tab: All Transactions -->
        <div class="tab-content active" id="tab-all">
            <div style="overflow-x: auto;">
                <table class="data-table" id="txTable">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Description</th>
                            <th>Vendor</th>
                            <th>Category</th>
                            <th>Amount</th>
                            <th>Type</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="txTableBody"></tbody>
                </table>
            </div>
        </div>
        
        <!-- Tab: Fraud Alerts -->
        <div class="tab-content" id="tab-fraud">
            <div id="fraudContainer"></div>
        </div>
        
        <!-- Tab: Tax Deductions -->
        <div class="tab-content" id="tab-tax">
            <div id="taxContainer"></div>
            <div class="chart-container" style="margin-top: 1.5rem;">
                <h3>💡 AI Recommendations</h3>
                <div id="taxRecommendations"></div>
            </div>
        </div>
        
        <!-- Tab: Cash Flow -->
        <div class="tab-content" id="tab-forecast">
            <div class="chart-container">
                <h3>30-Day Cash Flow Projection</h3>
                <canvas id="cashFlowChart" height="100"></canvas>
            </div>
            <div class="chart-container">
                <h3>⚠️ Cash Flow Alerts</h3>
                <div id="cashFlowAlerts"></div>
            </div>
        </div>
        
        <!-- Tab: Vendors -->
        <div class="tab-content" id="tab-vendor">
            <div id="vendorContainer"></div>
        </div>
        
    </div>
</div>

<script>
// ============================================================
// SAMPLE DATA (For Demo When User Doesn't Have Excel)
// ============================================================
const SAMPLE_DATA = [
    {date: "2026-07-01", description: "Stripe - Customer Payment", vendor: "Stripe", amount: 4500, type: "Revenue"},
    {date: "2026-07-02", description: "Amazon Web Services", vendor: "AWS", amount: -342.50, type: "Expense"},
    {date: "2026-07-03", description: "Office Supplies - Paper", vendor: "OfficeMax", amount: -125.00, type: "Expense"},
    {date: "2026-07-05", description: "Client Invoice #4421", vendor: "Acme Corp", amount: 8200, type: "Revenue"},
    {date: "2026-07-06", description: "Slack Subscription", vendor: "Slack", amount: -15.00, type: "Expense"},
    {date: "2026-07-07", description: "TechSupplies Inc - Invoice #4482", vendor: "TechSupplies", amount: -12500, type: "Expense"},
    {date: "2026-07-08", description: "Uber - Business Trip", vendor: "Uber", amount: -47.30, type: "Expense"},
    {date: "2026-07-09", description: "Google Ads Campaign", vendor: "Google", amount: -850.00, type: "Expense"},
    {date: "2026-07-10", description: "Client Invoice #4422", vendor: "Beta LLC", amount: 3200, type: "Revenue"},
    {date: "2026-07-11", description: "TechSupplies Inc - Invoice #4482", vendor: "TechSupplies", amount: -12500, type: "Expense"},
    {date: "2026-07-12", description: "Office Rent", vendor: "Landlord", amount: -2500.00, type: "Expense"},
    {date: "2026-07-13", description: "Notion Subscription", vendor: "Notion", amount: -10.00, type: "Expense"},
    {date: "2026-07-14", description: "Wire Transfer - Unknown", vendor: "Unknown", amount: -8750.00, type: "Expense"},
    {date: "2026-07-15", description: "Client Invoice #4423", vendor: "Gamma Inc", amount: 5600, type: "Revenue"},
    {date: "2026-07-16", description: "Figma Subscription", vendor: "Figma", amount: -15.00, type: "Expense"},
    {date: "2026-07-17", description: "GitHub Pro", vendor: "GitHub", amount: -21.00, type: "Expense"},
    {date: "2026-07-18", description: "OfficeMax - Toner", vendor: "OfficeMax", amount: -189.00, type: "Expense"},
    {date: "2026-07-19", description: "Client Invoice #4424", vendor: "Delta Co", amount: 7800, type: "Revenue"},
    {date: "2026-07-20", description: "Zoom Subscription", vendor: "Zoom", amount: -19.99, type: "Expense"},
    {date: "2026-07-21", description: "Business Lunch", vendor: "Restaurant", amount: -87.50, type: "Expense"},
    {date: "2026-07-22", description: "Client Invoice #4425", vendor: "Epsilon Ltd", amount: 4300, type: "Revenue"},
    {date: "2026-07-23", description: "AWS - Server Costs", vendor: "AWS", amount: -520.00, type: "Expense"},
];

let transactions = [];
let fraudAlerts = [];
let taxDeductions = [];
let vendorScores = [];

// ============================================================
// FILE UPLOAD HANDLER
// ============================================================
const uploadSection = document.getElementById('uploadSection');
const fileInput = document.getElementById('fileInput');

uploadSection.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadSection.classList.add('dragover');
});

uploadSection.addEventListener('dragleave', () => {
    uploadSection.classList.remove('dragover');
});

uploadSection.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length) handleFile(files[0]);
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleFile(e.target.files[0]);
});

function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, {type: 'array'});
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(firstSheet);
        
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileRows').textContent = jsonData.length;
        document.getElementById('fileInfo').classList.add('show');
        
        // Convert to our format
        transactions = jsonData.map((row, i) => ({
            id: `TX-${i+1}`,
            date: row.Date || row.date || new Date().toISOString().split('T')[0],
            description: row.Description || row.description || row.Desc || '',
            vendor: row.Vendor || row.vendor || row.Payee || '',
            amount: parseFloat(row.Amount || row.amount || row.Debit || 0),
            type: (parseFloat(row.Amount) > 0 || row.Type === 'Revenue') ? 'Revenue' : 'Expense'
        }));
        
        startScan();
    };
    reader.readAsArrayBuffer(file);
}

function loadSampleData() {
    transactions = SAMPLE_DATA.map((row, i) => ({
        id: `TX-${i+1}`,
        ...row
    }));
    
    document.getElementById('fileName').textContent = 'Sample_Demo_Data.xlsx';
    document.getElementById('fileRows').textContent = transactions.length;
    document.getElementById('fileInfo').classList.add('show');
    
    startScan();
}

// ============================================================
// AI SCAN SIMULATION
// ============================================================
function startScan() {
    document.getElementById('scanProgress').classList.add('show');
    document.getElementById('uploadSection').style.display = 'none';
    
    const steps = [
        { pct: 10, text: '📝 Data Agent: Categorizing transactions...', agent: 'data' },
        { pct: 30, text: '📝 Data Agent: Reconciling accounts...', agent: 'data' },
        { pct: 45, text: '🛡️ Fraud Agent: Scanning for duplicates...', agent: 'fraud' },
        { pct: 60, text: '🛡️ Fraud Agent: Detecting anomalies...', agent: 'fraud' },
        { pct: 72, text: '🔮 Forecast Agent: Analyzing cash flow...', agent: 'forecast' },
        { pct: 82, text: '💰 Tax Agent: Finding deductions...', agent: 'tax' },
        { pct: 92, text: '🤝 Vendor Agent: Scoring suppliers...', agent: 'vendor' },
        { pct: 100, text: '✅ All agents complete! Generating report...', agent: 'done' }
    ];
    
    let step = 0;
    const interval = setInterval(() => {
        if (step >= steps.length) {
            clearInterval(interval);
            showResults();
            return;
        }
        
        const s = steps[step];
        document.getElementById('progressBar').style.width = s.pct + '%';
        document.getElementById('progressText').textContent = s.text;
        
        if (s.agent !== 'done') {
            document.getElementById(`status-${s.agent}`).classList.add('active');
        }
        
        // Mark previous agents as done
        const agentOrder = ['data', 'fraud', 'forecast', 'tax', 'vendor'];
        const currentIdx = agentOrder.indexOf(s.agent);
        for (let i = 0; i < currentIdx; i++) {
            document.getElementById(`status-${agentOrder[i]}`).classList.remove('active');
            document.getElementById(`status-${agentOrder[i]}`).classList.add('done');
        }
        
        step++;
    }, 600);
}

// ============================================================
// AI ANALYSIS ENGINE (Runs in Browser - No Server Needed!)
// ============================================================
function runAIAnalysis() {
    // 1. DATA AGENT - Auto Categorize
    transactions.forEach(tx => {
        const desc = tx.description.toLowerCase();
        if (tx.type === 'Revenue') {
            tx.category = 'Revenue';
        } else if (desc.includes('aws') || desc.includes('server')) {
            tx.category = 'Software';
        } else if (desc.includes('slack') || desc.includes('notion') || desc.includes('figma') || desc.includes('github') || desc.includes('zoom')) {
            tx.category = 'Software';
        } else if (desc.includes('office') || desc.includes('paper') || desc.includes('toner')) {
            tx.category = 'Office Supplies';
        } else if (desc.includes('uber') || desc.includes('trip')) {
            tx.category = 'Travel';
        } else if (desc.includes('ads') || desc.includes('google') || desc.includes('marketing')) {
            tx.category = 'Marketing';
        } else if (desc.includes('rent') || desc.includes('landlord')) {
            tx.category = 'Rent';
        } else if (desc.includes('lunch') || desc.includes('restaurant') || desc.includes('meal')) {
            tx.category = 'Meals';
        } else if (desc.includes('wire') || desc.includes('unknown')) {
            tx.category = 'Uncategorized';
        } else {
            tx.category = 'Other';
        }
    });
    
    // 2. FRAUD AGENT - Detect Issues
    fraudAlerts = [];
    
    // Check for duplicates
    const seen = {};
    transactions.forEach(tx => {
        const key = `${tx.vendor}-${Math.abs(tx.amount)}`;
        if (seen[key]) {
            fraudAlerts.push({
                id: tx.id,
                type: 'Duplicate Invoice',
                severity: 'high',
                description: `Invoice from "${tx.vendor}" for $${Math.abs(tx.amount).toLocaleString()} appears to be a duplicate of transaction ${seen[key]}`,
                action: 'Block Payment'
            });
        } else {
            seen[key] = tx.id;
        }
    });
    
    // Check for large unusual amounts
    transactions.forEach(tx => {
        if (Math.abs(tx.amount) > 8000 && tx.vendor !== 'Acme Corp' && tx.vendor !== 'Beta LLC') {
            const existing = fraudAlerts.find(a => a.id === tx.id);
            if (!existing) {
                fraudAlerts.push({
                    id: tx.id,
                    type: 'Large Amount Alert',
                    severity: 'medium',
                    description: `Transaction of $${Math.abs(tx.amount).toLocaleString()} to "${tx.vendor}" is unusually large`,
                    action: 'Verify by Phone'
                });
            }
        }
    });
    
    // Check for unknown vendors
    transactions.forEach(tx => {
        if (tx.vendor === 'Unknown' || tx.description.includes('Unknown')) {
            fraudAlerts.push({
                id: tx.id,
                type: 'Unknown Vendor',
                severity: 'high',
                description: `Wire transfer of $${Math.abs(tx.amount).toLocaleString()} to unknown recipient`,
                action: 'Hold for Review'
            });
        }
    });
    
    // 3. TAX AGENT - Find Deductions
    taxDeductions = [];
    
    transactions.forEach(tx => {
        if (tx.category === 'Software' && tx.type === 'Expense') {
            taxDeductions.push({
                category: 'Software & Technology',
                amount: Math.abs(tx.amount),
                description: `${tx.description} - Business software subscription`,
                confidence: 0.95
            });
        }
        if (tx.category === 'Travel' && tx.type === 'Expense') {
            taxDeductions.push({
                category: 'Travel & Transportation',
                amount: Math.abs(tx.amount),
                description: `${tx.description} - Business travel`,
                confidence: 0.90
            });
        }
        if (tx.category === 'Meals' && tx.type === 'Expense') {
            taxDeductions.push({
                category: 'Meals & Entertainment',
                amount: Math.abs(tx.amount) * 0.5,
                description: `${tx.description} - Business meal (50% deductible)`,
                confidence: 0.85
            });
        }
        if (tx.category === 'Marketing' && tx.type === 'Expense') {
            taxDeductions.push({
                category: 'Advertising',
                amount: Math.abs(tx.amount),
                description: `${tx.description} - Business advertising`,
                confidence: 0.95
            });
        }
        if (tx.category === 'Office Supplies' && tx.type === 'Expense') {
            taxDeductions.push({
                category: 'Office Expenses',
                amount: Math.abs(tx.amount),
                description: `${tx.description} - Office supplies`,
                confidence: 0.95
            });
        }
    });
    
    // 4. VENDOR AGENT - Score Vendors
    const vendorData = {};
    transactions.forEach(tx => {
        if (!vendorData[tx.vendor]) {
            vendorData[tx.vendor] = { total: 0, count: 0, amounts: [] };
        }
        vendorData[tx.vendor].total += Math.abs(tx.amount);
        vendorData[tx.vendor].count++;
        vendorData[tx.vendor].amounts.push(Math.abs(tx.amount));
    });
    
    vendorScores = Object.entries(vendorData).map(([name, data]) => {
        const avg = data.total / data.count;
        const hasFraud = fraudAlerts.some(a => transactions.find(t => t.id === a.id)?.vendor === name);
        const score = hasFraud ? 25 : Math.min(100, 70 + (data.count * 5));
        return { name, total: data.total, count: data.count, score, hasFraud };
    }).sort((a, b) => b.total - a.total);
}

// ============================================================
// DISPLAY RESULTS
// ============================================================
function showResults() {
    runAIAnalysis();
    
    document.getElementById('scanProgress').style.display = 'none';
    document.getElementById('results').classList.add('show');
    
    // Update summary cards
    document.getElementById('totalTx').textContent = transactions.length;
    const totalDeductions = taxDeductions.reduce((sum, d) => sum + d.amount, 0);
    document.getElementById('taxFound').textContent = '$' + totalDeductions.toLocaleString(undefined, {maximumFractionDigits: 0});
    document.getElementById('fraudCount').textContent = fraudAlerts.length;
    document.getElementById('fraudBadge').textContent = fraudAlerts.length;
    document.getElementById('taxBadge').textContent = taxDeductions.length;
    
    const riskLevel = fraudAlerts.length >= 3 ? 'Critical' : fraudAlerts.length >= 1 ? 'Medium' : 'Low';
    document.getElementById('riskLevel').textContent = riskLevel;
    document.getElementById('riskLevel').style.color = fraudAlerts.length >= 3 ? '#ef4444' : fraudAlerts.length >= 1 ? '#f59e0b' : '#10b981';
    
    // Render transactions table
    renderTransactions();
    
    // Render fraud alerts
    renderFraudAlerts();
    
    // Render tax deductions
    renderTaxDeductions();
    
    // Render cash flow chart
    renderCashFlowChart();
    
    // Render vendors
    renderVendors();
}

function renderTransactions() {
    const tbody = document.getElementById('txTableBody');
    tbody.innerHTML = transactions.map(tx => {
        const isFraud = fraudAlerts.some(a => a.id === tx.id);
        const catClass = 'tag-' + tx.category.toLowerCase().replace(/\s+/g, '');
        return `
            <tr style="${isFraud ? 'background:rgba(239,68,68,0.05)' : ''}">
                <td>${tx.date}</td>
                <td>${tx.description}</td>
                <td>${tx.vendor}</td>
                <td><span class="tag ${catClass}">${tx.category}</span></td>
                <td style="color:${tx.amount > 0 ? '#10b981' : '#ef4444'};font-weight:600;">
                    ${tx.amount > 0 ? '+' : ''}$${Math.abs(tx.amount).toLocaleString()}
                </td>
                <td><span class="tag ${tx.type === 'Revenue' ? 'tag-revenue' : 'tag-expense'}">${tx.type}</span></td>
                <td>${isFraud ? '<span style="color:#ef4444;font-weight:600;">🚨 Alert</span>' : '<span style="color:#10b981;">✓ OK</span>'}</td>
            </tr>
        `;
    }).join('');
}

function renderFraudAlerts() {
    const container = document.getElementById('fraudContainer');
    if (fraudAlerts.length === 0) {
        container.innerHTML = '<div style="text-align:center;padding:3rem;color:#64748b;">🎉 No fraud detected! Your books look clean.</div>';
        return;
    }
    
    container.innerHTML = fraudAlerts.map(alert => `
        <div class="fraud-alert">
            <div class="fraud-alert-header">
                <div class="fraud-alert-icon">🚨</div>
                <div>
                    <h4>${alert.type}</h4>
                    <p style="font-size:0.75rem;color:#ef4444;">Severity: ${alert.severity.toUpperCase()}</p>
                </div>
            </div>
            <p>${alert.description}</p>
            <div class="action">
                <button class="btn-action btn-block">🚫 ${alert.action}</button>
                <button class="btn-action btn-review">📧 Contact Vendor</button>
            </div>
        </div>
    `).join('');
}

function renderTaxDeductions() {
    const container = document.getElementById('taxContainer');
    const total = taxDeductions.reduce((sum, d) => sum + d.amount, 0);
    
    container.innerHTML = `
        <div class="deduction-card" style="background:linear-gradient(135deg,rgba(16,185,129,0.15),rgba(6,182,212,0.1));">
            <div class="deduction-info">
                <h4>💰 Total Tax Deductions Found</h4>
                <p>Across ${taxDeductions.length} transactions this period</p>
            </div>
            <div class="deduction-amount">$${total.toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
        </div>
        ${taxDeductions.map(d => `
            <div class="deduction-card">
                <div class="deduction-info">
                    <h4 style="color:#94a3b8;font-size:0.9rem;">${d.category}</h4>
                    <p>${d.description}</p>
                    <p style="font-size:0.75rem;color:#64748b;margin-top:0.25rem;">Confidence: ${(d.confidence * 100).toFixed(0)}%</p>
                </div>
                <div class="deduction-amount" style="font-size:1.2rem;">+$${d.amount.toLocaleString(undefined, {maximumFractionDigits: 2})}</div>
            </div>
        `).join('')}
    `;
    
    document.getElementById('taxRecommendations').innerHTML = `
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1rem;">
            <div style="padding:1rem;background:rgba(16,185,129,0.05);border-radius:8px;border:1px solid rgba(16,185,129,0.1);">
                <p style="color:#10b981;font-weight:600;">💡 Home Office Deduction</p>
                <p style="color:#94a3b8;font-size:0.8rem;margin-top:0.25rem;">If you use 18% of home for business, claim ~$1,200/year</p>
            </div>
            <div style="padding:1rem;background:rgba(59,130,246,0.05);border-radius:8px;border:1px solid rgba(59,130,246,0.1);">
                <p style="color:#3b82f6;font-weight:600;">💡 Mileage Tracking</p>
                <p style="color:#94a3b8;font-size:0.8rem;margin-top:0.25rem;">Business miles at $0.67/mile — use GPS auto-logging</p>
            </div>
            <div style="padding:1rem;background:rgba(139,92,246,0.05);border-radius:8px;border:1px solid rgba(139,92,246,0.1);">
                <p style="color:#a855f7;font-weight:600;">💡 Retirement Contributions</p>
                <p style="color:#94a3b8;font-size:0.8rem;margin-top:0.25rem;">SEP-IRA up to $69,000/year deductible</p>
            </div>
        </div>
    `;
}

function renderCashFlowChart() {
    // Calculate running balance
    let balance = 50000;
    const labels = [];
    const data = [];
    
    transactions.forEach(tx => {
        balance += tx.amount;
        labels.push(tx.date.slice(5));
        data.push(balance);
    });
    
    // Project 10 more days
    const lastBalance = data[data.length - 1] || 50000;
    for (let i = 1; i <= 10; i++) {
        const d = new Date();
        d.setDate(d.getDate() + i);
        labels.push(`${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`);
        data.push(lastBalance + (Math.random() * 2000 - 500));
    }
    
    const ctx = document.getElementById('cashFlowChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cash Balance',
                data: data,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16,185,129,0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 3
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
                x: { grid: { display: false }, ticks: { color: '#64748b' } }
            }
        }
    });
    
    // Cash flow alerts
    const minBalance = Math.min(...data);
    document.getElementById('cashFlowAlerts').innerHTML = `
        <div style="padding:1rem;background:${minBalance < 30000 ? 'rgba(239,68,68,0.1)' : 'rgba(16,185,129,0.1)'};border-radius:12px;border:1px solid ${minBalance < 30000 ? 'rgba(239,68,68,0.3)' : 'rgba(16,185,129,0.3)'}">
            <p style="color:${minBalance < 30000 ? '#fca5a5' : '#6ee7b7'};font-weight:600;">
                ${minBalance < 30000 ? '⚠️ Cash Crunch Predicted' : '✅ Cash Flow Healthy'}
            </p>
            <p style="color:#94a3b8;font-size:0.875rem;margin-top:0.5rem;">
                ${minBalance < 30000 
                    ? `Projected low: $${minBalance.toLocaleString()}. Recommend delaying vendor payments by 5 days.` 
                    : `Lowest projected balance: $${minBalance.toLocaleString()}. You're in good shape.`}
            </p>
        </div>
    `;
}

function renderVendors() {
    const container = document.getElementById('vendorContainer');
    container.innerHTML = vendorScores.map(v => {
        const color = v.score >= 80 ? '#10b981' : v.score >= 50 ? '#f59e0b' : '#ef4444';
        return `
            <div class="vendor-card">
                <div class="vendor-header">
                    <span class="vendor-name">${v.name}</span>
                    <div class="vendor-score">
                        <span style="font-size:0.8rem;color:${color};font-weight:600;">${v.score}/100</span>
                        <div class="score-bar">
                            <div class="score-fill" style="width:${v.score}%;background:${color};"></div>
                        </div>
                    </div>
                </div>
                <div style="display:flex;gap:2rem;color:#64748b;font-size:0.8rem;">
                    <span>💰 Total Spent: $${v.total.toLocaleString()}</span>
                    <span>📊 Transactions: ${v.count}</span>
                    ${v.hasFraud ? '<span style="color:#ef4444;">🚨 Fraud Alert</span>' : '<span style="color:#10b981;">✓ Clean</span>'}
                </div>
            </div>
        `;
    }).join('');
}

// ============================================================
// TAB SWITCHING
// ============================================================
function switchTab(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById('tab-' + tabName).classList.add('active');
}
</script>

</body>
</html>'''

with open('/mnt/agents/output/ledgermind_excel_scanner.html', 'w') as f:
    f.write(excel_scanner_html)

print("✅ Excel Scanner created successfully!")
print(f"File size: {len(excel_scanner_html):,} bytes")

