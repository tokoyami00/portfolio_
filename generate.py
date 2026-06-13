#!/usr/bin/env python3
"""
generate.py
images/ フォルダをスキャンして images.json を自動生成するスクリプト。

【推奨】WebP変換オプション付き
  python generate.py          → images.json だけ生成
  python generate.py --webp   → WebP変換 + images.json 生成（爆速化）
"""

import os, sys, json, re
from pathlib import Path

# ─────────────────────────────────────────────────────────
# ★ ここだけ編集してください（初回のみ）
# ─────────────────────────────────────────────────────────
ARTIST = {
    "name":      "常闇",
    "name_en":   "tokoyami",
    "tagline":   "a quiet archive",
    "twitter":   "",   # XのID（@なし）例: "tokoyami_photo"
    "instagram": "",   # InstagramのID 例: "tokoyami.photo"
}

# WebP変換の品質 (0-100)
# 95 = 肉眼でオリジナルと区別できない高画質、ファイルサイズ約40-60%削減
WEBP_QUALITY = 95

# サムネ用の小さい画像を自動生成するか（サムネバーの読み込みが爆速になる）
# True にすると images/thumbs/ フォルダに 120px の極小画像を作成
MAKE_THUMBS = True
THUMB_SIZE  = 120  # px (長辺)
# ─────────────────────────────────────────────────────────

IMAGE_EXTS = {".jpg",".jpeg",".png",".webp",".JPG",".JPEG",".PNG",".WEBP"}
IMAGES_DIR  = Path("images")
THUMBS_DIR  = IMAGES_DIR / "thumbs"
OUTPUT_FILE = Path("images.json")

def normalize(f):
    return f.stem + f.suffix.lower()

def parse_name(stem):
    stem = re.sub(r"^work[-_]?\d+[-_]?", "", stem)
    stem = re.sub(r"^\d+[-_]?", "", stem)
    ym = re.search(r"[-_](\d{4})$", stem)
    year = ""
    if ym:
        year = ym.group(1)
        stem = stem[:ym.start()]
    return {"title": re.sub(r"[-_]+"," ",stem).strip(), "year": year}

def scan():
    if not IMAGES_DIR.exists():
        print(f"\n⚠  '{IMAGES_DIR}/' フォルダが見つかりません。作成します。")
        IMAGES_DIR.mkdir()
        return []

    files = sorted(
        [f for f in IMAGES_DIR.iterdir()
         if f.is_file() and f.suffix in IMAGE_EXTS and f.parent == IMAGES_DIR],
        key=lambda f: f.name.lower()
    )
    if not files:
        print(f"\n⚠  '{IMAGES_DIR}/' に画像が見つかりません。")
        return []

    works = []
    for f in files:
        n = normalize(f)
        if n != f.name:
            print(f"  ⚠  大文字拡張子: {f.name} → images.json には '{n}' で記録")
        meta = parse_name(f.stem)
        works.append({"file": n, "title": meta["title"], "year": meta["year"]})
        print(f"  ✓  {n}")
    return works

def convert_webp(works):
    """
    Pillow を使って全画像を WebP に変換する。
    変換後は images.json のファイル名も .webp に更新する。
    """
    try:
        from PIL import Image
    except ImportError:
        print("\n⚠  Pillow がインストールされていません。")
        print("   pip install Pillow  を実行してから再度試してください。")
        print("   WebP変換をスキップして images.json のみ生成します。\n")
        return works

    print("\n  WebP変換中...\n")
    new_works = []
    for w in works:
        src = IMAGES_DIR / w["file"]
        if not src.exists():
            new_works.append(w)
            continue
        stem = src.stem
        # すでにWebPなら変換不要
        if src.suffix.lower() == '.webp':
            new_works.append(w)
            continue
        dst = IMAGES_DIR / (stem + ".webp")
        try:
            img = Image.open(src)
            if img.mode in ("RGBA","LA","P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.save(dst, "webp", quality=WEBP_QUALITY, method=6)
            orig_kb = src.stat().st_size // 1024
            new_kb  = dst.stat().st_size // 1024
            saved   = int((1 - new_kb/orig_kb)*100) if orig_kb else 0
            print(f"  ✓  {src.name} → {dst.name}  ({orig_kb}KB → {new_kb}KB, -{saved}%)")
            new_works.append({**w, "file": dst.name})
        except Exception as e:
            print(f"  ✗  {src.name} 変換失敗: {e}")
            new_works.append(w)

    print(f"\n  💡 元の画像ファイル（.jpg/.png）はそのまま残しています。")
    print(f"  💡 GitHub には .webp ファイルだけアップすればOKです。")
    print(f"  💡 元ファイルを削除したい場合は手動で削除してください。")
    return new_works

def make_thumbs(works):
    """
    サムネ用の極小画像を images/thumbs/ に生成する。
    サムネバーの読み込みが劇的に速くなる。
    """
    try:
        from PIL import Image
    except ImportError:
        return

    THUMBS_DIR.mkdir(exist_ok=True)
    print(f"\n  サムネ生成中（{THUMB_SIZE}px）...\n")
    for w in works:
        src = IMAGES_DIR / w["file"]
        if not src.exists():
            continue
        dst = THUMBS_DIR / (src.stem + ".jpg")
        if dst.exists() and dst.stat().st_mtime > src.stat().st_mtime:
            print(f"  ✓  {dst.name} (スキップ: 最新)")
            continue
        try:
            img = Image.open(src)
            img.thumbnail((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
            img = img.convert("RGB")
            img.save(dst, "jpeg", quality=75, optimize=True)
            print(f"  ✓  {dst.name}  ({dst.stat().st_size//1024}KB)")
        except Exception as e:
            print(f"  ✗  {src.name}: {e}")

def main():
    use_webp = '--webp' in sys.argv
    print("=" * 52)
    print("  generate.py — images.json 生成")
    if use_webp:
        print("  モード: WebP変換 + サムネ生成")
    print("=" * 52)
    print(f"\n  '{IMAGES_DIR}/' をスキャン中...\n")

    works = scan()
    if not works:
        print("\n終了します。")
        return

    if use_webp:
        works = convert_webp(works)
        if MAKE_THUMBS:
            make_thumbs(works)
    elif MAKE_THUMBS:
        # --webp なしでもサムネだけは作る（Pillowがあれば）
        make_thumbs(works)

    output = {"artist": ARTIST, "works": works}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fp:
        json.dump(output, fp, ensure_ascii=False, indent=2)

    print(f"\n✅  {OUTPUT_FILE} を生成しました（{len(works)} 件）")
    print(f"\n次のステップ:")
    if use_webp:
        print(f"  1. images/*.webp + images/thumbs/*.jpg + images.json を GitHub にアップ")
    else:
        print(f"  1. images/ フォルダと images.json を GitHub にアップ")
        print(f"  💡 'python generate.py --webp' を実行すると画質そのままで")
        print(f"     ファイルサイズを40〜60%削減できます（Pillow必要）。")
    print(f"  2. GitHub Pages に反映（1〜2分）")

if __name__ == "__main__":
    main()
