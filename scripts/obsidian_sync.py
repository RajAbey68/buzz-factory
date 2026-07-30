import os
import datetime

OBSIDIAN_VAULT_PATHS = [
    "/Users/arajiv/Documents/Obsidian Vault/Mama_Obsidian/buzz-digest.md",
    "/Users/arajiv/second-brain/inbox/buzz-digest.md"
]

def append_sync_entry(entry_content):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    date_heading = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    formatted_entry = f"""

## [{date_heading}] Buzz Fleet Synchronization Digest
- **Timestamp:** `{timestamp}`
- **Source Gateway:** `buzz-acp` (`devserver.hostinger` / `wss://ai-integ.communities.buzz.xyz`)
- **System Tags:** `#buzz-fleet` `#obsidian-sync` `#ollama-rag`

### Activity Log
{entry_content}

---
"""
    for path in OBSIDIAN_VAULT_PATHS:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(formatted_entry)
            print(f"Successfully synced to Obsidian Vault: {path}")
        except Exception as e:
            print(f"Warning: Could not write to {path}: {e}")

if __name__ == "__main__":
    sample_log = "All 3 agent fleets (Software, Marketing, AutHarvest) operational. Relay configured to wss://ai-integ.communities.buzz.xyz."
    append_sync_entry(sample_log)
