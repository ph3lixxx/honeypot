import re
import os
import json
from datetime import datetime
import requests

LOG_FILE = "logs/activity.log"

def parse_log():
    if not os.path.exists(LOG_FILE):
        print("[!] File log tidak ditemukan.")
        return []

    with open(LOG_FILE, "r") as f:
        log_data = f.read()

    entries = log_data.split("="*60)
    parsed_entries = []

    for entry in entries:
        lines = entry.strip().split("\n")
        if not lines or len(lines) < 4:
            continue

        try:
            time = lines[0].replace("Time: ", "").strip()
            ip = lines[1].replace("IP: ", "").strip()
            method = lines[2].replace("Method: ", "").strip()
            path = lines[3].replace("Path: ", "").strip()

            headers_line = next((line for line in lines if "Headers:" in line), "")
            headers = eval(headers_line.replace("Headers: ", "").strip()) if headers_line else {}

            form_line = next((line for line in lines if "Form Data:" in line), "")
            form_data = eval(form_line.replace("Form Data: ", "").strip()) if form_line else {}

            parsed_entries.append({
                "time": time,
                "ip": ip,
                "method": method,
                "path": path,
                "headers": headers,
                "form_data": form_data
            })
        except Exception as e:
            print(f"[!] Gagal parsing satu entry: {e}")
            continue

    return parsed_entries

def ip_lookup(ip):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if res.status_code == 200:
            data = res.json()
            return f"{data.get('city', '')}, {data.get('region', '')}, {data.get('country', '')} | ISP: {data.get('org', '')}"
    except:
        pass
    return "Tidak diketahui"

def detect_attack(data):
    suspicious = []
    combined = json.dumps(data.get("form_data", {})) + data.get("path", "")
    
    if re.search(r"('|--|%27|\bOR\b|\bSELECT\b|\bUNION\b)", combined, re.IGNORECASE):
        suspicious.append("🔥 Kemungkinan SQL Injection")

    if re.search(r"<script>|%3Cscript%3E|onerror=|alert\(", combined, re.IGNORECASE):
        suspicious.append("⚠️ Kemungkinan XSS (Cross Site Scripting)")

    if data.get("path", "") == "/" and data["method"] == "POST" and "password" in combined.lower():
        suspicious.append("🔑 Kemungkinan brute-force login")

    if "sqlmap" in data.get("headers", {}).get("User-Agent", "").lower():
        suspicious.append("🤖 Deteksi otomatis tool SQLMap")

    return suspicious

def explain_log(parsed_logs):
    for i, log in enumerate(parsed_logs):
        print(f"\n📌 Aktivitas #{i+1}")
        print(f"🕒 Waktu: {log['time']}")
        print(f"🌐 IP: {log['ip']} ({ip_lookup(log['ip'])})")
        print(f"📩 Metode: {log['method']}")
        print(f"📍 Path: {log['path']}")
        print(f"📦 Form Data: {log['form_data'] if log['form_data'] else 'Tidak ada'}")

        attacks = detect_attack(log)
        if attacks:
            print("🚨 Analisa Serangan:")
            for atk in attacks:
                print(f"   → {atk}")
        else:
            print("✅ Tidak terdeteksi aktivitas mencurigakan.")
        print("-" * 50)

if __name__ == "__main__":
    logs = parse_log()
    if logs:
        explain_log(logs)
    else:
        print("[!] Tidak ada log untuk dianalisa.")
