import re


def _count_chinese_chars(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def validate_grant(markdown_text: str):
    references_count = len(re.findall(r"^\d+\.\s", markdown_text, flags=re.MULTILINE))
    figures_count = len(re.findall(r"!\[.*?\]\(.*?\)", markdown_text))

    # rough section extraction
    rationale = _extract_section(markdown_text, "## 一、立项依据", "## 二、研究内容与研究目标")
    objectives = _extract_section(markdown_text, "## 二、研究内容与研究目标", "## 三、具体研究方案")
    plan = _extract_section(markdown_text, "## 三、具体研究方案", "## 参考文献")

    report = {
        "rationale_chars": _count_chinese_chars(rationale),
        "objectives_chars": _count_chinese_chars(objectives),
        "plan_chars": _count_chinese_chars(plan),
        "references_count": references_count,
        "figures_count": figures_count,
        "pass": True,
        "issues": [],
    }

    if report["rationale_chars"] < 800:
        report["pass"] = False
        report["issues"].append("立项依据字数偏少")
    if report["objectives_chars"] < 400:
        report["pass"] = False
        report["issues"].append("研究内容与目标字数偏少")
    if report["plan_chars"] < 1200:
        report["pass"] = False
        report["issues"].append("研究方案字数偏少")
    if references_count < 10:
        report["pass"] = False
        report["issues"].append("参考文献不足10篇")
    if figures_count < 2:
        report["pass"] = False
        report["issues"].append("图片不足2张")

    return report


def _extract_section(text: str, start_marker: str, end_marker: str) -> str:
    try:
        start = text.index(start_marker) + len(start_marker)
        end = text.index(end_marker)
        return text[start:end].strip()
    except ValueError:
        return ""
