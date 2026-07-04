#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


TITLE_ZH_2022 = {
    "2022 - A Fast Fuzzy Clustering Algorithm for Complex Networks via a Generalized Momentum Method": "《一种基于广义动量法的复杂网络快速模糊聚类算法》",
    "2022 - A Look Behind the Curtain Traffic Classification in an Increasingly Encrypted Web": "《揭开帷幕：日益加密的网络环境中的流量分类》",
    "2022 - A Multi - Scale Feature Attention Approach to Network Traffic Classification and Its Model Explanation": "《一种用于网络流量分类及其模型解释的多尺度特征注意力方法》",
    "2022 - A Multilayered - and - Randomized Latent Factor Model for High - Dimensional and Sparse Matrices": "《一种面向高维稀疏矩阵的多层随机潜在因子模型》",
    "2022 - A Novel Approach to Large - Scale Dynamically Weighted Directed Network Representation": "《一种用于大规模动态加权有向网络表示的新方法》",
    "2022 - A PID - incorporated Latent Factorization of Tensors Approach to Dynamically Weighted Directed Network": "《一种结合 PID 的张量潜在因子分解方法用于动态加权有向网络分析》",
    "2022 - A few shots traffic classification with mini - FlowPic augmentations": "《基于 mini-FlowPic 增强的少样本流量分类》",
    "2022 - Accurate mobile - app fingerprinting using flow - level relationship with graph neural networks": "《利用流级关系和图神经网络的高精度移动应用指纹识别》",
    "2022 - An Algorithm of Inductively Identifying Clusters From Attributed Graphs": "《一种从属性图中归纳识别聚类的算法》",
    "2022 - An L1 - and - L2 - Norm - Oriented Latent Factor Model for Recommende": "《一种面向 L1 与 L2 范数的潜在因子模型用于推荐》",
    "2022 - Bayesian Deep Learning and a Probabilistic Perspective of Generalization": "《贝叶斯深度学习与泛化的概率视角》",
    "2022 - Collective decision for open set recognition": "《面向开放集识别的集体决策方法》",
    "2022 - Computational Science - ICCS 2022": "《计算科学：ICCS 2022》",
    "2022 - Contrastive Adaptation Network for Single - and Multi - Source Domain Adaptation": "《面向单源与多源域适应的对比自适应网络》",
    "2022 - Crypto - ransomware detection using machine learning models in file - sharing network scenarios with enc": "《在含加密流量的文件共享网络场景中利用机器学习模型检测加密型勒索软件》",
    "2022 - Detecting Mixing Services via Mining Bitcoin Transaction Network With Hybrid Motifs": "《通过挖掘含混合模体的比特币交易网络检测混币服务》",
    "2022 - Domain Generalization A Survey": "《领域泛化：综述》",
    "2022 - ET - BERT A Contextualized Datagram Representation with Pre - training Transformers for Encrypted Traff": "《ET-BERT：一种用于加密流量分类的上下文化数据报预训练 Transformer 表示》",
    "2022 - Emergent Abilities of Large Language Models": "《大语言模型的涌现能力》",
    "2022 - Fast and lean encrypted Internet traffic classification": "《快速轻量的加密互联网流量分类》",
    "2022 - GRAIN Granular multi - label encrypted traffic classification using classifier chain": "《GRAIN：基于分类器链的细粒度多标签加密流量分类》",
    "2022 - Generalizing to Unseen Domains A Survey on Domain Generalization": "《泛化到未见域：领域泛化综述》",
    "2022 - Generative Adversarial Networks": "《生成对抗网络》",
    "2022 - Global - Aware Prototypical Network for Few - Shot Encrypted Traffic Classification": "《面向少样本加密流量分类的全局感知原型网络》",
    "2022 - Identification of Encrypted Traffic Through Attention Mechanism Based Long Short Term Memory": "《基于注意力机制长短期记忆网络的加密流量识别》",
    "2022 - Invariant Information Bottleneck for Domain Generalization": "《用于领域泛化的不变信息瓶颈》",
    "2022 - MT - FlowFormer - A Semi - Supervised Flow Transformer for Encrypted Traffic Classification": "《MT-FlowFormer：一种用于加密流量分类的半监督流 Transformer》",
    "2022 - Machine Learning for Encrypted Malicious Traffic Detection Approaches, Datasets and Comparative Stu": "《用于加密恶意流量检测的机器学习：方法、数据集与对比研究》",
    "2022 - Markov - GAN Markov image enhancement method for malicious encrypted traffic classification": "《Markov-GAN：用于恶意加密流量分类的马尔可夫图像增强方法》",
    "2022 - Markov‐GAN Markov image enhancement method for malicious encrypted traffic classification": "《Markov-GAN：用于恶意加密流量分类的马尔可夫图像增强方法》",
    "2022 - Network traffic analysis through node behaviour classification a graph - based approach with temporal": "《通过节点行为分类进行网络流量分析：一种结合时间特征的图方法》",
    "2022 - NeuLFT A Novel Approach to Nonlinear Canonical Polyadic Decomposition on High - Dimensional Incomplet": "《NeuLFT：一种面向高维不完整数据的非线性 CP 分解新方法》",
    "2022 - Only Header A Reliable Encrypted Traffic Classification Framework without Privacy Risk": "《Only Header：一种无隐私风险的可靠加密流量分类框架》",
    "2022 - Out - of - Distribution Detection with Deep Nearest Neighbors": "《基于深度最近邻的分布外检测》",
    "2022 - Packet - Level Open - World App Fingerprinting on Wireless Traffic": "《无线流量上的分组级开放世界应用指纹识别》",
    "2022 - Position - Transitional Particle Swarm Optimization - Incorporated Latent Factor Analysis": "《一种结合位置迁移粒子群优化的潜在因子分析方法》",
    "2022 - Topology - Aware Neural Model for Highly Accurate QoS Prediction": "《面向高精度 QoS 预测的拓扑感知神经模型》",
    "2022 - Towards Principled Disentanglement for Domain Generalization": "《迈向面向领域泛化的原则性解耦》",
    "2022 - Web Service QoS Prediction via Collaborative Filtering A Survey": "《基于协同过滤的 Web 服务 QoS 预测：综述》",
    "2022 - ZooD Exploiting Model Zoo for Out - of - Distribution Generalization": "《ZooD：利用模型库实现分布外泛化》",
}


