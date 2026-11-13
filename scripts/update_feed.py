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
    if not incoming:
        raise RuntimeError("Feed senza eventi: archivio precedente conservato")

    old = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    by_id = {item["id"]: item for item in old.get("items", [])
             if isinstance(item, dict) and item.get("id")}
    for item in incoming:
        by_id[item["id"]] = item

    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    document = {
        "format": "azure-feed-v1",
        "source": SOURCE,
        "latest": timestamp,
        "fetched_at": timestamp,
        "items": sorted(by_id.values(), key=lambda item: item.get("when", ""), reverse=True),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Nuovi nel feed: {len(incoming)}; archivio totale: {len(by_id)}")


if __name__ == "__main__":
    main()
