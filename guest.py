"""Denz Tools protected loader (Termux/Python 3.14 compatible)."""
from pathlib import Path
import base64, hashlib, hmac

from security.integrity import enforce_release_integrity

enforce_release_integrity()

_S1='NSZznLi5503f3PiNAu3tcsJT63g1Y1GB4zqAlpLK4a8='
_S2='rul4bBDaq6GZVkciUJQL4e4wVrHRgzAjivFX2mH34ZY='
_S3='mZeNkK8FzJOL-2CUAKDkWJQmFeN39gbV_leYE6QLtHY='
_S4='fqsZa9isf-H55kldKnWVz60xLMALcKRmX2bqEH8xluE='
_PAYLOAD='guest.bin'
_AAD='DENZ-TOOLS-GUEST-V3'
_SOURCE='guest.py'

def _decrypt(blob, key, aad):
    nonce, tag, ciphertext = blob[:16], blob[16:48], blob[48:]
    expected = hmac.new(key, aad.encode() + nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        raise RuntimeError("Protected payload authentication failed.")
    out = bytearray()
    counter = 0
    while len(out) < len(ciphertext):
        out.extend(hashlib.sha256(key + nonce + counter.to_bytes(8, "big")).digest())
        counter += 1
    return bytes(a ^ b for a,b in zip(ciphertext, out[:len(ciphertext)]))

def _load():
    root = Path(__file__).resolve().parents[0]
    blob = (root / "protected" / _PAYLOAD).read_bytes()
    shares = [base64.urlsafe_b64decode(x) for x in (_S1, _S2, _S3, _S4)]
    key = bytes(a ^ b ^ c ^ d for a,b,c,d in zip(*shares))
    source = _decrypt(blob, key, _AAD)
    code = compile(source, str(root / _SOURCE), "exec")
    exec(code, globals(), globals())

_load()
del _load, _S1, _S2, _S3, _S4, _PAYLOAD, _AAD, _SOURCE, _decrypt, Path, base64, hashlib, hmac
