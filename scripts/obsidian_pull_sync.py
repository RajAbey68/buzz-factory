import os
import subprocess

REMOTE_SERVER = os.environ.get("BUZZ_DEVSERVER_HOST", "user@devserver.hostinger")
REMOTE_PATH = "~/.hermes/inbox/buzz-digest.md"
LOCAL_VAULT_PATH = "/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/buzz-digest.md"
LOCAL_SECOND_BRAIN = "/Users/arajiv/second-brain/inbox/buzz-digest.md"

def pull_sync():
    print(f"[PULL SYNC] Fetching remote digest from {REMOTE_SERVER}:{REMOTE_PATH}...")
    cmd = f"rsync -avz -e ssh {REMOTE_SERVER}:{REMOTE_PATH} /tmp/buzz-digest-pull.md 2>/dev/null || true"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if os.path.exists("/tmp/buzz-digest-pull.md") and os.path.getsize("/tmp/buzz-digest-pull.md") > 0:
        with open("/tmp/buzz-digest-pull.md", "r", encoding="utf-8") as f:
            pulled_content = f.read()

        for local_target in [LOCAL_VAULT_PATH, LOCAL_SECOND_BRAIN]:
            os.makedirs(os.path.dirname(local_target), exist_ok=True)
            with open(local_target, "a", encoding="utf-8") as target_file:
                target_file.write(f"\n\n<!-- Pulled via Mac Watchdog -->\n{pulled_content}")
            print(f"[PULL SYNC SUCCESS] Merged remote digest into {local_target}")

        os.remove("/tmp/buzz-digest-pull.md")
    else:
        print("[PULL SYNC NOTICE] Remote server unavailable or no new pull digest available.")

if __name__ == "__main__":
    pull_sync()
