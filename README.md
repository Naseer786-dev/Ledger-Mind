<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LedgerMind Excel Scanner</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen flex items-center justify-center p-4">
<div class="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full">
<h1 class="text-3xl font-bold text-center text-indigo-600 mb-2">LedgerMind AI Bookkeeper</h1>
<p class="text-center text-gray-600 mb-6">Upload Excel and detect fraud automatically</p>
<div class="border-2 border-dashed border-indigo-300 rounded-xl p-8 text-center mb-4">
<input type="file" id="fileInput" accept=".xlsx,.xls" class="hidden">
<label for="fileInput" class="cursor-pointer text-indigo-600 font-semibold">Click to Choose Excel File</label>
<p id="fileName" class="text-sm text-gray-500 mt-2"></p>
</div>
<button id="scanBtn" class="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700">Scan for Fraud</button>
<div id="results" class="mt-6 hidden"></div>
</div>
<script>
const API_URL = "https://ledger-mind-api.onrender.com/scan";
document.getElementById('fileInput').onchange = e => {
document.getElementById('fileName').textContent = e.target.files[0]?.name || '';
};
document.getElementById('scanBtn').onclick = async () => {
const file = document.getElementById('fileInput').files[0];
if(!file) return alert('Pick a file first!');
const formData = new FormData();
formData.append('file', file);
document.getElementById('scanBtn').textContent = 'Scanning...';
const res = await fetch(API_URL, {method: 'POST', body: formData});
const data = await res.json();
document.getElementById('results').classList.remove('hidden');
document.getElementById('results').innerHTML = `<pre class="bg-gray-100 p-4 rounded">${JSON.stringify(data, null, 2)}</pre>`;
document.getElementById('scanBtn').textContent = 'Scan for Fraud';
};
</script>
</body>
</html>


