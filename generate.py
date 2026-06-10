#!/usr/bin/env python3
"""
generate.py
images/ をスキャンして images.json を自動生成。
GitHub Actions で images/ に変更があるたびに自動実行される。
"""
import os, json, re
from pathlib import Path

# ★ ここだけ編集
ARTIST = {
    "name":      "常闇",
    "name_en":   "tokoyami",
    "tagline":   "a quiet archive",
    "twitter":   "",
    "instagram": "",
}

EXTS = {".jpg",".jpeg",".png",".webp",".JPG",".JPEG",".PNG",".WEBP"}
IMG_DIR = Path("images")
OUT     = Path("images.json")

def parse(stem):
    stem = re.sub(r"^\d+[_\-\s]*", "", stem)
    m = re.search(r"[_\-\s](\d{4})$", stem)
    year = m.group(1) if m else ""
    if m: stem = stem[:m.start()]
    return {"title": re.sub(r"[_\-]+"," ",stem).strip(), "year": year}

def main():
    IMG_DIR.mkdir(exist_ok=True)
    files = sorted([f for f in IMG_DIR.iterdir() if f.suffix in EXTS], key=lambda f: f.name.lower())
    works = []
    for f in files:
        m = parse(f.stem)
        # Always store as lowercase extension
        norm = f.stem + f.suffix.lower()
        works.append({"file": norm, "title": m["title"], "year": m["year"]})
        print(f"  ✓ {norm}")
    OUT.write_text(json.dumps({"artist": ARTIST, "works": works}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ {len(works)} 件 → {OUT}")

if __name__ == "__main__":
    main()
