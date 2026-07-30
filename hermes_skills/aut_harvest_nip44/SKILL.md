---
name: aut-harvest-nip44
description: Encrypts job review cards and application links using Nostr NIP-44 pairwise encryption before publishing to relays.
author: AutHarvest / Hermes
version: 1.0.0
---

# NIP-44 Encrypted Channel Notification Skill

This Hermes skill secures candidate job search activity by encrypting all channel payload events using Nostr NIP-44 pairwise encryption targeted to the user's private pubkey.

## Security Rules
1. Never publish raw candidate PII (phone, address, email, CV links) in plaintext Nostr events.
2. Encrypt the event content using candidate `pubkey` + agent `nsec`.
3. Publish encrypted `kind: 4` or `kind: 1059` gift-wrap Nostr events to `#job-hunter`.