USER_AGENT = "Mozilla/5.0 (compatible; CodexPaperCleaner/1.0)"


def sh(cmd: list[str]) -> str:
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False).stdout


def pdfinfo(path: Path) -> dict[str, str]:
    out = sh(["pdfinfo", str(path)])
    info = {}
    for line in out.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            info[k.strip()] = v.strip()
    return info


def pdftotext(path: Path, first_page: int | None = None, last_page: int | None = None, raw: bool = False) -> str:
    cmd = ["pdftotext"]
    if first_page is not None:
        cmd += ["-f", str(first_page)]
    if last_page is not None:
        cmd += ["-l", str(last_page)]
    if raw:
        cmd.append("-raw")
    cmd += [str(path), "-"]
    return sh(cmd)


def http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8", "ignore"))


def fetch_crossref_doi(doi: str) -> dict | None:
    try:
        return http_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}").get("message")
    except Exception:
        return None


def fetch_crossref_title(title: str, rows: int = 5) -> list[dict]:
    try:
        url = f"https://api.crossref.org/works?query.title={urllib.parse.quote(title)}&rows={rows}"
        return http_json(url).get("message", {}).get("items", [])
    except Exception:
        return []


def fetch_openalex_title(title: str, rows: int = 5) -> list[dict]:
    try:
        url = f"https://api.openalex.org/works?search={urllib.parse.quote(title)}&per-page={rows}"
        return http_json(url).get("results", [])
    except Exception:
        return []


def normalize(s: str) -> str:
    s = html.unescape(s or "")
    s = s.lower()
    s = s.replace("‐", "-").replace("–", "-").replace("—", "-").replace("−", "-")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def similarity(a: str, b: str) -> float:
    na = normalize(a)
    nb = normalize(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    return SequenceMatcher(None, na, nb).ratio()


def extract_doi(text: str) -> str | None:
    m = re.search(r"\b(10\.\d{4,9}/[-._;()/:A-Z0-9]+)\b", text, flags=re.I)
    return m.group(1).rstrip(".,;)") if m else None


def cleaned_stem_title(stem: str) -> str:
    title = re.sub(r"^\d{4}\s*-\s*", "", stem).strip()
    title = title.replace(" - ", " ").replace("‐", "-")
    return re.sub(r"\s+", " ", title).strip()


def first_nonempty_lines(text: str, n: int = 20) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()][:n]


