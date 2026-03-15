#!/usr/bin/env python3
"""
generate.py — images/ フォルダをスキャンして images.json を自動生成

使い方:
  python generate.py

images/ に写真を入れて実行するだけ。
ファイル名の先頭に数字があれば並び順として使用。
例: 01_息をひそめて_2023.jpg → title: 息をひそめて, year: 2023
    photo.jpg               → title: photo
"""

import os
import json
import re
from pathlib import Path

# ─────────────────────────────────────
# ★ ここだけ編集してください ★
ARTIST = {
    "name":      "常闇",
    "name_en":   "tokoyami",
    "tagline":   "a quiet archive",
    "twitter":   "keer_pmom",        # X (Twitter) のID（@なし）例: "tokoyami_photo"
    "instagram": "loodmmm",        # Instagram のID 例: "tokoyami.photo"
}
# ─────────────────────────────────────

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
IMAGES_DIR = Path("images")
OUTPUT_FILE = Path("images.json")


def parse_filename(stem: str) -> dict:
    """
    ファイル名からタイトルと年を抽出する。
    パターン例:
      01_息をひそめて_2023  → title: 息をひそめて, year: 2023
      02_光の縁             → title: 光の縁, year: ""
      portrait_2022         → title: portrait, year: 2022
      photo                 → title: photo, year: ""
    """
    # 先頭の連番を除去
    stem = re.sub(r"^\d+[_\-\s]*", "", stem)

    # 末尾の年（4桁）を抽出
    year_match = re.search(r"[_\-\s](\d{4})$", stem)
    year = ""
    if year_match:
        year = year_match.group(1)
        stem = stem[: year_match.start()]

    # アンダースコア・ハイフンをスペースに変換してタイトルに
    title = re.sub(r"[_\-]+", " ", stem).strip()

    return {"title": title, "year": year}


def scan_images() -> list:
    if not IMAGES_DIR.exists():
        print(f"[warn] {IMAGES_DIR}/ フォルダが見つかりません。作成します。")
        IMAGES_DIR.mkdir()
        return []

    files = sorted(
        [f for f in IMAGES_DIR.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS],
        key=lambda f: f.name.lower(),
    )

    works = []
    for f in files:
        meta = parse_filename(f.stem)
        works.append({
            "file":  f.name,
            "title": meta["title"],
            "year":  meta["year"],
        })
        print(f"  ✓ {f.name}  →  title: '{meta['title']}'  year: '{meta['year']}'")

    return works


def main():
    print("=== generate.py: images/ をスキャン中... ===\n")

    works = scan_images()

    output = {
        "artist": ARTIST,
        "works":  works,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fp:
        json.dump(output, fp, ensure_ascii=False, indent=2)

    print(f"\n✅ {OUTPUT_FILE} を生成しました（{len(works)}件）")

    if not works:
        print("\n💡 images/ フォルダに写真を入れてから再実行してください。")
        print("   対応形式: jpg / jpeg / png / webp")
    else:
        print("\n💡 タイトルや年を変更したい場合は images.json を直接編集してください。")
        print("   次回 generate.py を実行すると上書きされます。")


if __name__ == "__main__":
    main()
