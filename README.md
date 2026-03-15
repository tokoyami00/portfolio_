# 常闇 — canvas note

> 写真を並べて、あなただけの世界をつくる

---

## セットアップ

### Step 1 — 写真を入れる

```
images/
  01_息をひそめて_2023.jpg   ← ファイル名がそのままタイトル・年になる
  02_光の縁_2022.jpg
  03.jpg                     ← タイトルなしでもOK
```

**ファイル名のルール（任意）:**
| ファイル名 | タイトル | 年 |
|---|---|---|
| `01_息をひそめて_2023.jpg` | 息をひそめて | 2023 |
| `02_光の縁.jpg` | 光の縁 | — |
| `portrait.jpg` | portrait | — |

### Step 2 — generate.py を実行する

```bash
python generate.py
```

`images.json` が自動生成される。初回は `generate.py` の上部にある作家情報を編集：

```python
ARTIST = {
    "name":      "常闇",        # サイトに表示される名前
    "name_en":   "tokoyami",    # 英語表記
    "tagline":   "a quiet archive",
    "twitter":   "your_id",     # X (Twitter) ID（@なし）
    "instagram": "your_id",     # Instagram ID
}
```

### Step 3 — GitHub に push する

```bash
git init
git add .
git commit -m "init"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

### Step 4 — GitHub Pages を有効化する

1. リポジトリの **Settings → Pages**
2. Source: `GitHub Actions` を選択
3. 数秒〜1分で公開される

公開URL: `https://USERNAME.github.io/REPO/`

---

## 写真を追加・更新するとき

```bash
# images/ に写真を追加・削除する
python generate.py          # images.json を再生成
git add images/ images.json
git commit -m "add photos"
git push
```

push すると GitHub Actions が自動でサイトをデプロイする。

---

## ファイル構成

```
tokoyami/
├── index.html                        # サイト本体（基本的に触らなくてOK）
├── generate.py                       # ★ images/ をスキャンして images.json を生成
├── images.json                       # generate.py が自動生成（手動編集も可）
├── images/                           # ★ ここに写真を入れる
│   ├── 01_息をひそめて_2023.jpg
│   └── ...
├── .github/
│   └── workflows/
│       ├── generate.yml              # push 時に images.json を自動更新
│       └── deploy.yml                # GitHub Pages へ自動デプロイ
└── README.md
```

---

## images.json を手動で編集したい場合

`generate.py` を実行せず直接編集できる。タイトルや順番を細かく調整したいときに使う。

```json
{
  "artist": {
    "name": "常闇",
    "name_en": "tokoyami",
    "tagline": "a quiet archive",
    "twitter": "your_twitter_id",
    "instagram": "your_instagram_id"
  },
  "works": [
    { "file": "01.jpg", "title": "息をひそめて", "year": "2023" },
    { "file": "02.jpg", "title": "光の縁",       "year": "2022" }
  ]
}
```

> ⚠️ 次に `generate.py` を実行すると上書きされる。手動編集を維持したい場合は `generate.py` を実行しない。

---

## シェア機能

- **URL コピー** — レイアウト情報をURLにエンコードして共有
- **X（Twitter）** — ツイート画面をサイトURL付きで開く
- **Instagram** — URLをクリップボードにコピー → Instagramを開く（Web APIの制限のため直接投稿は不可）

---

## 対応ブラウザ

Chrome / Safari / Firefox / Edge（最新版）

モバイルはタッチドラッグ対応。ただし最適化はデスクトップ向け。
