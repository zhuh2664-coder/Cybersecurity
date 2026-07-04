from __future__ import annotations

import json
import re
from pathlib import Path


SITE_DIR = Path(__file__).resolve().parent
ROOT = SITE_DIR.parent
SOURCE_DIRS = [
    "CCFA",
    "CCFB",
    "CCFC",
    "中科院一区",
    "中科院二区",
    "中科院三区",
    "中科院四区",
]


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(r"^- ([^:：]+)[:：]\s*(.*)$", stripped)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            fields[key] = value
    return fields


def parse_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value.strip())


def parse_deadline_date(value: str) -> str:
    if not value:
        return ""
    value = value.strip()
    patterns = [
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{4}/\d{2}/\d{2})",
        r"(\d{4}\.\d{2}\.\d{2})",
        r"(\d{4}年\d{1,2}月\d{1,2}日)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            date_text = match.group(1)
            date_text = (
                date_text.replace("年", "-")
                .replace("月", "-")
                .replace("日", "")
                .replace("/", "-")
                .replace(".", "-")
            )
            parts = date_text.split("-")
            if len(parts) == 3:
                year, month, day = parts
                return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    return ""


def infer_deadline_kind(fields: dict[str, str]) -> tuple[str, str, str]:
    yearly = clean_text(fields.get("是否全年可投"))
    deadline_text = clean_text(fields.get("固定截稿时间") or fields.get("固定 deadline"))

    combined = f"{yearly} {deadline_text}".lower()
    rolling_markers = [
        "是",
        "滚动投稿",
        "全年可投",
        "no deadline",
        "there is no deadline",
        "未见固定",
        "没有固定",
    ]
    if any(marker in combined for marker in rolling_markers):
        return "rolling", deadline_text or yearly or "全年可投/滚动投稿", ""

    exact_date = parse_deadline_date(deadline_text)
    if exact_date:
        return "fixed", deadline_text, exact_date

    if deadline_text:
        return "textual", deadline_text, ""

    return "unknown", "", ""


def infer_verification_status(text: str, fields: dict[str, str]) -> str:
    short_raw = "来源：" in text and len(text) < 280
    if short_raw:
        return "原始条目"
    if "暂未逐刊统一核查" in text or "本地分区表" in text:
        return "初筛整理"
    if "最后核查日期" in text and "信息来源" in text:
        return "已核查"
    if "最后核查日期" in text:
        return "已细化"
    return "初筛整理"


def categorize_engineering(title: str, text: str) -> str:
    target = f"{title} {text}".upper()
    rules = [
        ("交通运输", ["TRANSPORT", "TRAFFIC", "VEHICLE", "RAIL", "MARITIME", "AIR TRANSPORT", "ITS", "LOGISTICS"]),
        ("能源电力", ["ENERGY", "POWER", "GRID", "BATTERY", "FUEL", "RENEWABLE", "ELECTRIFICATION", "NUCLEAR", "PETROLEUM", "GAS"]),
        ("制造机械", ["MANUFACTUR", "MECHAN", "TRIBO", "WEAR", "VIBRATION", "ADDITIVE", "INDUSTRIAL ENGINEERING", "MECHATRON"]),
        ("土木岩土", ["BUILDING", "CONSTRUCTION", "STRUCTURE", "GEOTECH", "EARTHQUAKE", "SOIL", "ROCK", "STEEL", "WIND ENGINEERING", "GEOENVIRONMENT"]),
        ("电子芯片", ["ELECTRON", "DEVICE", "VLSI", "SEMICONDUCT", "QUANTUM ELECTRON", "LIGHTWAVE", "MICROWAVE", "TERAHERTZ", "OPTICS", "LASER", "SENSOR", "MEASUREMENT", "CIRCUIT"]),
        ("流体热工", ["FLUID", "HEAT", "THERMAL", "THERMODYNAM", "MULTIPHASE", "AERODYNAM", "OCEAN"]),
        ("材料化工", ["CHEMICAL", "DESALINATION", "MEMBRANE", "CO2", "POWDER", "MATERIAL", "SEPARATION", "FRACTURE", "CORROSION"]),
        ("安全管理", ["SAFETY", "RISK", "MANAGEMENT", "ERGONOMICS", "QUALITY", "TECHNOMETRICS", "RELIABILITY"]),
    ]
    for label, keywords in rules:
        if any(keyword in target for keyword in keywords):
            return label
    return "综合工程"


