from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STAGE_ID = "1013R_R223M_P4_P1_NOTE_WEIGHT_REDUCTION_AND_MARGINIZATION"


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


def main() -> int:
    required = [
        "R223M_P4_P1_teacher_readable_process_v6.md",
        "R223M_P4_P1_teacher_readable_process_v6.html",
        "R223M_P4_P1_margin_note_policy.md",
        "R223M_P4_P1_default_vs_review_view_rules.md",
        "R223M_P4_P1_teacher_confirmation_summary.md",
        "R223M_P4_P1_marginized_review_note_ledger.json",
        "R223M_P4_P1_before_after_compare_with_P4.md",
        "R223M_P4_P1_report.md",
        "README_FOR_GPT_REVIEW.md",
        "PACKAGE_MANIFEST.json",
    ]
    checks = 0
    failures: list[str] = []
    for name in required:
        checks += 1
        if not (ROOT / name).exists():
            failures.append(f"missing:{name}")
    if failures:
        result = {"passed": False, "check_count": checks, "failed": len(failures), "failures": failures, "stage_id": STAGE_ID}
        print(json.dumps(result, ensure_ascii=False))
        return 1

    md = read("R223M_P4_P1_teacher_readable_process_v6.md")
    html = read("R223M_P4_P1_teacher_readable_process_v6.html")
    margin = read("R223M_P4_P1_margin_note_policy.md")
    view_rules = read("R223M_P4_P1_default_vs_review_view_rules.md")
    confirmation = read("R223M_P4_P1_teacher_confirmation_summary.md")
    manifest = json.loads(read("PACKAGE_MANIFEST.json"))
    ledger = json.loads(read("R223M_P4_P1_marginized_review_note_ledger.json"))

    for phrase in ["【本环节在做什么】", "【教师关注】", "【下游影响】", "过渡语："]:
        checks += 1
        count = md.count(phrase)
        if count != 7:
            failures.append(f"bad_default_count:{phrase}:{count}")

    for heavy in ["【小教判断】", "核心：", "风险：", "建议动作：", "确认点：", "素材/组件确认："]:
        checks += 1
        if heavy in md:
            failures.append(f"heavy_note_in_default:{heavy}")

    for phrase in ["连续教学过程", "审核视图", "页边注化", "不压在教学过程正文前"]:
        checks += 1
        if phrase not in margin:
            failures.append(f"missing_margin_policy:{phrase}")

    for phrase in ["默认教师阅读稿", "审核 / 开发视图", "小教判断", "师维控制点", "派生物影响"]:
        checks += 1
        if phrase not in view_rules:
            failures.append(f"missing_view_rule:{phrase}")

    for phrase in ["大屏素材", "学习单栏位", "组件候选", "评价证据", "teacher_confirmed=false"]:
        checks += 1
        if phrase not in confirmation:
            failures.append(f"missing_confirmation_summary:{phrase}")

    checks += 1
    if len(ledger.get("events", [])) != 7:
        failures.append("ledger_event_count_not_7")
    for event in ledger.get("events", []):
        checks += 1
        full = event.get("review_view_only", {}).get("xiaojiao_judgement_full", {})
        if not all(k in full for k in ["core_judgement", "high_risk", "suggested_action", "teacher_confirmation"]):
            failures.append(f"ledger_missing_full_judgement:{event.get('event_id')}")
        checks += 1
        default = event.get("default_teacher_visible", {})
        if not default.get("teacher_focus") or not default.get("downstream_impact"):
            failures.append(f"ledger_missing_default_notes:{event.get('event_id')}")

    for token in ["data-note-weight=\"reduced\"", "data-preview-only=\"true\"", "data-teacher-confirmed=\"false\"", STAGE_ID]:
        checks += 1
        if token not in html:
            failures.append(f"missing_html_state:{token}")

    for token in ["???", "锟", "\ufffd"]:
        checks += 1
        if token in html:
            failures.append(f"mojibake:{token}")

    checks += 1
    if manifest.get("stage_id") != STAGE_ID:
        failures.append("manifest_stage_mismatch")
    checks += 1
    if manifest.get("boundary", {}).get("r97b_modified") is not False:
        failures.append("r97b_modified_not_false")
    checks += 1
    if manifest.get("boundary", {}).get("formal_ui") is not False:
        failures.append("formal_ui_not_false")

    result = {
        "passed": not failures,
        "check_count": checks,
        "failed": len(failures),
        "failures": failures,
        "stage_id": STAGE_ID,
        "teacher_focus_count": md.count("【教师关注】"),
        "downstream_impact_count": md.count("【下游影响】"),
        "full_judgement_in_ledger": True,
        "formal_ui": "blocked",
    }
    (ROOT / "validate_1013R_R223M_P4_P1_note_weight_reduction_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