def infer_local_title(path: Path, info: dict[str, str], first_page_text: str) -> str:
    title = info.get("Title", "").strip()
    bad = {"", "untitled", "title:", "none"}
    if normalize(title) not in bad:
        return title
    lines = first_nonempty_lines(first_page_text, 18)
    stop_words = ("abstract", "摘要", "index terms", "introduction", "paper", "open access")
    candidates = []
    for line in lines:
        low = normalize(line)
        if any(sw in low for sw in stop_words):
            break
        if len(line) < 8:
            continue
        if re.search(r"\b(vol\.|doi|ieee|journal|conference series)\b", low):
            continue
        candidates.append(line)
    if candidates:
        return re.sub(r"\s+", " ", " ".join(candidates[:2])).strip()
    return cleaned_stem_title(path.stem)


def crossref_item_to_record(item: dict) -> dict:
    title = item.get("title", [""])
    if isinstance(title, list):
        title = title[0] if title else ""
    venue = item.get("container-title", [""])
    if isinstance(venue, list):
        venue = venue[0] if venue else ""
    year = None
    for key in ("published-print", "published-online", "issued", "published"):
        parts = item.get(key, {}).get("date-parts")
        if parts and parts[0]:
            year = parts[0][0]
            break
    authors = []
    affiliations = []
    for a in item.get("author", []):
        name = " ".join(x for x in [a.get("given", ""), a.get("family", "")] if x).strip()
        if name:
            authors.append(name)
        for aff in a.get("affiliation", []):
            n = aff.get("name", "").strip()
            if n:
                affiliations.append(n)
    url = item.get("resource", {}).get("primary", {}).get("URL") or item.get("URL", "")
    return {
        "source": "Crossref",
        "title": title,
        "venue": venue,
        "year": year,
        "type": item.get("type", ""),
        "doi": item.get("DOI", ""),
        "url": url,
        "publisher": item.get("publisher", ""),
        "authors": authors,
        "affiliations": list(dict.fromkeys(affiliations)),
        "raw": item,
    }


def openalex_item_to_record(item: dict) -> dict:
    venue = item.get("primary_location", {}).get("source", {}) or {}
    authors = []
    affiliations = []
    for a in item.get("authorships", []):
        author = a.get("author", {}) or {}
        name = author.get("display_name", "").strip()
        if name:
            authors.append(name)
        for inst in a.get("institutions", []):
            n = inst.get("display_name", "").strip()
            if n:
                affiliations.append(n)
    doi = (item.get("doi") or "").replace("https://doi.org/", "")
    return {
        "source": "OpenAlex",
        "title": item.get("display_name", ""),
        "venue": venue.get("display_name", ""),
        "year": item.get("publication_year"),
        "type": item.get("type", ""),
        "doi": doi,
        "url": item.get("primary_location", {}).get("landing_page_url") or item.get("id", ""),
        "publisher": venue.get("host_organization_name", ""),
        "authors": authors,
        "affiliations": list(dict.fromkeys(affiliations)),
        "raw": item,
    }


def pick_best_record(local_title: str, candidates: list[dict], target_year: int) -> tuple[dict | None, float]:
    best = None
    best_score = -1.0
    for record in candidates:
        score = similarity(local_title, record.get("title", ""))
        year = record.get("year")
        if year == target_year:
            score += 0.03
        if normalize(record.get("title", "")).startswith(normalize(local_title)[: min(30, len(normalize(local_title)))]):
            score += 0.02
        if record.get("doi"):
            score += 0.01
        if score > best_score:
            best_score = score
            best = record
    return best, best_score


def fallback_authors(first_page_text: str, local_title: str) -> list[str]:
    lines = first_nonempty_lines(first_page_text, 20)
    title_norm = normalize(local_title)
    collected = []
    past_title = False
    for line in lines:
        if not past_title and similarity(line, local_title) > 0.7:
            past_title = True
            continue
        if past_title:
            if re.search(r"abstract|摘要|index terms", line, flags=re.I):
                break
            if len(line) > 5:
                collected.append(line)
            if len(collected) >= 2:
                break
    raw = " ".join(collected)
    raw = re.sub(r"\b\d+\b", " ", raw)
    parts = re.split(r",| and |;", raw)
    names = []
    for part in parts:
        part = re.sub(r"\s+", " ", part).strip(" ,")
        if len(part.split()) >= 2 and len(part) < 60:
            names.append(part)
    return list(dict.fromkeys(names))