def categorize_computing(title: str, text: str) -> str:
    target = f"{title} {text}".upper()
    rules = [
        ("网络与通信", ["NETWORK", "COMMUNICATION", "WIRELESS", "MOBILE", "INTERNET", "ROUTING"]),
        ("网络安全", ["SECURITY", "PRIVACY", "FORENSIC", "CRYPTO", "TRUST", "DEPENDABLE"]),
        ("人工智能", ["NEURAL", "PATTERN", "MACHINE LEARNING", "INTELLIGEN", "FUZZY", "CYBERNETICS", "EVOLUTIONARY", "VISION"]),
        ("软件系统", ["SOFTWARE", "PROGRAM", "LANGUAGE", "SYSTEM", "TESTING", "REQUIREMENTS"]),
        ("数据智能", ["DATA", "DATABASE", "RETRIEVAL", "KNOWLEDGE", "INFORMATION SYSTEM", "BIG DATA"]),
        ("图形多媒体", ["GRAPHICS", "IMAGE", "MULTIMEDIA", "ROBOT", "HUMAN-COMPUTER", "INTERACTION"]),
    ]
    for label, keywords in rules:
        if any(keyword in target for keyword in keywords):
            return label
    return "综合计算机"


def infer_direction(source_root: str, rel_parts: list[str], title: str, text: str, fields: dict[str, str]) -> str:
    if source_root.startswith("CCF"):
        return rel_parts[1] if len(rel_parts) > 1 else "未分类"

    subject = rel_parts[1] if len(rel_parts) > 1 else clean_text(fields.get("学科方向")) or "未分类"
    if subject == "工程技术":
        return categorize_engineering(title, text)
    if subject == "计算机科学":
        return categorize_computing(title, text)
    return subject


def extract_entry(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    title = parse_title(text, path.stem)
    fields = parse_fields(text)
    top = path.parts[0]
    rel_parts = list(path.parts)
    source_system = "CCF" if top.startswith("CCF") else "中科院"
    rank = top
    subject = rel_parts[1] if len(rel_parts) > 1 else clean_text(fields.get("学科方向")) or ""
    direction = infer_direction(top, rel_parts, title, text, fields)

    deadline_kind, deadline_text, deadline_date = infer_deadline_kind(fields)
    verification_status = infer_verification_status(text, fields)

    official_url = clean_text(fields.get("官网") or fields.get("期刊主页") or fields.get("主页"))
    submission_url = clean_text(fields.get("投稿入口"))
    publication_type = clean_text(fields.get("刊物类型")) or "期刊"
    issn = clean_text(fields.get("ISSN"))
    oa = clean_text(fields.get("是否 OA"))
    difficulty = clean_text(fields.get("投稿难度判断"))
    review = clean_text(fields.get("是否 Review") or fields.get("Review"))
    checked_at = clean_text(fields.get("最后核查日期"))

    search_blob = " ".join(
        filter(
            None,
            [
                title,
                source_system,
                rank,
                subject,
                direction,
                issn,
                oa,
                difficulty,
                review,
                fields.get("更适合什么样的论文", ""),
                fields.get("领域", ""),
            ],
        )
    )

    return {
        "title": title,
        "sourceSystem": source_system,
        "rank": rank,
        "subject": subject,
        "direction": direction,
        "publicationType": publication_type,
        "deadlineKind": deadline_kind,
        "deadlineText": deadline_text,
        "deadlineDate": deadline_date,
        "officialUrl": official_url,
        "submissionUrl": submission_url,
        "issn": issn,
        "oa": oa,
        "difficulty": difficulty,
        "review": review,
        "verificationStatus": verification_status,
        "checkedAt": checked_at,
        "relativePath": path.as_posix(),
        "searchBlob": search_blob.lower(),
    }


def main() -> None:
    entries: list[dict[str, object]] = []
    for root_name in SOURCE_DIRS:
        root = ROOT / root_name
        for path in sorted(root.rglob("*.md")):
            if path.name == "核查进度.md":
                continue
            entries.append(extract_entry(path.relative_to(ROOT)))

    entries.sort(key=lambda item: (item["sourceSystem"], item["rank"], item["direction"], item["title"]))
    payload = "window.JOURNAL_DATA = " + json.dumps(entries, ensure_ascii=False, indent=2) + ";\n"
    (SITE_DIR / "data.js").write_text(payload, encoding="utf-8")
    print(f"Generated {len(entries)} entries -> {SITE_DIR / 'data.js'}")


if __name__ == "__main__":
    main()
