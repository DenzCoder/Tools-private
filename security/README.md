# SELLER_PROTECTED

This release uses two client-side controls:

- `manifest.json` + `manifest.sig`: signed SHA-256 hashes for runtime files. A missing/renamed or modified required file is detected at startup.
- `license.py`: the authenticated session token is checked against the production `/license` endpoint after login.

The Ed25519 private signing key is **not** shipped in the repository. Keep it offline and use it only when producing a new release.

Client-side integrity checks are tamper-evidence, not an absolute anti-reverse-engineering boundary. Keep API secrets and genuinely sensitive business logic on the server.
