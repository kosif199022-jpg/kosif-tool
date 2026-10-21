#!/usr/bin/env python3
"""Shared credential detector for KOSIF writers (FusionForge and any script that persists free text).

  find_secrets(text)        -> list of pattern names found in text (never the matched values)
  refuse_secrets(**fields)  -> raises SecretError naming the field and the kinds, never the value
  scan_object(obj)          -> [(json_path, [kinds])] for every string (and key, and "key: value" pair) inside a
                               JSON-like object

It is a detector, not a vault: it catches common token formats and key/value credential assignments (plain,
quoted JSON/YAML/Python, CLI flags, Arabic labels) so they are not written to disk. Values that only reference a
secret ($VAR, ${VAR}, %VAR%, <placeholder>, {{template}}) or are paths are not flagged. It cannot prove that a
text is secret-free. Python stdlib only.
"""
from __future__ import annotations

import re

_STRONG_KEYS = (r"api[_-]?key|apikey|access[_-]?key|account[_-]?key|secret[_-]?key|client[_-]?secret|private[_-]?key"
                r"|auth[_-]?token|access[_-]?token|refresh[_-]?token|bearer[_-]?token|session[_-]?token|passw(?:or)?d|pwd|passphrase")
_WEAK_KEYS = r"secret|token"  # ordinary English words: their value must also look like a credential
_ASSIGN_KEYS = _STRONG_KEYS + "|" + _WEAK_KEYS

