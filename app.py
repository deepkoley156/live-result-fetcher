from flask import Flask, jsonify, render_template_string
import requests
import time

app = Flask(__name__)

API_URL = "https://api.bdg88zf.com/api/webapi/GetNoaverageEmerdList"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120.0 Mobile Safari/537.36",
    "Origin": "https://okwin.bio",
    "Referer": "https://okwin.bio/"
}

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
      max-width: 520px;
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

    .number-big {
      font-size: 42px;
      text-align: center;
      font-weight: 800;
      margin: 12px 0;
      color: #facc15;
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

    .clear {
      background: #334155;
      margin-top: 10px;
      width: 100%;
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
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 8px;
      font-size: 13px;
      overflow: hidden;
      border-radius: 12px;
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
      max-height: 360px;
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
    </div>

    <div class="buttons">
      <button class="start" onclick="startFetch()">Start</button>
      <button class="stop" onclick="stopFetch()">Stop</button>
    </div>

    <button class="clear" onclick="clearHistory()">Clear History</button>

    <div class="status" id="status">Page loaded. Auto fetch starting...</div>

    <div class="history-title">History</div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Issue</th>
            <th>Number</th>
            <th>Colour</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody id="history"></tbody>
      </table>
    </div>

    <div class="small-text">
      Auto fetch interval: 5 seconds
    </div>
  </div>

<script>
let timer = null;
let lastIssue = "";
let isRunning = false;

function colourClass(colour) {
  if (!colour) return "";
  const c = colour.toLowerCase();
  if (c.includes("green")) return "green";
  if (c.includes("red")) return "red";
  if (c.includes("violet")) return "violet";
  return "";
}

async function fetchData() {
  try {
    document.getElementById("status").innerText = "Fetching...";

    const res = await fetch("/api/latest");
    const data = await res.json();

    if (data.success) {
      const item = data.result;

      document.getElementById("issueNumber").innerText = item.issueNumber;
      document.getElementById("number").innerText = item.number;
      document.getElementById("numberSmall").innerText = item.number;

      const colourEl = document.getElementById("colour");
      colourEl.innerText = item.colour;
      colourEl.className = "value " + colourClass(item.colour);

      document.getElementById("status").innerText = "Last update: " + new Date().toLocaleTimeString();

      if (item.issueNumber !== lastIssue) {
        lastIssue = item.issueNumber;

        const row = `
          <tr>
            <td>${item.issueNumber}</td>
            <td>${item.number}</td>
            <td class="${colourClass(item.colour)}">${item.colour}</td>
            <td>${new Date().toLocaleTimeString()}</td>
          </tr>
        `;

        document.getElementById("history").insertAdjacentHTML("afterbegin", row);
      }

    } else {
      document.getElementById("status").innerText = data.message || "No data found";
    }

  } catch (err) {
    document.getElementById("status").innerText = "Fetch error: " + err.message;
  }
}

function startFetch() {
  if (isRunning) return;

  isRunning = true;
  fetchData();
  timer = setInterval(fetchData, 5000);

  document.getElementById("status").innerText = "Auto fetch started";
}

function stopFetch() {
  clearInterval(timer);
  timer = null;
  isRunning = false;

  document.getElementById("status").innerText = "Auto fetch stopped";
}

function clearHistory() {
  document.getElementById("history").innerHTML = "";
  lastIssue = "";
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

@app.route("/api/latest")
def latest():
    payload = {
        "pageSize": 10,
        "pageNo": 1,
        "typeId": 1,
        "language": 0,
        "random": "4a0522c6ecd8410496260e686be2a57c",
        "signature": "334B5E70A0C9B8918B0B15E517E2069C",
        "timestamp": int(time.time())
    }

    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=20)

        if response.status_code != 200:
            return jsonify({
                "success": False,
                "message": "API status: " + str(response.status_code)
            })

        data = response.json()
        rows = data.get("data", {}).get("list", [])

        if not rows:
            return jsonify({
                "success": False,
                "message": "No data found"
            })

        latest_item = rows[0]

        return jsonify({
            "success": True,
            "result": {
                "issueNumber": latest_item.get("issueNumber", ""),
                "number": latest_item.get("number", ""),
                "colour": latest_item.get("colour", "")
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
