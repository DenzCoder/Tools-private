# Release security

- `core.py` is now a small loader; the implementation is stored in `protected/core.bin` encrypted at rest.
- No `.env`, session, device ID, token, or local logs are included in the release.
- Copy `.env.example` to `.env` only when local configuration is needed.
- Authentication and authorization remain server-side.

## Important
This client-side protection is designed to stop casual source inspection and accidental exposure. A determined reverse engineer who can execute the client can eventually analyze runtime code. Keep API secrets and genuinely sensitive business logic on the server.

## GitHub release
Commit the repository after checking `git status` and verifying no secrets are staged. Never commit real `.env` or session files.


## SELLER_PROTECTED

- `security/manifest.json` lists SHA-256 hashes for protected runtime files.
- `security/manifest.sig` authenticates the manifest with Ed25519.
- `security/integrity.py` verifies the signature and hashes before application startup.
- `security/license.py` verifies the logged-in session token against `/license`.
- The Ed25519 private signing key is never included in the customer ZIP or Git repository.

If a customer renames or modifies a protected runtime file, the integrity check detects the missing or changed path.


### Protected modules

`app.py`, `guest.py`, `music_service.py`, and `ui/dashboard.py` in the seller release are small loaders. Their implementation payloads are stored as encrypted files under `protected/`. The license endpoint remains authoritative. Do not place API secrets or the Ed25519 private signing key in this repository.
