import json
import re
from difflib import SequenceMatcher
from pathlib import Path

IN_PATH = Path("docs/data/raw.json")
OUT_PATH = Path("docs/data/clustered.json")

def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^0-9a-z가-힣\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def sim(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()

def main():
    raw = json.loads(IN_PATH.read_text(encoding="utf-8"))
    items = raw["items"]

    clusters = []
    TH = 0.72  # 묶이는 정도 (0.65~0.80 사이에서 조절)

    for it in items:
        placed = False
        for c in clusters:
            if sim(it["title"], c["rep_title"]) >= TH:
                c["items"].append(it)
                placed = True
                break
        if not placed:
            clusters.append({"rep_title": it["title"], "items": [it]})

    # 점수: 묶음 크기 + 출처 다양성 보너스
    for c in clusters:
        sources = {x["source"] for x in c["items"]}
        c["score"] = len(c["items"]) + 0.5 * len(sources)

    clusters.sort(key=lambda x: x["score"], reverse=True)

    out = {
        "date_kst": raw["date_kst"],
        "generated_at_kst": raw["generated_at_kst"],
        "clusters": clusters[:20],  # 상위 20개 이슈
    }

    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()