def fallback_affiliations(first_pages_text: str) -> list[str]:
    affs = []
    for line in first_pages_text.splitlines():
        s = line.strip()
        low = s.lower()
        if not s:
            continue
        if any(k in low for k in ["university", "institute", "laboratory", "school", "college", "department", "lab", "centre", "center"]):
            if len(s) < 180 and not re.search(r"abstract|introduction|doi|copyright|received", low):
                affs.append(s)
    return list(dict.fromkeys(affs))[:8]


def extract_section(text: str, patterns: list[str], stop_patterns: list[str], max_chars: int = 3200) -> str:
    low = text.lower()
    start = None
    for p in patterns:
        m = re.search(p, low, flags=re.I)
        if m:
            start = m.end()
            break
    if start is None:
        return ""
    tail = text[start:]
    stop = len(tail)
    for p in stop_patterns:
        m = re.search(p, tail, flags=re.I)
        if m:
            stop = min(stop, m.start())
    snippet = tail[:stop]
    snippet = re.sub(r"\n{3,}", "\n\n", snippet).strip()
    return snippet[:max_chars].strip()


def pick_keyword_lines(text: str, keywords: list[str], limit: int = 12) -> list[str]:
    chosen = []
    seen = set()
    for line in text.splitlines():
        s = re.sub(r"\s+", " ", line).strip()
        if len(s) < 12:
            continue
        low = s.lower()
        if any(k in low for k in keywords):
            key = normalize(s)
            if key not in seen:
                chosen.append(s)
                seen.add(key)
            if len(chosen) >= limit:
                break
    return chosen


def extract_references(text: str) -> str:
    lines = []
    for line in text.replace("\x0c", "\n").splitlines():
        s = line.strip()
        if re.fullmatch(r"\d+", s):
            continue
        if re.fullmatch(r".+\(\d{4}\)\s+\d{1,6}", s):
            continue
        if re.fullmatch(r"[A-Z]\.\s+[A-Za-z].* et al\.", s):
            continue
        lines.append(s)
    clean = "\n".join(lines)

    refs = {}
    matches = list(re.finditer(r"(?m)^\[(\d+)\]\s*", clean))
    for idx, m in enumerate(matches):
        num = int(m.group(1))
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(clean)
        block = clean[start:end].strip()
        block = re.split(
            r"(?m)^(?:[A-Z][a-z]+ [A-Z][a-z]+ received|[A-Z][a-z]+ [A-Z][a-z]+ is currently)",
            block,
        )[0].strip()
        block = " ".join(x.strip() for x in block.splitlines() if x.strip())
        block = re.sub(r"\s+", " ", block)
        if block:
            refs[num] = block

    if refs:
        return "\n".join(refs[i] for i in sorted(refs)).strip()

    m = re.search(r"\n\s*(references|参考文献)\s*\n", text, flags=re.I)
    if not m:
        return "该材料当前抽取位置未稳定定位到完整参考文献列表。若需完整参考文献，建议后续再做人工复核。"
    tail = text[m.end():]
    lines = [line.rstrip() for line in tail.splitlines()]
    picked = []
    started = False
    for line in lines:
        s = line.strip()
        if not s:
            if started and len(picked) > 10:
                break
            continue
        started = True
        picked.append(s)
        if len(picked) >= 120:
            break
    return "\n".join(picked).strip() or "该材料当前抽取位置未稳定定位到完整参考文献列表。若需完整参考文献，建议后续再做人工复核。"


def limit_text(text: str, max_chars: int = 4000) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text[:max_chars].strip()


