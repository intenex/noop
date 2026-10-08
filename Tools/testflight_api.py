#!/usr/bin/env python3
"""Manual App Store Connect operations; signing keys and tokens never enter logs."""
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature


def bearer_token():
    key_id = os.environ.get("ASC_KEY_ID", "RNUYKTH74C")
    issuer = os.environ.get("ASC_ISSUER_ID", "5b461d34-a054-404e-9fe6-f477ff5669a7")
    key_path = Path(os.environ.get("ASC_KEY_PATH", str(
        Path.home() / ".appstoreconnect/private_keys" / f"AuthKey_{key_id}.p8")))
    encode = lambda data: base64.urlsafe_b64encode(data).decode().rstrip("=")
    now = int(time.time())
    header = encode(json.dumps({"alg": "ES256", "kid": key_id, "typ": "JWT"}).encode())
    payload = encode(json.dumps({"iss": issuer, "iat": now - 30, "exp": now + 600,
                                 "aud": "appstoreconnect-v1"}).encode())
    message = f"{header}.{payload}".encode()
    key = serialization.load_pem_private_key(key_path.read_bytes(), password=None)
    r, s = decode_dss_signature(key.sign(message, ec.ECDSA(hashes.SHA256())))
    return f"{header}.{payload}.{encode(r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))}"


def request(path, method="GET", body=None):
    base = "https://api.appstoreconnect.apple.com/"
    url = path if path.startswith(base) else base + "v1/" + path
    if not url.startswith(base):
        raise ValueError("Only the official Apple API is allowed")
    req = urllib.request.Request(url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + bearer_token(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            return {} if response.status == 204 else json.load(response)
    except urllib.error.HTTPError as error:
        details = json.loads(error.read()).get("errors", [])
        raise RuntimeError(f"Apple API {error.code}: " + "; ".join(
            f"{item.get('code')}: {item.get('detail', item.get('title', ''))}"
            for item in details)) from None


def collection(path):
    rows = []
    for _ in range(20):
        result = request(path)
        rows.extend(result.get("data", []))
        path = result.get("links", {}).get("next")
        if not path:
            return rows
    raise RuntimeError("Apple pagination exceeded the manual operation limit")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--method", default="GET", choices=["GET", "POST", "PATCH"])
    parser.add_argument("--body-file", type=Path)
    args = parser.parse_args()
    body = json.loads(args.body_file.read_text()) if args.body_file else None
    print(json.dumps(request(args.path, args.method, body), indent=2))
