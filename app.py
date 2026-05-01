from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Self Learning Prediction Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: linear-gradient(135deg, #020617, #111827);
      color: white;
      padding: 16px;
    }

    .container {
      max-width: 1150px;
      margin: auto;
    }

    .header {
      text-align: center;
      margin-bottom: 18px;
    }

    h1 {
      margin: 0;
      font-size: 28px;
    }

    .sub {
      color: #94a3b8;
      font-size: 13px;
      margin-top: 8px;
    }

    .live-dot {
      display: inline-block;
      width: 10px;
      height: 10px;
      background: #22c55e;
      border-radius: 50%;
      margin-right: 7px;
      box-shadow: 0 0 12px #22c55e;
    }

    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }

    .box {
      background: rgba(17, 24, 39, 0.96);
      border: 1px solid #1f2937;
      border-radius: 22px;
      padding: 18px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.38);
    }

    .box h2 {
      margin: 0 0 14px;
      font-size: 20px;
      color: #e5e7eb;
    }

    .big-number {
      font-size: 58px;
      text-align: center;
      font-weight: 900;
      color: #facc15;
      margin: 8px 0 14px;
    }

    .predict-number {
      font-size: 72px;
      text-align: center;
      font-weight: 900;
      color: #38bdf8;
      margin: 8px 0 6px;
    }

    .row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      padding: 10px 0;
      border-bottom: 1px solid #374151;
    }

    .row:last-child {
      border-bottom: none;
    }

    .label {
      color: #9ca3af;
      font-size: 14px;
    }

    .value {
      font-weight: bold;
      font-size: 16px;
      text-align: right;
      word-break: break-word;
    }

    .status {
      text-align: center;
      margin: 14px 0;
      color: #facc15;
      font-size: 14px;
      min-height: 20px;
    }

    .buttons {
      display: flex;
      gap: 10px;
      margin: 12px 0 0;
    }

    button {
      flex: 1;
      padding: 12px;
      border: none;
      border-radius: 13px;
      font-size: 15px;
      font-weight: bold;
      cursor: pointer;
      color: white;
    }

    .btn-start {
      background: #16a34a;
    }

    .btn-stop {
      background: #dc2626;
    }

    .btn-refresh {
      background: #2563eb;
    }

    .btn-clear {
      background: #334155;
    }

    .cards {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-top: 16px;
    }

    .mini {
      background: #1f2937;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 14px;
      text-align: center;
    }

    .mini .num {
      font-size: 24px;
      font-weight: 900;
      color: #facc15;
      margin-top: 6px;
    }

    .mini .txt {
      color: #94a3b8;
      font-size: 12px;
    }

    .history-title {
      margin: 16px 0 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .count {
      color: #facc15;
      font-size: 13px;
    }

    .table-wrap {
      max-height: 430px;
      overflow-y: auto;
      border: 1px solid #374151;
      border-radius: 14px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }

    th, td {
      padding: 9px 6px;
      border-bottom: 1px solid #374151;
      text-align: center;
    }

    th {
      background: #111827;
      color: #facc15;
      position: sticky;
      top: 0;
      z-index: 2;
    }

    td {
      color: #e5e7eb;
    }

    .green {
      color: #22c55e;
      font-weight: bold;
    }

    .red {
      color: #ef4444;
      font-weight: bold;
    }

    .violet {
      color: #a855f7;
      font-weight: bold;
    }

    .ok {
      color: #22c55e;
      font-weight: bold;
    }

    .bad {
      color: #ef4444;
      font-weight: bold;
    }

    .warn {
      color: #facc15;
      font-weight: bold;
    }

    .alt-list {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-top: 10px;
    }

    .alt-card {
      background: #1f2937;
      border: 1px solid #334155;
      border-radius: 15px;
      padding: 12px;
      text-align: center;
    }

    .alt-card .n {
      font-size: 28px;
      font-weight: 900;
      color: #facc15;
    }

    .alt-card .p {
      color: #94a3b8;
      font-size: 12px;
      margin-top: 4px;
    }

    .weights {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin-top: 8px;
    }

    .weight {
      background: #1f2937;
      border-radius: 12px;
      padding: 10px;
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      border: 1px solid #334155;
    }

    .footer-note {
      color: #94a3b8;
      font-size: 12px;
      text-align: center;
      margin-top: 16px;
      line-height: 1.6;
    }

    @media (max-width: 850px) {
      .grid {
        grid-template-columns: 1fr;
      }

      .cards {
        grid-template-columns: repeat(2, 1fr);
      }

      .alt-list {
        grid-template-columns: repeat(2, 1fr);
      }

      .weights {
        grid-template-columns: 1fr;
      }

      .predict-number {
        font-size: 58px;
      }
    }
  </style>
</head>
<body>

<div class="container">

  <div class="header">
    <h1><span class="live-dot"></span>Self Learning Prediction Dashboard</h1>
    <div class="sub">
      Cloudflare Worker + KV Memory + Adaptive Model Weights
    </div>
  </div>

  <div class="grid">

    <div class="box">
      <h2>Latest Result</h2>

      <div class="big-number" id="latestNumber">---</div>

      <div class="row">
        <span class="label">Issue Number:</span>
        <span class="value" id="latestIssue">---</span>
      </div>

      <div class="row">
        <span class="label">Number:</span>
        <span class="value" id="latestNumberSmall">---</span>
      </div>

      <div class="row">
        <span class="label">Colour:</span>
        <span class="value" id="latestColour">---</span>
      </div>

      <div class="row">
        <span class="label">Saved Time:</span>
        <span class="value" id="latestTime">---</span>
      </div>

      <div class="buttons">
        <button class="btn-start" onclick="startAuto()">Start</button>
        <button class="btn-stop" onclick="stopAuto()">Stop</button>
      </div>

      <div class="buttons">
        <button class="btn-refresh" onclick="loadAll()">Refresh Now</button>
        <button class="btn-clear" onclick="clearTableOnly()">Clear Table</button>
      </div>

      <div class="status" id="status">Page loaded...</div>
    </div>

    <div class="box">
      <h2>Next Prediction</h2>

      <div class="predict-number" id="predictedNumber">---</div>

      <div class="row">
        <span class="label">Predict For Issue:</span>
        <span class="value" id="predictIssue">---</span>
      </div>

      <div class="row">
        <span class="label">Big / Small:</span>
        <span class="value" id="predictBigSmall">---</span>
      </div>

      <div class="row">
        <span class="label">Predicted Colour:</span>
        <span class="value" id="predictColour">---</span>
      </div>

      <div class="row">
        <span class="label">Confidence:</span>
        <span class="value" id="predictConfidence">---</span>
      </div>

      <div class="row">
        <span class="label">Created At:</span>
        <span class="value" id="predictTime">---</span>
      </div>

      <h2 style="font-size:16px;margin-top:16px;">Alternative Numbers</h2>
      <div class="alt-list" id="alternatives"></div>
    </div>

  </div>

  <div class="cards">
    <div class="mini">
      <div class="txt">Total Checked</div>
      <div class="num" id="totalChecked">0</div>
    </div>
    <div class="mini">
      <div class="txt">Correct</div>
      <div class="num ok" id="correctCount">0</div>
    </div>
    <div class="mini">
      <div class="txt">Wrong</div>
      <div class="num bad" id="wrongCount">0</div>
    </div>
    <div class="mini">
      <div class="txt">Accuracy</div>
      <div class="num" id="accuracyPercent">0%</div>
    </div>
  </div>

  <div class="grid" style="margin-top:16px;">

    <div class="box">
      <h2>Last Checked Prediction</h2>

      <div class="row">
        <span class="label">Issue:</span>
        <span class="value" id="checkedIssue">---</span>
      </div>

      <div class="row">
        <span class="label">Predicted Number:</span>
        <span class="value" id="checkedPredicted">---</span>
      </div>

      <div class="row">
        <span class="label">Actual Number:</span>
        <span class="value" id="checkedActual">---</span>
      </div>

      <div class="row">
        <span class="label">Result:</span>
        <span class="value" id="checkedResult">---</span>
      </div>

      <div class="row">
        <span class="label">Checked At:</span>
        <span class="value" id="checkedAt">---</span>
      </div>
    </div>

    <div class="box">
      <h2>Model Weights Memory</h2>
      <div class="weights" id="weightsBox"></div>
    </div>

  </div>

  <div class="box" style="margin-top:16px;">
    <div class="history-title">
      <h2 style="margin:0;">Saved History</h2>
      <span class="count" id="totalHistory">Total: 0</span>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Issue</th>
            <th>Number</th>
            <th>Colour</th>
            <th>Saved Time</th>
          </tr>
        </thead>
        <tbody id="historyBody"></tbody>
      </table>
    </div>
  </div>

  <div class="footer-note">
    This is a probability-based self-learning project. It improves model weights from previous prediction results,
    but it cannot guarantee future random outcomes.
  </div>

</div>

<script>
let timer = null;
let running = false;

const API_BASE = "https://live-result-worker.deepkoley156.workers.dev";

const URLS = {
  latest: API_BASE + "/api/latest",
  history: API_BASE + "/api/history",
  lastPrediction: API_BASE + "/api/last-prediction",
  accuracy: API_BASE + "/api/accuracy",
  lastChecked: API_BASE + "/api/last-checked",
  fetchNow: API_BASE + "/api/fetch-now"
};

function colourClass(colour) {
  if (!colour) return "";
  const c = String(colour).toLowerCase();

  if (c.includes("green")) return "green";
  if (c.includes("red")) return "red";
  if (c.includes("violet")) return "violet";

  return "";
}

function formatTime(timeText) {
  if (!timeText) return "---";

  try {
    const d = new Date(timeText);
    if (isNaN(d.getTime())) return timeText;
    return d.toLocaleString();
  } catch (e) {
    return timeText;
  }
}

function setText(id, value) {
  document.getElementById(id).innerText =
    value === undefined || value === null || value === "" ? "---" : value;
}

async function loadLatest() {
  const res = await fetch(URLS.latest);
  const data = await res.json();

  if (!data.success || !data.result) return;

  const item = data.result;

  setText("latestIssue", item.issueNumber);
  setText("latestNumber", item.number);
  setText("latestNumberSmall", item.number);
  setText("latestTime", formatTime(item.savedTime));

  const colourEl = document.getElementById("latestColour");
  colourEl.innerText = item.colour || "---";
  colourEl.className = "value " + colourClass(item.colour);
}

async function loadPrediction() {
  const res = await fetch(URLS.lastPrediction);
  const data = await res.json();

  if (!data.success || !data.prediction) return;

  const p = data.prediction;

  setText("predictedNumber", p.predictedNumber);
  setText("predictIssue", p.predictForIssue);
  setText("predictBigSmall", p.predictedBigSmall);

  const colourEl = document.getElementById("predictColour");
  colourEl.innerText = p.predictedColour || "---";
  colourEl.className = "value " + colourClass(p.predictedColour);

  setText("predictConfidence", (p.confidence || 0) + "%");
  setText("predictTime", formatTime(p.createdAt));

  const altBox = document.getElementById("alternatives");
  altBox.innerHTML = "";

  const alternatives = p.alternatives || [];

  alternatives.forEach(a => {
    const html = `
      <div class="alt-card">
        <div class="n">${a.number}</div>
        <div class="p">${a.bigSmall || ""}</div>
        <div class="p ${colourClass(a.colour)}">${a.colour || ""}</div>
        <div class="p">${a.confidence || 0}%</div>
      </div>
    `;
    altBox.insertAdjacentHTML("beforeend", html);
  });

  if (!alternatives.length) {
    altBox.innerHTML = "<div class='warn'>No alternatives yet</div>";
  }
}

async function loadAccuracy() {
  const res = await fetch(URLS.accuracy);
  const data = await res.json();

  if (!data.success) return;

  const acc = data.accuracy || {};
  const weights = data.modelWeights || {};

  setText("totalChecked", acc.totalChecked || 0);
  setText("correctCount", acc.correct || 0);
  setText("wrongCount", acc.wrong || 0);
  setText("accuracyPercent", (acc.accuracyPercent || 0) + "%");

  const weightsBox = document.getElementById("weightsBox");
  weightsBox.innerHTML = "";

  Object.keys(weights).forEach(k => {
    const html = `
      <div class="weight">
        <span>${k}</span>
        <b>${weights[k]}</b>
      </div>
    `;
    weightsBox.insertAdjacentHTML("beforeend", html);
  });
}

async function loadLastChecked() {
  const res = await fetch(URLS.lastChecked);
  const data = await res.json();

  if (!data.success || !data.lastCheckedPrediction) return;

  const p = data.lastCheckedPrediction;

  setText("checkedIssue", p.predictForIssue);
  setText("checkedPredicted", p.predictedNumber);
  setText("checkedActual", p.actualNumber);
  setText("checkedAt", formatTime(p.checkedAt));

  const resultEl = document.getElementById("checkedResult");

  if (p.correct === true) {
    resultEl.innerText = "Correct";
    resultEl.className = "value ok";
  } else if (p.correct === false) {
    resultEl.innerText = "Wrong";
    resultEl.className = "value bad";
  } else {
    resultEl.innerText = "---";
    resultEl.className = "value";
  }
}

async function loadHistory() {
  const res = await fetch(URLS.history);
  const data = await res.json();

  if (!data.success) return;

  setText("totalHistory", "Total: " + (data.total || 0));

  const tbody = document.getElementById("historyBody");
  tbody.innerHTML = "";

  const results = data.results || [];

  results.forEach(item => {
    const html = `
      <tr>
        <td>${item.issueNumber || ""}</td>
        <td>${item.number || ""}</td>
        <td class="${colourClass(item.colour)}">${item.colour || ""}</td>
        <td>${formatTime(item.savedTime || item.time)}</td>
      </tr>
    `;

    tbody.insertAdjacentHTML("beforeend", html);
  });
}

async function loadAll() {
  try {
    document.getElementById("status").innerText = "Refreshing...";

    await Promise.all([
      loadLatest(),
      loadPrediction(),
      loadAccuracy(),
      loadLastChecked(),
      loadHistory()
    ]);

    document.getElementById("status").innerText =
      "Last refresh: " + new Date().toLocaleTimeString();

  } catch (err) {
    document.getElementById("status").innerText =
      "Error: " + err.message;
  }
}

function startAuto() {
  if (running) return;

  running = true;
  loadAll();
  timer = setInterval(loadAll, 10000);

  document.getElementById("status").innerText = "Auto refresh started";
}

function stopAuto() {
  clearInterval(timer);
  timer = null;
  running = false;

  document.getElementById("status").innerText = "Auto refresh stopped";
}

function clearTableOnly() {
  document.getElementById("historyBody").innerHTML = "";
  document.getElementById("status").innerText =
    "Only table view cleared. Saved data is not deleted.";
}

window.onload = function() {
  startAuto();
};
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