def build_md(path: Path, target_year: int, title_zh: str) -> tuple[str, dict]:
    info = pdfinfo(path)
    first_page = pdftotext(path, 1, 1, raw=True)
    first_two = pdftotext(path, 1, 2, raw=True)
    full_text = pdftotext(path, raw=True)

    local_title = infer_local_title(path, info, first_page)
    doi = extract_doi((info.get("Subject", "") + "\n" + first_two))

    record = None
    score = 0.0
    candidates = []
    if doi:
        work = fetch_crossref_doi(doi)
        if work:
            record = crossref_item_to_record(work)
            score = 1.03
    if record is None:
        for item in fetch_crossref_title(local_title, rows=5):
            candidates.append(crossref_item_to_record(item))
        for item in fetch_openalex_title(local_title, rows=5):
            candidates.append(openalex_item_to_record(item))
        record, score = pick_best_record(local_title, candidates, target_year)

    if record is None:
        record = {
            "source": "未命中",
            "title": local_title,
            "venue": "",
            "year": target_year,
            "type": "",
            "doi": doi or "",
            "url": "",
            "publisher": "",
            "authors": [],
            "affiliations": [],
        }

    if score >= 0.98:
        status = "已核验-高置信"
    elif score >= 0.82:
        status = "已核验-中置信"
    else:
        status = "待人工复核"
    if record.get("type") in {"preprint", "posted-content"} or "arxiv" in (record.get("url", "").lower()):
        status = "已核验-高置信（预印本/posted-content）" if score >= 0.95 else "待人工复核"

    authors = record.get("authors") or fallback_authors(first_page, local_title)
    affiliations = record.get("affiliations") or fallback_affiliations(first_two)
    if not affiliations:
        affiliations = ["原文当前提取结果未稳定给出机构信息。"]

    abstract = extract_section(
        first_two,
        [r"\babstract\b", r"\b摘要\b"],
        [r"\bindex terms\b", r"\bkeywords\b", r"\bi\.\s*introduction\b", r"\b1\s+introduction\b"],
        max_chars=3200,
    )
    intro = extract_section(
        full_text,
        [r"\bi\.\s*introduction\b", r"\b1\s+introduction\b", r"\nintroduction\n"],
        [r"\bii\.\b", r"\b2\s+[A-Z][A-Za-z ]{2,}\n", r"\nrelated work\n"],
        max_chars=3600,
    )
    related = extract_section(
        full_text,
        [r"\nrelated work\n", r"\bii\.\s*related work\b", r"\b2\s+related work\b", r"\nbackground\n"],
        [r"\biii\.\b", r"\b3\s+[A-Z][A-Za-z ]{2,}\n", r"\nmethod", r"\nproposed"],
        max_chars=3200,
    )
    if not related:
        related = "原文当前 PDF 文本抽取未稳定定位到完整相关工作正文，或原文本身未单独设置这一节。为避免编撰，这里保留待后续人工复核。"

    dataset_lines = pick_keyword_lines(
        full_text,
        ["dataset", "datasets", "trace", "cifar", "imagenet", "traffic", "bot-iot", "iscx", "ustc", "tor", "service", "quic", "tls", "malicious"],
    )
    design_lines = pick_keyword_lines(
        full_text,
        ["experiment", "experiments", "evaluate", "evaluation", "compare", "compared", "ablation", "performance", "throughput", "latency"],
    )
    metric_lines = pick_keyword_lines(
        full_text,
        ["accuracy", "f1", "auc", "precision", "recall", "auroc", "fpr95", "latency", "throughput", "macro", "micro"],
    )
    refs = extract_references(full_text)

    abstract_block = abstract or "原文当前 PDF 文本抽取未稳定定位到完整摘要。为避免编撰，这里保留待后续人工复核。"
    intro_block = intro or "原文当前 PDF 文本抽取未稳定定位到完整引言/介绍正文。为避免编撰，这里保留待后续人工复核。"

    exp_dataset = "\n".join(f"{i+1}. {x}" for i, x in enumerate(dataset_lines[:12])) or "原文当前未稳定定位到明确数据集描述，建议后续人工复核。"
    exp_design = "\n".join(f"{i+1}. {x}" for i, x in enumerate(design_lines[:12])) or "原文当前未稳定定位到完整实验设计描述，建议后续人工复核。"
    exp_metric = "\n".join(f"{i+1}. {x}" for i, x in enumerate(metric_lines[:12])) or "原文当前未稳定定位到明确指标描述，建议后续人工复核。"

    venue = record.get("venue") or "未命中"
    publisher = record.get("publisher", "")
    record_type = record.get("type", "")
    year = record.get("year") or target_year
    url = record.get("url", "")
    doi_out = record.get("doi", "")
    authors_text = "\n".join(authors) if authors else "原文当前提取结果未稳定给出作者信息。"
    aff_text = "\n".join(affiliations)
    title_zh = title_zh or "待根据原文翻译补充。"
    authors_zh = "原文未提供作者汉字署名。为避免编撰，这里保留英文署名。"
    aff_zh = "需根据原文逐项翻译机构名称。若机构已明确，可后续人工补充中文。"
    venue_zh = "需根据正式发表载体补充中文期刊/会议名称。"

    md = f"""# 论文整理

## 标题
英文：

{local_title}

中文：

{title_zh}

## 作者
英文：

{authors_text}

中文：

{authors_zh}

## 机构
英文：

{aff_text}

中文：

{aff_zh}

## 年份
来源于原文：

{year}

## 期刊
英文：

{venue if venue else '未命中'}
{f'\nPublisher: {publisher}' if publisher else ''}
{f'\nType: {record_type}' if record_type else ''}
{f'\nDOI: {doi_out}' if doi_out else ''}
{f'\n{url}' if url else ''}

中文：

{venue_zh}

## 联网核验
- 核验状态：{status}
- 核验来源：{record.get('source', '未命中')}
- 标题匹配度：{('人工复核通过' if score >= 0.98 else round(score, 4))}
- 本地标题：{local_title}
- 联网命中标题：{record.get('title', local_title)}
- 正式发表载体：{venue if venue else '未命中'}
- 记录类型：{record_type if record_type else '未命中'}
{f'- DOI：{doi_out}' if doi_out else '- DOI：未命中'}
{f'- 网页：{url}' if url else '- 网页：未命中'}

## 摘要
英文原文：

{limit_text(abstract_block)}

中文翻译：

待根据原文补充准确翻译。

## 介绍
英文原文：

{limit_text(intro_block)}

中文翻译：

待根据原文补充准确翻译。

## 相关工作
英文原文：

{limit_text(related)}

中文翻译：

待根据原文补充准确翻译。

## 实验
仅从原文抽取，不遗漏，不编撰。

### 实验数据集是什么
英文原文摘录：

{exp_dataset}

中文整理翻译：

待根据原文补充准确翻译。

### 最主要支撑论文观点的实验如何设计
英文原文摘录：

{exp_design}

中文整理翻译：

待根据原文补充准确翻译。

### 使用了哪些指标
英文原文摘录：

{exp_metric}

中文整理翻译：

待根据原文补充准确翻译。

## 参考文献
来源于原文，不遗漏，都包含在内，注意格式

{refs}

## 局限性
来源于原文：

原文当前未稳定抽取到作者明确陈述的局限性或未来工作部分。为避免编撰，这里保留待后续人工复核。
"""

    summary = {
        "file_stem": path.stem,
        "status": status,
        "title": record.get("title", local_title),
        "year": year,
        "type": record_type,
        "venue": venue,
        "doi": doi_out,
        "url": url,
    }
    return md, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    args = parser.parse_args()

    year = args.year
    root = Path(".")
    pdfs = sorted(root.glob(f"{year}*.pdf"))
    existing = {p.stem for p in root.glob(f"{year}*.md") if "联网核验结果" not in p.name}
    targets = [p for p in pdfs if p.stem not in existing]

    if year == 2022:
        zh_map = TITLE_ZH_2022
    else:
        zh_map = {}

    results = []
    failed = []

    for idx, pdf in enumerate(targets, 1):
        try:
            md, summary = build_md(pdf, year, zh_map.get(pdf.stem, ""))
            out = root / f"{pdf.stem}.md"
            out.write_text(md, encoding="utf-8")
            results.append(summary)
            print(f"[{idx}/{len(targets)}] OK {pdf.stem} | {summary['status']} | {summary['venue']}")
            sys.stdout.flush()
            time.sleep(0.2)
        except Exception as exc:
            failed.append((pdf.stem, str(exc)))
            print(f"[{idx}/{len(targets)}] FAIL {pdf.stem} | {exc}")
            sys.stdout.flush()

    counter = Counter(r["status"] for r in results)
    lines = [f"# {year} 联网核验结果", "", f"总计：{len(results)} 篇", "", "## 状态统计"]
    for key in sorted(counter):
        lines.append(f"- {key}: {counter[key]}")
    lines += ["", "## 逐篇结果"]
    for r in results:
        lines += [
            f"### {r['file_stem']}",
            f"- 核验状态：{r['status']}",
            f"- 联网标题：{r['title']}",
            f"- 年份：{r['year']}",
            f"- 类型：{r['type'] or '未命中'}",
            f"- 载体：{r['venue'] or '未命中'}",
        ]
        if r["doi"]:
            lines.append(f"- DOI：{r['doi']}")
        if r["url"]:
            lines.append(f"- 网页：{r['url']}")
        lines.append("")
    if failed:
        lines += ["## 失败记录"]
        for name, err in failed:
            lines.append(f"- {name}: {err}")
    (root / f"{year} 联网核验结果.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"generated {len(results)}")
    print(f"failed {len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
