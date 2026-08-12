"""Denz Tools protected loader (Termux/Python 3.14 compatible)."""
from pathlib import Path
import base64, hashlib, hmac

from security.integrity import enforce_release_integrity

enforce_release_integrity()

_S1='8jJ_dDFxqZ2f-99swdytMhmtyOavjDm9g15MPE7BJT4='
_S2='89-LcTIjzJhZimFgCDZ7StdAHVw179lcgAvh_kUrNaA='
_S3='LsjAT8utRAvXnxVofnLwPY3P0rXIaHQWmbDQ78d5xvo='
_S4='Xntm4m-VG0UzpEqfCSlzBpw5rFTxh2FOgFwU7vErxF0='
_PAYLOAD='dashboard.bin'
_AAD='DENZ-TOOLS-DASHBOARD-V3'
_SOURCE='ui/dashboard.py'

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
    root = Path(__file__).resolve().parents[1]
    blob = (root / "protected" / _PAYLOAD).read_bytes()
    shares = [base64.urlsafe_b64decode(x) for x in (_S1, _S2, _S3, _S4)]
    key = bytes(a ^ b ^ c ^ d for a,b,c,d in zip(*shares))
    source = _decrypt(blob, key, _AAD)
    code = compile(source, str(root / _SOURCE), "exec")
    exec(code, globals(), globals())

_load()
del _load, _S1, _S2, _S3, _S4, _PAYLOAD, _AAD, _SOURCE, _decrypt, Path, base64, hashlib, hmac
