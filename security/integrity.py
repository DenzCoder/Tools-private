"""Pure-Python signed release integrity verifier (no native dependencies)."""
from __future__ import annotations
import base64, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "security" / "manifest.json"
SIGNATURE = ROOT / "security" / "manifest.sig"
PUBLIC_KEY_B64 = "6Er8KuegATAe9mQxD47VOF+hIUXjtDDFFTvpz/s+U7Q="

_Q = 2**255 - 19
_L = 2**252 + 27742317777372353535851937790883648493
_D = (-121665 * pow(121666, _Q-2, _Q)) % _Q
_I = pow(2, (_Q-1)//4, _Q)

def _inv(x): return pow(x, _Q-2, _Q)

def _xrecover(y):
    xx = (y*y - 1) * _inv(_D*y*y + 1) % _Q
    x = pow(xx, (_Q+3)//8, _Q)
    if (x*x - xx) % _Q != 0:
        x = x * _I % _Q
    if x & 1:
        x = _Q - x
    return x

def _edwards_add(P, Q):
    x1,y1=P; x2,y2=Q
    denx = _inv((1 + _D*x1*x2*y1*y2) % _Q)
    deny = _inv((1 - _D*x1*x2*y1*y2) % _Q)
    return ((x1*y2+y1*x2)*denx % _Q, (y1*y2+x1*x2)*deny % _Q)

def _scalarmult(P, e):
    R=(0,1)
    while e:
        if e & 1: R=_edwards_add(R,P)
        P=_edwards_add(P,P)
        e >>= 1
    return R

def _decodepoint(s):
    if len(s) != 32: raise ValueError("bad point length")
    y = int.from_bytes(s, "little") & ((1<<255)-1)
    sign = s[31] >> 7
    if y >= _Q: raise ValueError("bad point")
    x = _xrecover(y)
    if (x & 1) != sign: x = _Q-x
    P=(x,y)
    # Edwards curve check: -x² + y² = 1 + d x² y²
    if (-x*x + y*y - 1 - _D*x*x*y*y) % _Q:
        raise ValueError("invalid point")
    return P

_By = 4 * _inv(5) % _Q
_B = (_xrecover(_By), _By)

def _verify_ed25519(public_key, signature, message):
    if len(public_key) != 32 or len(signature) != 64: return False
    try:
        A = _decodepoint(public_key)
        R = _decodepoint(signature[:32])
        S = int.from_bytes(signature[32:], "little")
        if S >= _L: return False
        h = int.from_bytes(hashlib.sha512(signature[:32] + public_key + message).digest(), "little") % _L
        SB = _scalarmult(_B, S)
        Rp = _edwards_add(R, _scalarmult(A, h))
        return SB == Rp
    except Exception:
        return False

def _canonical_manifest(data: dict) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def _fail(message):
    raise RuntimeError(f"Release integrity check failed: {message}")

def verify_manifest(*, strict=True):
    if not MANIFEST.is_file() or not SIGNATURE.is_file():
        if strict: _fail("manifest or signature is missing")
        return False
    try:
        manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
        sig=base64.b64decode(SIGNATURE.read_text(encoding="ascii").strip())
        pub=base64.b64decode(PUBLIC_KEY_B64)
        if not _verify_ed25519(pub, sig, _canonical_manifest(manifest)):
            raise ValueError("invalid manifest signature")
    except Exception as exc:
        if strict: _fail(str(exc))
        return False
    expected=manifest.get("files")
    if not isinstance(expected,dict) or not expected:
        if strict: _fail("manifest contains no file entries")
        return False
    for relative, expected_hash in expected.items():
        path=ROOT/relative
        if not path.is_file():
            if strict: _fail(f"required file missing: {relative}")
            return False
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected_hash:
            if strict: _fail(f"file changed or renamed: {relative}")
            return False
    return True

def enforce_release_integrity():
    verify_manifest(strict=True)
