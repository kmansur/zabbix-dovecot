#!/usr/bin/env python3
"""Static and cross-version validation for Dovecot Zabbix template exports."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "7.0": ROOT / "templates" / "7.0" / "dovecot-by-zabbix-agent.yaml",
    "8.0": ROOT / "templates" / "8.0" / "dovecot-by-zabbix-agent.yaml",
}

EXPECTED_TEMPLATE_UUID = "a46637264254413e838cc95b1cacb91d"
EXPECTED_TEMPLATE_NAME = "Dovecot by Zabbix agent"
EXPECTED_VENDOR = "Net Tech"
EXPECTED_VERSION = "3.0.0"
UUIDV4_RE = re.compile(r"^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}$")

EXPECTED_KEYS = {
    "dovecot.stats",
    "dovecot.collector.available",
    "dovecot.collector.error",
    "dovecot.collector.version",
    "dovecot.connections.imap",
    "dovecot.connections.pop3",
    "dovecot.connections.total",
    "dovecot.connections.users",
    "dovecot.connections.max_per_user",
    "dovecot.version",
    "proc.num[{$DOVECOT.PROCESS.NAME}]",
    "net.tcp.service[imap,,{$DOVECOT.IMAP.PORT}]",
    "net.tcp.service[tcp,,{$DOVECOT.IMAPS.PORT}]",
    "net.tcp.service[pop,,{$DOVECOT.POP3.PORT}]",
    "net.tcp.service[tcp,,{$DOVECOT.POP3S.PORT}]",
    "net.tcp.service.perf[imap,,{$DOVECOT.IMAP.PORT}]",
    "net.tcp.service.perf[tcp,,{$DOVECOT.IMAPS.PORT}]",
    "net.tcp.service.perf[pop,,{$DOVECOT.POP3.PORT}]",
    "net.tcp.service.perf[tcp,,{$DOVECOT.POP3S.PORT}]",
    "vfs.file.cksum[{$DOVECOT.CONF.FILE}]",
    "vfs.file.cksum[{$DOVECOT.SQL.CONF.FILE}]",
}


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def load_template(path: Path, export_version: str) -> tuple[dict, dict, str]:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)

    assert data["zabbix_export"]["version"] == export_version, (
        f"{path}: export version mismatch"
    )

    templates = data["zabbix_export"].get("templates", [])
    assert len(templates) == 1, f"{path}: expected exactly one template"
    template = templates[0]

    assert template.get("uuid") == EXPECTED_TEMPLATE_UUID, (
        f"{path}: template UUID changed unexpectedly"
    )
    assert template.get("template") == EXPECTED_TEMPLATE_NAME, (
        f"{path}: technical template name is not standardized"
    )
    assert template.get("name") == EXPECTED_TEMPLATE_NAME, (
        f"{path}: visible template name is not standardized"
    )

    vendor = template.get("vendor", {})
    assert vendor.get("name") == EXPECTED_VENDOR, f"{path}: vendor name mismatch"
    assert str(vendor.get("version")) == EXPECTED_VERSION, (
        f"{path}: vendor version mismatch"
    )

    assert not re.search(r"Template App\s+Dovecot", text), (
        f"{path}: legacy template name remains"
    )

    keys = {
        obj["key"]
        for obj in walk(template)
        if isinstance(obj, dict) and isinstance(obj.get("key"), str)
    }
    missing_keys = EXPECTED_KEYS - keys
    assert not missing_keys, f"{path}: missing keys: {sorted(missing_keys)}"

    uuids = [
        obj["uuid"].lower()
        for obj in walk(data)
        if isinstance(obj, dict) and isinstance(obj.get("uuid"), str)
    ]
    duplicates = sorted({uuid for uuid in uuids if uuids.count(uuid) > 1})
    assert not duplicates, f"{path}: duplicate UUIDs: {duplicates}"

    invalid_uuidv4 = sorted(uuid for uuid in uuids if not UUIDV4_RE.fullmatch(uuid))
    assert not invalid_uuidv4, f"{path}: invalid UUIDv4 values: {invalid_uuidv4}"

    defined_macros = {
        macro["macro"]
        for macro in template.get("macros", [])
        if isinstance(macro, dict) and "macro" in macro
    }
    referenced_macros = set(re.findall(r"\{\$[A-Z0-9_.]+\}", text))
    missing_macros = referenced_macros - defined_macros
    assert not missing_macros, f"{path}: undefined macros: {sorted(missing_macros)}"

    assert "net.tcp.service[tcp,,{$DOVECOT.IMAP.PORT}]" not in text, (
        f"{path}: IMAP must use protocol-aware service check"
    )
    assert "net.tcp.service[tcp,,{$DOVECOT.POP3.PORT}]" not in text, (
        f"{path}: POP3 must use protocol-aware service check"
    )

    return data, template, text


def item_uuid_by_key(template: dict) -> dict[str, str]:
    result = {}
    for obj in walk(template):
        if (
            isinstance(obj, dict)
            and isinstance(obj.get("key"), str)
            and isinstance(obj.get("uuid"), str)
        ):
            result[obj["key"]] = obj["uuid"]
    return result


def macro_values(template: dict) -> dict[str, str]:
    return {
        macro["macro"]: str(macro.get("value", ""))
        for macro in template.get("macros", [])
        if isinstance(macro, dict) and isinstance(macro.get("macro"), str)
    }


def named_uuid_set(data: dict) -> set[tuple[str, str]]:
    result = set()
    for obj in walk(data):
        if (
            isinstance(obj, dict)
            and isinstance(obj.get("uuid"), str)
            and isinstance(obj.get("name"), str)
        ):
            result.add((obj["name"], obj["uuid"]))
    return result


def validate_cross_version(
    data7: dict, template7: dict, data8: dict, template8: dict
) -> None:
    items7 = item_uuid_by_key(template7)
    items8 = item_uuid_by_key(template8)
    assert items7 == items8, "7.0/8.0 item key-to-UUID mapping differs"

    macros7 = macro_values(template7)
    macros8 = macro_values(template8)
    assert macros7 == macros8, "7.0/8.0 macro names/default values differ"

    named7 = named_uuid_set(data7)
    named8 = named_uuid_set(data8)
    only7 = sorted(named7 - named8)
    only8 = sorted(named8 - named7)
    assert not only7 and not only8, (
        "7.0/8.0 named UUID objects differ: "
        f"only7={only7[:10]} only8={only8[:10]}"
    )


def main() -> int:
    loaded = {}
    for version, path in TEMPLATES.items():
        loaded[version] = load_template(path, version)
        print(f"OK: {path.relative_to(ROOT)}")

    data7, template7, _ = loaded["7.0"]
    data8, template8, _ = loaded["8.0"]
    validate_cross_version(data7, template7, data8, template8)
    print("OK: Zabbix 7.0/8.0 semantic parity")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
