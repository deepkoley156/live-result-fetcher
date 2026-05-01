from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Live Result Fetcher</title>
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

    .box {
      max-width: 560px;
      margin: auto;
      background: rgba(17, 24, 39, 0.95);
      padding: 20px;
      border-radius: 22px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.45);
      border: 1px solid #1f2937;
    }

    h2 {
      text-align: center;
      margin: 0 0 20px;
      font-size: 24px;
    }

    .live-dot {
      display: inline-block;
      width: 10px;
      height: 10px;
      background: #22c55e;
      border-radius: 50%;
      margin-right: 6px;
      box-shadow: 0 0 12px #22c55e;
    }

    .card {
      background: #1f2937;
      padding: 16px;
      border-radius: 16px;
      margin-bottom: 16px;
    }

    .number-big {
      font-size: 46px;
      text-align: center;
      font-weight: 800;
      margin: 12px 0;
      color: #facc15;
    }

    .row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      padding: 11px 0;
      border-bottom: 1px solid #374151;
    }

    .row:last-child {
      border-bottom: none;
    }

    .label {
      color: #9ca3af;
      font-size: 15px;
    }

    .value {
      font-weight: bold;
      font-size: 18px;
      word-break: break-word;
      text-align: right;
    }

    .buttons {
      display: flex;
      gap: 10px;
      margin-top: 12px;
    }

    button {
      flex: 1;
      padding: 13px;
      border: none;
      border-radius: 14px;
      font-size: 16px;
      font-weight: bold;
      cursor: pointer;
      color: white;
    }

    .start {
      background: #16a34a;
    }

    .stop {
      background: #dc2626;
    }

    .refresh {
      background: #2563eb;
      width: 100%;
      margin-top: 10px;
    }

    .clear {
      background: #334155;
      width: 100%;
      margin-top: 10px;
    }

    .status {
      text-align: center;
      margin: 15px 0;
      color: #facc15;
      font-size: 14px;
      min-height: 20px;
    }

    .history-title {
      margin-top: 18px;
      margin-bottom: 8px;
      color: #e5e7eb;
      font-size: 16px;
      font-weight: bold;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .count {
      color: #facc15;
      font-size: 13px;
      font-weight: normal;
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
      color: #facc15;
      background: #111827;
      position: sticky;
      top: 0;
    }

    td {
      color: #e5e7eb;
    }

    .table-wrap {
      max-height: 420px;
      overflow-y: auto;
      border: 1px solid #374151;
      border-radius: 12px;
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

    .small-text {
      color: #94a3b8;
      text-align: center;
      font-size: 12px;
      margin-top: 14px;
      line-height: 1.5;
    }
  </style>
</head>
<body>

  <div class="box">
    <h2><span class="live-dot"></span>Live Result Fetcher</h2>

    <div class="card">
      <div class="number-big" id="number">---</div>

      <div class="row">
        <span class="label">Issue Number:</span>
        <span class="value" id="issueNumber">---</span>
      </div>

      <div class="row">
        <span class="label">Number:</span>
        <span class="value" id="numberSmall">---</span>
      </div>

      <div class="row">
        <span class="label">Colour:</span>
        <span class="value" id="colour">---</span>
      </div>

      <div class="row">
        <span class="label">Saved Time:</span>
        <span class="value" id="savedTime">---</span>
      </div>
    </div>

    <div class="buttons">
      <button class="start" onclick="startFetch()">Start</button>
      <button class="stop" onclick="stopFetch()">Stop</button>
    </div>

    <button class="refresh" onclick="loadAll()">Refresh Now</button>
    <button class="clear" onclick="clearTableOnly()">Clear Table View</button>

    <div class="status" id="status">Page loaded. Auto refresh starting...</div>

    <div class="history-title">
      <span>Saved History</span>
      <span class="count" id="totalCount">Total: 0</span>
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
        <tbody id="history"></tbody>
      </table>
    </div>

    <div class="small-text">
      Data is saved in Cloudflare KV storage.<br>
      Worker auto fetch interval: 1 minute using Cron Trigger.<br>
      Webpage refresh interval: 10 seconds.
    </div>
  </div>

<script>
let timer = null;
let isRunning = false;

const API_BASE = "https://live-result-worker.deepkoley156.workers.dev";
const LATEST_LINK = API_BASE + "/api/latest";
const HISTORY_LINK = API_BASE + "/api/history";

function colourClass(colour) {
  if (!colour) return "";
  const c = colour.toLowerCase();

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

async function loadLatest() {
  try {
    const res = await fetch(LATEST_LINK);
    const data = await res.json();

    if (!data.success || !data.result) {
      document.getElementById("status").innerText = data.message || "Latest data not found";
      return;
    }

    const item = data.result;

    document.getElementById("issueNumber").innerText = item.issueNumber || "---";
    document.getElementById("number").innerText = item.number || "---";
    document.getElementById("numberSmall").innerText = item.number || "---";
    document.getElementById("savedTime").innerText = formatTime(item.savedTime);

    const colourEl = document.getElementById("colour");
    colourEl.innerText = item.colour || "---";
    colourEl.className = "value " + colourClass(item.colour);

    document.getElementById("status").innerText =
      "Latest updated: " + new Date().toLocaleTimeString();

  } catch (err) {
    document.getElementById("status").innerText = "Latest fetch error: " + err.message;
  }
}

async function loadHistory() {
  try {
    const res = await fetch(HISTORY_LINK);
    const data = await res.json();

    if (!data.success) {
      document.getElementById("status").innerText = data.message || "History not found";
      return;
    }

    document.getElementById("totalCount").innerText = "Total: " + (data.total || 0);

    const tbody = document.getElementById("history");
    tbody.innerHTML = "";

    const results = data.results || [];

    results.forEach(item => {
      const row = `
        <tr>
          <td>${item.issueNumber || ""}</td>
          <td>${item.number || ""}</td>
          <td class="${colourClass(item.colour)}">${item.colour || ""}</td>
          <td>${formatTime(item.savedTime || item.time)}</td>
        </tr>
      `;

      tbody.insertAdjacentHTML("beforeend", row);
    });

  } catch (err) {
    document.getElementById("status").innerText = "History fetch error: " + err.message;
  }
}

async function loadAll() {
  document.getElementById("status").innerText = "Refreshing...";
  await loadLatest();
  await loadHistory();
}

function startFetch() {
  if (isRunning) return;

  isRunning = true;
  loadAll();

  timer = setInterval(loadAll, 10000);

  document.getElementById("status").innerText = "Auto refresh started";
}

function stopFetch() {
  clearInterval(timer);
  timer = null;
  isRunning = false;

  document.getElementById("status").innerText = "Auto refresh stopped";
}

function clearTableOnly() {
  document.getElementById("history").innerHTML = "";
  document.getElementById("status").innerText = "Only table view cleared. Saved data is not deleted.";
}

window.onload = function() {
  startFetch();
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
