# UI / Bug Fixes

- Fixed the post-login screen: the dashboard now renders the actual feature menu.
- Added responsive two-column feature layout for Termux/Rich.
- Added clearer session/status/quick-help panels.
- Admin Panel (99) is now shown only for authenticated admin sessions.
- Command Palette also hides admin functionality for normal users.
- Dashboard refresh rebuilds the feature map so role changes are reflected.
- Fixed `music_service.py` data path so `data/music_queue.json` stays inside the project.
- Verified `app.py`, `core.py`, `music_service.py`, `guest.py`, and `ui/dashboard.py` compile successfully.
