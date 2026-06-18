#!/usr/bin/env python3

"""Validate a code change plan Markdown file.



Checks: 7 mandatory sections, approval status, traceability chains.

Read-only, standard library only.

"""

import argparse

import re

from pathlib import Path



SECTIONS = [

    ("1", "基本信息与需求分析"),

    ("2", "当前实现与差距"),

    ("3", "目标方案与对比"),

    ("4", "影响范围与文件清单"),

    ("5", "实施顺序"),

    ("6", "测试、验证与完成"),

    ("7", "执行契约与审批"),

]



APPROVAL_RE = re.compile(

    r"WAITING_FOR_APPROVAL|APPROVED_WITH_CHANGES|APPROVED(?!_)|REJECTED|SUPERSEDED",

    re.IGNORECASE,

)





def find_sections(content):

    sections = []

    for line_number, line in enumerate(content.splitlines(), start=1):

        match = re.match(r"^##\s+\d+\.\s*(.+)$", line)

        if match:

            sections.append((match.group(1).strip(), line_number))

    return sections





def extract_ids(content, prefix):

    pattern = re.compile(r"\b(" + prefix + r"-\d+)\b", re.IGNORECASE)

    return {match.group(1).upper() for match in pattern.finditer(content)}





def check_traceability(content):

    errors = []

    req_ids = extract_ids(content, "REQ")

    ac_ids = extract_ids(content, "AC")

    cu_ids = extract_ids(content, "CU")

    v_ids = extract_ids(content, "V")

    lr_ids = extract_ids(content, "LR")



    if req_ids and not ac_ids:

        errors.append("REQ IDs found but no AC (acceptance criteria) IDs")

    if ac_ids and not cu_ids:

        errors.append("AC IDs found but no CU (modification unit) IDs")

    if cu_ids and not v_ids:

        errors.append("CU IDs found but no V (verification) IDs")

    if lr_ids and not cu_ids:

        errors.append("LR IDs found but no CU references")



    return errors





def validate(plan_path):

    result = {

        "plan_path": str(plan_path),

        "valid": True,

        "errors": [],

        "warnings": [],

        "sections_found": [],

        "sections_missing": [],

        "approval_status": None,

    }



    if not plan_path.is_file():

        result["valid"] = False

        result["errors"].append("Plan file not found: " + str(plan_path))

        return result



    content = plan_path.read_text(encoding="utf-8", errors="replace")



    # --- UTF-8 integrity check ---

    raw_bytes = plan_path.read_bytes()

    if raw_bytes[:3] == b'\xef\xbb\xbf':

        result["errors"].append("UTF-8 BOM detected; plans must be UTF-8 without BOM")

    try:

        test_decode = raw_bytes.decode("utf-8")

    except UnicodeDecodeError as ude:

        result["errors"].append("Invalid UTF-8 encoding: " + str(ude))

    else:

        if '\ufffd' in test_decode:

            result["errors"].append("Unicode replacement characters found; file encoding is corrupted (mojibake)")

    # --- end UTF-8 check ---



    sections = find_sections(content)

    result["sections_found"] = [section[0] for section in sections]



    section_titles_lower = [section[0].lower() for section in sections]

    for section_id, keyword in SECTIONS:

        found = any(keyword.lower() in title for title in section_titles_lower)

        if not found:

            result["sections_missing"].append(section_id + ". " + keyword)

            result["errors"].append("Missing section: " + section_id + ". " + keyword)



    for line in content.splitlines():

        if any(keyword in line for keyword in ["审批状态", "审批记录"]):

            match = APPROVAL_RE.search(line)

            if match:

                result["approval_status"] = match.group(0).upper()

                break



    if result["approval_status"]:

        if result["approval_status"] != "WAITING_FOR_APPROVAL":

            result["errors"].append(

                "Approval status is "

                + result["approval_status"]

                + ", must be WAITING_FOR_APPROVAL"

            )

    else:

        result["approval_status"] = "WAITING_FOR_APPROVAL"



    result["errors"].extend(check_traceability(content))



    if result["errors"]:

        result["valid"] = False



    return result





def main():

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--plan", required=True, help="Path to the change plan Markdown file")

    args = parser.parse_args()



    result = validate(Path(args.plan).resolve())



    print("Plan: " + result["plan_path"])

    print("Sections found: " + str(len(result["sections_found"])) + "/7")

    if result["sections_missing"]:

        print("Missing sections:")

        for section in result["sections_missing"]:

            print("  - " + section)

    print("Approval status: " + (result["approval_status"] or "NOT DETECTED"))



    if result["errors"]:

        print("\nErrors (" + str(len(result["errors"])) + "):")

        for error in result["errors"]:

            print("  - " + error)



    if result["warnings"]:

        print("\nWarnings (" + str(len(result["warnings"])) + "):")

        for warning in result["warnings"]:

            print("  - " + warning)



    if result["valid"]:

        print("\nVALID")

        return 0



    print("\nINVALID (" + str(len(result["errors"])) + " errors)")

    return 1





if __name__ == "__main__":

    raise SystemExit(main())

