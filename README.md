# Denz Tools

Animated Rich terminal toolkit for Termux/Android.

## Install

```bash
git clone <repository-url>
cd denz-tools
python -m pip install -r requirements.txt
python app.py
```

For Termux music playback:

```bash
pkg update
pkg install python mpv
pip install -r requirements.txt
```

## Authentication

The API response is authoritative for username, role, status, and token.
The Admin Panel (`99`) is shown only when the server-authenticated role is `admin`.

## Features

01 Bind Info
02 Bind Email
03 Unbind
04 Change Bind
05 Cancel Request
06 EAT → Token
07 Revoke Token
08 Bound Accounts
09 AmPrem
10 Owner Details
11 Update Bio
12 Ban Status (UID)
13 Music Queue
14 Guest Generator
15 YouTube
16 GPT-5 AI
17 DeepSeek AI
99 Admin Panel (admin)

## Security

Never commit session files, tokens, passwords, API secrets, `.env`, cache, or logs.


## License API
The client has no public registration. Accounts are created by the admin. Before release, set `API_BASE_URL` in `app.py` to your deployed Vercel API URL (or provide it through the environment).

## Admin Manager Upgrade

The `ui/dashboard.py` module provides an admin-only manager for the existing VIP API.

Run:

```bash
python -m ui.dashboard
```

Optional API URL:

```bash
export VIP_API_URL=https://api-endpoint-denz.vercel.app
```

Admin operations use the existing API endpoints:
- `/api/auth`
- `/api/admin/stats`
- `/api/admin/users`
- `/api/admin/extend`
- `/api/admin/reset-device`
- `/api/admin/status`
- `/api/admin/delete`
- `/api/admin/activity`

No customer self-management UI is added.

## SELLER_PROTECTED

This release includes startup integrity verification and a remote license hook. Required files are listed in `security/manifest.json`; missing/renamed or modified files cause startup to stop.

For production, set `SELLER_LICENSE_REQUIRED=1`, `LICENSE_API_URL`, and `LICENSE_KEY` in the deployment environment. Do not commit `.env` or customer license keys to GitHub.


## Seller Protected Release

This release separates the public client launchers from encrypted implementation payloads under `protected/`.
The client still performs signed-manifest integrity checks and authenticated server-side license verification.
The encrypted payloads are intended to deter casual source inspection; they are not a cryptographic guarantee against runtime reverse engineering on an end-user device.

### GitHub distribution

Commit the release files except private signing material. Keep the Ed25519 private signing key offline.
Customers can clone the repository, install requirements, and run `python app.py`; an active server license is required after authentication.


## Termux V3
Runtime protection uses Python standard-library SHA-256/HMAC primitives, so the protected loader no longer requires `cryptography`, Rust, or maturin on the customer device. Ed25519 manifest verification is implemented in pure Python. This is packaging/obfuscation, not absolute anti-reverse-engineering protection; keep secrets and sensitive business logic server-side.
