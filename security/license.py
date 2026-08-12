"""Online license hook.

The server remains authoritative. No customer license secret is embedded in
this client. A valid authenticated token must be accepted by /license.
"""
from __future__ import annotations

import os
from typing import Any

import requests

API_BASE = os.getenv(
    "API_BASE_URL", "https://api-endpoint-denz.vercel.app/api"
).rstrip("/")


def verify_license(token: str, *, device_id: str = "", username: str = "") -> dict[str, Any]:
    token = str(token or "").strip()
    if not token:
        return {"success": False, "message": "Session token tidak tersedia."}

    headers = {"Authorization": f"Bearer {token}"}
    params = {}
    if device_id:
        params["device_id"] = device_id
    if username:
        params["username"] = username

    try:
        response = requests.get(
            f"{API_BASE}/license",
            headers=headers,
            params=params,
            timeout=10,
        )
        try:
            data = response.json()
        except Exception:
            data = {"success": response.ok, "message": response.text[:300]}
        if not isinstance(data, dict):
            data = {"success": False, "message": "Respons license tidak valid."}
        data.setdefault("success", response.ok)
        return data
    except requests.RequestException as exc:
        return {"success": False, "message": f"License server tidak dapat dihubungi: {exc}"}


def require_license(session: dict[str, Any]) -> dict[str, Any]:
    result = verify_license(
        session.get("token", ""),
        device_id=str(session.get("device_id", "")),
        username=str(session.get("username", "")),
    )
    if not result.get("success"):
        raise RuntimeError(result.get("message") or "License tidak aktif.")
    return result
