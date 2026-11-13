#!/usr/bin/env python3
"""Archive Microsoft's PUBLIC Azure Status RSS feed as a static JSON document.

No Azure credentials, internal metrics or customer data are used.
"""
import datetime as dt
import email.utils
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
try:
    from scripts.history import HISTORY_URL, parse_history
except ModuleNotFoundError:
    # Running as `python scripts/update_feed.py` places scripts/ on sys.path.
    from history import HISTORY_URL, parse_history

SOURCE = "https://rssfeed.azure.status.microsoft/en-us/status/feed/"
OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "azure-feed.json"


def tag_text(node, name):
    for child in node:
        if child.tag.split("}")[-1].lower() == name.lower():
            return (child.text or "").strip()
    return ""


def plain(value):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", value or ""))).strip()


def parse_date(value):
    try:
        date = email.utils.parsedate_to_datetime(value)
        return date.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    except (TypeError, ValueError, OverflowError):
        return ""


def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    root_name = root.tag.split("}")[-1].lower()
    if root_name not in ("rss", "rdf", "feed"):
        raise RuntimeError(f"Formato XML inatteso: {root_name}")
    entries = []
    for node in root.iter():
        if node.tag.split("}")[-1].lower() != "item":
            continue
        title = tag_text(node, "title") or "Evento Azure"
        description = plain(tag_text(node, "description") or tag_text(node, "summary"))[:7000]
        published = tag_text(node, "pubDate")
        link = tag_text(node, "link")
        guid = tag_text(node, "guid") or link or (title + "|" + published)
        scope = (title + " " + description).lower()
        entries.append({
            "id": guid,
            "title": title,
            "description": description,
            "link": link if link.startswith("https://") else "",
            "when": parse_date(published),
            "italy": bool(re.search(r"\bitaly north\b|\bitalynorth\b", scope)),
            "germany": bool(re.search(r"\bgermany west central\b|\bgermanywestcentral\b|\bfrankfurt\b|\bfrancoforte\b", scope)),
            "source": "Azure Status RSS (pubblico)",
        })
    return entries


def main():
    request = urllib.request.Request(
        SOURCE,
        headers={"Accept": "application/rss+xml,application/xml,text/xml",
                 "User-Agent": "MulticloudMonitor/1.0 (public Azure status reader)"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"Azure RSS HTTP {response.status}")
        xml_bytes = response.read(8_000_000)

    incoming = parse_feed(xml_bytes)
    # Un feed RSS valido puo essere vuoto: non e un errore e non cancella lo storico.

    old = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    # History acquisition is independent: never discard a successful RSS read.
    historic = []
    history_status = "ok"
    try:
        history_req = urllib.request.Request(
            HISTORY_URL, headers={"User-Agent": "MulticloudMonitor/1.0 (public Azure PIR reader)"})
        with urllib.request.urlopen(history_req, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError(f"Azure history HTTP {response.status}")
            historic = parse_history(response.read(12_000_000))
        if not historic:
            history_status = "no_pirs_extracted"
            print("WARNING: No PIRs extracted from history page; retaining archived data.")
    except Exception as exc:
        history_status = "fetch_error"
        print(f"WARNING: History acquisition failed ({type(exc).__name__}): {exc}")

    by_id = {item["id"]: item for item in old.get("items", [])
             if isinstance(item, dict) and item.get("id")}

    # Backfill selected *publicly identified* PIRs by their Microsoft Tracking ID.
    # Microsoft serves each historical PIR at /status/history/?trackingId=...
    seed_file = OUTPUT.parent / "azure-history-seeds.json"
    seeds = json.loads(seed_file.read_text(encoding="utf-8"))["tracking_ids"] if seed_file.exists() else []
    seed_imported = 0
    seed_failures = 0
    known_ids = set(by_id) | {item["id"] for item in historic}
    for tracking in seeds[:25]:
        key = "pir:" + tracking.upper()
        if key in known_ids:
            continue
        if not __import__("re").fullmatch(r"[A-Z0-9_]{3,}-[A-Z0-9_]{2,}", tracking, __import__("re").I):
            seed_failures += 1
            continue
        from urllib.parse import quote
        link = HISTORY_URL + "/?trackingId=" + quote(tracking, safe="")
        try:
            request = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                parsed = parse_history(response.read(1500000))
            matching = [item for item in parsed if item["id"].upper() == key.upper()]
            if len(matching) != 1:
                raise RuntimeError("Tracking ID not uniquely present in official response")
            historic.append(matching[0])
            known_ids.add(key)
            seed_imported += 1
        except Exception as exc:
            seed_failures += 1
            print(f"WARNING: historical seed {tracking}: {type(exc).__name__}: {exc}")
    for item in incoming + historic:
        by_id[item["id"]] = item

    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    document = {
        "format": "azure-feed-v1",
        "source": SOURCE,
        "latest": timestamp,
        "fetched_at": timestamp,
        "latest_feed_count": len(incoming),
        "feed_status": "ok_empty" if not incoming else "ok",
        "history_status": history_status,
        "history_latest_count": len(historic),
        "history_source": HISTORY_URL,
        "history_seed_imported": seed_imported,
        "history_seed_failures": seed_failures,
        "history_seed_total": len(seeds),
        "items": sorted(by_id.values(), key=lambda item: item.get("when", ""), reverse=True),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"RSS: {len(incoming)}; PIRs: {len(historic)}; seeds added: {seed_imported}; seed failures: {seed_failures}; history status: {history_status}; total: {len(by_id)}")


if __name__ == "__main__":
    main()
