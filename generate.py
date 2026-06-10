#!/usr/bin/env python3
"""
generate.py
images/ フォルダをスキャンして images.json を自動生成するスクリプト。
"""

import os
import json
import re
from pathlib import Path

# ─────────────────────────────────────────────────────────
# ★ ここだけ編集してください（初回のみ）
# ─────────────────────────────────────────────────────────
ARTIST = {
    "name":      "常闇",        # サイトに表示される名前
    "name_en":   "tokoyami",    # 英語表記（URLやOGPに使用）
    "tagline":   "a quiet archive",
    "twitter":   "",            # X (Twitter) のID（@なし）例: "tokoyami_photo"
    "instagram": "",            # Instagram のID 例: "tokoyami.photo"
}
# ─────────────────────────────────────────────────────────

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp",
    ".JPG", ".JPEG", ".PNG", ".WEBP",  # 大文字も検索
}

IMAGES_DIR  = Path("images")
OUTPUT_FILE = Path("images.json")


def normalize_filename(f: Path) -> str:
    """
    拡張子を小文字に統一する。
    GitHub Pages は Linux サーバーなので大文字小文字を区別します。
    work-01.JPG → work-01.jpg のように小文字に変換して返します。
    """
    return f.stem + f.suffix.lower()


def parse_filename(stem: str) -> dict:
    """
    ファイル名からタイトルと年を推測する（任意）。

    例:
      work-01_息をひそめて_2023 → title: 息をひそめて, year: 2023
      work-02                   → title: "", year: ""
      portrait_2022             → title: portrait, year: 2022
    """
    # 先頭の "work-01" 形式の番号を除去
    stem = re.sub(r"^work[-_]?\d+[-_]?", "", stem)
    stem = re.sub(r"^\d+[-_]?", "", stem)

    # 末尾の年（4桁）を抽出
    year_match = re.search(r"[-_](\d{4})$", stem)
    year = ""
    if year_match:
        year = year_match.group(1)
        stem = stem[: year_match.start()]

    # アンダースコア・ハイフンをスペースに変換
    title = re.sub(r"[-_]+", " ", stem).strip()

    return {"title": title, "year": year}


def scan_images() -> list:
    if not IMAGES_DIR.exists():
        print(f"\n⚠  '{IMAGES_DIR}/' フォルダが見つかりません。")
        print(f"   このスクリプトと同じ場所に '{IMAGES_DIR}/' フォルダを作って")
        print(f"   その中に写真を入れてから再実行してください。\n")
        IMAGES_DIR.mkdir()
        return []

    files = sorted(
        [f for f in IMAGES_DIR.iterdir() if f.suffix.lower().rstrip() in {e.lower() for e in IMAGE_EXTENSIONS}],
        key=lambda f: f.name.lower(),
    )

    if not files:
        print(f"\n⚠  '{IMAGES_DIR}/' フォルダに画像ファイルが見つかりません。")
        print(f"   対応形式: jpg / jpeg / png / webp\n")
        return []

    works = []
    warn_count = 0
    for f in files:
        normalized = normalize_filename(f)
        meta = parse_filename(f.stem)

        if normalized != f.name:
            print(f"  ⚠  大文字拡張子を検出: {f.name}")
            print(f"     → images.json には '{normalized}' として記録します")
            print(f"     → GitHub 上のファイル名も '{normalized}' にリネームしてください")
            warn_count += 1

        works.append({
            "file":  normalized,
            "title": meta["title"],
            "year":  meta["year"],
        })
        print(f"  ✓  {normalized}")

    if warn_count:
        print(f"\n  ⚠  大文字拡張子のファイルが {warn_count} 件あります。")
        print(f"     GitHub にアップするときはファイル名を小文字にしてください。")

    return works


def main():
    print("=" * 52)
    print("  generate.py — images.json 生成")
    print("=" * 52)
    print(f"\n  '{IMAGES_DIR}/' フォルダをスキャン中...\n")

    works = scan_images()

    output = {"artist": ARTIST, "works": works}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fp:
        json.dump(output, fp, ensure_ascii=False, indent=2)

    print(f"\n✅  {OUTPUT_FILE} を生成しました（{len(works)} 件）")

    if works:
        print(f"\n次のステップ:")
        print(f"  1. images/ フォルダと images.json を GitHub にアップ")
        print(f"  2. タイトルや年を変更したい場合は images.json を直接編集してもOK")
        print(f"     （次回 generate.py を実行すると上書きされます）")


if __name__ == "__main__":
    main()
