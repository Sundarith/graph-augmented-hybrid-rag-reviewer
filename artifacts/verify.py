"""Verify the archived CTI-Bench outcomes and recount the paper result."""

import csv
import hashlib
import json
import re
from pathlib import Path

ARTIFACTS = Path(__file__).resolve().parent
EXPECTED = {"mapped": (837, 903), "unmapped": (72, 97)}


def check(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def main():
    manifest = json.loads((ARTIFACTS / "manifest.json").read_text(encoding="utf-8"))
    check(manifest.keys() == EXPECTED.keys(), "Unexpected split manifest")
    total_correct = 0
    total_cases = 0
    for split, (expected_correct, expected_cases) in EXPECTED.items():
        entry = manifest[split]
        path = ARTIFACTS / f"phi4_{split}.csv"
        check(path.name == entry["file"], f"{split}: unexpected filename")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        check(digest == entry["sha256"], f"{split}: checksum mismatch")

        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            check(reader.fieldnames == ["completion_ordinal", "cve_id", "passed"],
                  f"{split}: unexpected CSV columns")
            rows = list(reader)

        cases = len(rows)
        check(cases == entry["count"] == expected_cases, f"{split}: incorrect case count")
        for ordinal, row in enumerate(rows, 1):
            check(row["completion_ordinal"] == str(ordinal), f"{split}: invalid case order")
            check(re.fullmatch(r"CVE-\d{4}-\d+", row["cve_id"]), f"{split}: invalid CVE ID")
            check(row["passed"] in ("0", "1"), f"{split}: invalid outcome")

        correct = sum(row["passed"] == "1" for row in rows)
        check(correct == entry["correct"] == expected_correct, f"{split}: incorrect pass count")
        total_correct += correct
        total_cases += cases
        print(f"{split}: {correct}/{cases} ({correct / cases:.1%})")

    print(f"combined: {total_correct}/{total_cases} ({total_correct / total_cases:.1%})")


if __name__ == "__main__":
    main()