# (name, pattern) — ordered from specific formats to the generic assignment rules
PATTERNS = (
    ("anthropic_api_key", r"(?<![A-Za-z0-9])sk-ant-[A-Za-z0-9_-]{16,}"),
    ("openai_api_key", r"(?<![A-Za-z0-9_-])sk-(?:proj-|svcacct-|admin-)?(?=[A-Za-z0-9_-]*[0-9])(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{20,}"),
    ("aws_access_key_id", r"(?<![A-Z0-9])(?:AKIA|ASIA|AGPA|AIDA|AROA|ANPA|ANVA|AIPA)[0-9A-Z]{16}(?![A-Z0-9])"),
    ("aws_secret_access_key", r"(?i)aws_?secret_?access_?key[\"']?\s*[=:]\s*[\"']?[A-Za-z0-9/+=]{16,}"),
    ("github_token", r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{20,}"),
    ("github_fine_grained_pat", r"github_pat_[A-Za-z0-9_]{20,}"),
    ("gitlab_token", r"(?<![A-Za-z0-9])glpat-[A-Za-z0-9_-]{20,}"),
    ("google_api_key", r"AIza[0-9A-Za-z_-]{30,}"),
    ("google_oauth_client_secret", r"(?<![A-Za-z0-9])GOCSPX-[A-Za-z0-9_-]{20,}"),
    ("google_oauth_access_token", r"(?<![A-Za-z0-9])ya29\.[A-Za-z0-9_-]{20,}"),
    ("slack_token", r"(?<![A-Za-z0-9])(?:xox[abposre]-[A-Za-z0-9-]{10,}|xapp-[0-9]+-[A-Za-z0-9-]{10,})"),
    ("slack_webhook", r"hooks\.slack\.com/services/[A-Za-z0-9/_-]{20,}"),
    ("stripe_secret_key", r"(?<![A-Za-z0-9])[sr]k_(?:live|test)_[0-9A-Za-z]{16,}"),
    ("huggingface_token", r"(?<![A-Za-z0-9])hf_[A-Za-z0-9]{30,}"),
    ("npm_token", r"(?<![A-Za-z0-9])npm_[A-Za-z0-9]{36}"),
    ("pypi_token", r"(?<![A-Za-z0-9])pypi-[A-Za-z0-9_-]{40,}"),
    ("digitalocean_token", r"(?<![A-Za-z0-9])do[opr]_v1_[A-Za-z0-9]{32,}"),
    ("shopify_token", r"(?<![A-Za-z0-9])shp(?:at|ca|pa|ss)_[A-Fa-f0-9]{24,}"),
    ("mailgun_key", r"(?<![A-Za-z0-9])key-[0-9a-f]{32}(?![0-9a-f])"),
    ("twilio_api_key", r"(?<![A-Za-z0-9])SK[0-9a-f]{32}(?![0-9A-Za-z])"),
    ("discord_bot_token", r"(?<![A-Za-z0-9])[MN][A-Za-z0-9]{23,27}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27,}"),
    ("mysql_password_flag", r"\bmysql(?:dump|admin)?\b[^\n]*?\s-p(?![\s$<{%])\S{4,}"),
    ("sendgrid_key", r"(?<![A-Za-z0-9])SG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}"),
    ("telegram_bot_token", r"(?<![0-9])[0-9]{8,10}:[A-Za-z0-9_-]{35}(?![A-Za-z0-9_-])"),
    ("bearer_token", r"(?i)\bbearer\s+(?=[A-Za-z0-9._~+/=-]*[0-9._~+/=-])[A-Za-z0-9._~+/=-]{12,}"),
    ("basic_auth_header", r"(?i)\b(?:proxy-)?authorization[\"']?\s*[:=]\s*[\"']?(?:basic|digest)\s+[A-Za-z0-9+/._~-]{8,}=*"
                          r"|\bBasic\s+(?=[A-Za-z0-9+/]*[0-9+/=])[A-Za-z0-9+/]{12,}={0,2}(?![A-Za-z0-9+/=])"),
    ("jwt", r"(?<![A-Za-z0-9_-])eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    ("private_key_block", r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY[A-Z ]*-----"),
    ("url_credentials", r"(?i)\b[a-z][a-z0-9+.-]*://[^\s:/@]*:[^\s/@]+@"),
)
# generic rules: the value group is checked by _plausible before a hit counts
_ASSIGN_RX = re.compile(r"(?i)(?<![A-Za-z0-9])[\"']?(" + _ASSIGN_KEYS + r")[\"']?\s*[=:]\s*[\"']?([^\s\"',;]+)")
_FLAG_RX = re.compile(r"(?i)(?<![\w-])--?(password|passwd|pass|pwd|passphrase|token|auth-token|access-token|api-key|apikey|secret"
                      r"|client-secret|secret-key)(?:\s+|=)[\"']?([^\s\"']+)")
_ARABIC_RX = re.compile(r"(كلمة\s*(?:ال)?(?:مرور|سر)|كلمه\s*(?:ال)?(?:مرور|سر)|الرقم\s*السري|الرمز\s*السري|رمز\s*(?:ال)?(?:دخول|وصول|تحقق)"
                        r"|مفتاح\s*(?:ال)?(?:api|API|وصول|سري|الواجهة))\s*[:=：]\s*[\"'«]?([^\s\"'»]+)")
_COMPILED = tuple((name, re.compile(rx)) for name, rx in PATTERNS)
_ANY = re.compile("|".join(f"(?i:{rx[4:]})" if rx.startswith("(?i)") else f"(?:{rx})" for _name, rx in PATTERNS))  # one-pass prefilter
_KEY_HINT = re.compile(r"(?i)" + _ASSIGN_KEYS)
_REFERENCE = re.compile(r"[$%<{\[(/~]|\.{0,2}/|\*+$|x{4,}$|X{4,}$")
_WEAK = re.compile(_WEAK_KEYS, re.I)
_PROSE = {"required", "optional", "missing", "invalid", "incorrect", "expired", "changed", "protected", "redacted", "removed",
          "provided", "hidden", "masked", "needed", "rotated", "revoked", "placeholder", "example", "unknown", "configured"}


class SecretError(ValueError):
    """A field looks like it holds a credential; the message names the field and kinds, never the value."""

    def __init__(self, field: str, kinds):
        self.field = field
        self.kinds = list(kinds)
        super().__init__(f"field '{field}' looks like it contains a credential ({', '.join(self.kinds)}); "
                         "remove it and reference the secret by name instead (e.g. $API_KEY) — nothing was written")


def _plausible(key: str, value: str) -> bool:
    """True when value could be a real credential rather than a reference, a placeholder, a path or prose."""
    v = value.rstrip(".,;:)]}>")
    if len(v) < 6 or _REFERENCE.match(v) or set(v) <= set("*xX.-_#") or v.lower() in _PROSE:
        return False
    if _WEAK.fullmatch(key or ""):  # 'token: 128000', 'token: lifecycle', 'secret: manager' are prose
        has_mix = bool(re.search(r"[0-9]", v)) and bool(re.search(r"[A-Za-z]", v))
        return (has_mix and len(v) >= 8) or (len(v) >= 20 and bool(re.fullmatch(r"[A-Za-z0-9_+/=.-]+", v)) and not v.isalpha())
    return True


def find_secrets(text) -> list:
    """Names of the credential patterns present in text (empty list when none)."""
    if text is None:
        return []
    s = text if isinstance(text, str) else str(text)
    found = [name for name, rx in _COMPILED if rx.search(s)] if _ANY.search(s) else []
    if any(_plausible(m.group(1), m.group(2)) for m in _ASSIGN_RX.finditer(s)):
        found.append("credential_assignment")
    if any(_plausible(m.group(1).replace("-", "_"), m.group(2)) for m in _FLAG_RX.finditer(s)):
        found.append("credential_cli_flag")
    if any(_plausible("password", m.group(2)) for m in _ARABIC_RX.finditer(s)):
        found.append("credential_assignment_ar")
    return found


def _strings(value):
    if value is None:
        return
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield str(k)
            yield from _strings(v)
            if isinstance(v, (str, int, float)) and not isinstance(v, bool) and _KEY_HINT.search(str(k)):
                yield f'"{k}": "{v}"'
    elif isinstance(value, (list, tuple, set)):
        for v in value:
            yield from _strings(v)
    else:
        yield str(value)


def refuse_secrets(**fields) -> None:
    """Raise SecretError for the first field (in the given order) whose text looks like a credential."""
    for field, value in fields.items():
        kinds = []
        for s in _strings(value):
            kinds += [k for k in find_secrets(s) if k not in kinds]
        if kinds:
            raise SecretError(field, kinds)


def scan_object(obj, path: str = "$") -> list:
    """[(json_path, kinds)] for every string value, key, or "key": "value" pair in a nested JSON-like object."""
    hits = []
    if isinstance(obj, dict):
        for k in sorted(obj, key=str):
            kk = find_secrets(str(k))
            if kk:
                hits.append((f"{path}.<key>", kk))
            v = obj[k]
            sub = scan_object(v, f"{path}.{k}")
            if isinstance(v, (str, int, float)) and not isinstance(v, bool) and _KEY_HINT.search(str(k)):
                pair = [x for x in find_secrets(f'"{k}": "{v}"') if not any(x in kinds for _p, kinds in sub)]
                if pair:
                    sub.append((f"{path}.{k}", pair))
            hits += sub
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            hits += scan_object(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        kk = find_secrets(obj)
        if kk:
            hits.append((path, kk))
    return hits


if __name__ == "__main__":  # tiny CLI: read stdin, print the kinds found (exit 1 when any)
    import sys
    found = find_secrets(sys.stdin.read())
    print(", ".join(found) if found else "no credential patterns found")
    raise SystemExit(1 if found else 0)
