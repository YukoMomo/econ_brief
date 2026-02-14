import json
from pathlib import Path

SRC = Path("docs/data/clustered.json")
DST = Path("docs/data/latest.json")

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    DST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()