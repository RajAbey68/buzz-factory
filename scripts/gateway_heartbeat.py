import os
import sys
import time
import urllib.request
import json

GATEWAY_HEALTH_URL = os.environ.get("BUZZ_GATEWAY_HEALTH_URL", "http://devserver.local:8090/v1/health")
HEARTBEAT_LOG = "/tmp/buzz_gateway_heartbeat.log"
MAX_FAILED_BEATS = 2
MAX_RESTARTS_PER_DAY = 5

def check_heartbeat():
    failed_count = 0
    restarts_today = 0
    if os.path.exists(HEARTBEAT_LOG):
        try:
            with open(HEARTBEAT_LOG, "r") as f:
                data = json.load(f)
                failed_count = data.get("failed_count", 0)
                restarts_today = data.get("restarts_today", 0)
        except Exception:
            failed_count = 0

    try:
        req = urllib.request.Request(GATEWAY_HEALTH_URL, headers={"User-Agent": "BuzzGatewayHeartbeat/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                print(f"[HEARTBEAT OK] buzz-acp gateway healthy on {GATEWAY_HEALTH_URL}")
                with open(HEARTBEAT_LOG, "w") as f:
                    json.dump({"failed_count": 0, "restarts_today": restarts_today, "last_ok": time.time()}, f)
                return True
    except Exception as e:
        failed_count += 1
        print(f"[HEARTBEAT WARNING] Beat failed ({failed_count}/{MAX_FAILED_BEATS}): {e}")
        with open(HEARTBEAT_LOG, "w") as f:
            json.dump({"failed_count": failed_count, "restarts_today": restarts_today, "last_fail": time.time()}, f)

    if failed_count >= MAX_FAILED_BEATS:
        if restarts_today >= MAX_RESTARTS_PER_DAY:
            print(f"[HEARTBEAT CRITICAL] Max daily restarts ({MAX_RESTARTS_PER_DAY}) reached. Manual admin intervention required.")
            return False

        print(f"[HEARTBEAT ALERT] Gateway missed {MAX_FAILED_BEATS} consecutive beats! Triggering auto-restart...")
        restarts_today += 1
        restart_cmd = "systemctl --user restart buzz-acp 2>/dev/null || systemctl restart buzz-acp 2>/dev/null || pkill -f 'buzz_acp' || true"
        os.system(restart_cmd)
        
        with open(HEARTBEAT_LOG, "w") as f:
            json.dump({"failed_count": 0, "restarts_today": restarts_today, "last_restart": time.time()}, f)

    return False

if __name__ == "__main__":
    check_heartbeat()
