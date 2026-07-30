import os
import subprocess
import hashlib

REMOTE_SERVER = os.environ.get("BUZZ_DEVSERVER_HOST", "user@devserver.hostinger")
REMOTE_PATH = "~/.hermes/inbox/buzz-digest.md"
LOCAL_VAULT_PATH = "/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/buzz-digest.md"
LOCAL_SECOND_BRAIN = "/Users/arajiv/second-brain/inbox/buzz-digest.md"
HASH_TRACKER = "/tmp/.buzz_synced_hashes.log"

def is_hash_logged(content_hash):
    if os.path.exists(HASH_TRACKER):
        with open(HASH_TRACKER, "r") as f:
            return content_hash in f.read().splitlines()
    return False

def mark_hash_logged(content_hash):
    with open(HASH_TRACKER, "a") as f:
        f.write(content_hash + "\n")

def pull_sync():
    print(f"[PULL SYNC] Fetching remote digest from {REMOTE_SERVER}:{REMOTE_PATH}...")
    cmd = [
        "rsync", "-avz",
        "-e", "ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ForwardAgent=no",
        f"{REMOTE_SERVER}:{REMOTE_PATH}",
        "/tmp/buzz-digest-pull.md"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=15)
    except Exception as e:
        print(f"[PULL SYNC NOTICE] Remote server unavailable or pull sync skipped: {e}")
        return

    if os.path.exists("/tmp/buzz-digest-pull.md") and os.path.getsize("/tmp/buzz-digest-pull.md") > 0:
        with open("/tmp/buzz-digest-pull.md", "r", encoding="utf-8") as f:
            pulled_content = f.read()

        content_hash = hashlib.sha256(pulled_content.encode("utf-8")).hexdigest()

        if is_hash_logged(content_hash):
            print("[PULL SYNC DEDUP] Content hash already logged. Skipping duplicate append.")
        else:
            for local_target in [LOCAL_VAULT_PATH, LOCAL_SECOND_BRAIN]:
                os.makedirs(os.path.dirname(local_target), exist_ok=True)
                with open(local_target, "a", encoding="utf-8") as target_file:
                    target_file.write(f"\n\n<!-- Pulled via Mac Watchdog -->\n{pulled_content}")
                print(f"[PULL SYNC SUCCESS] Merged remote digest into {local_target}")

            mark_hash_logged(content_hash)

        os.remove("/tmp/buzz-digest-pull.md")

if __name__ == "__main__":
    pull_sync()
