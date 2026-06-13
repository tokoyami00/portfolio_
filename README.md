# 常闇 — canvas note

写真を並べて、あなただけのキャンバスをつくる

---

## フォルダ構成

```
tokoyami/
├── index.html          ← サイト本体（基本的に触らなくてOK）
├── generate.py         ← ★ 写真を追加したらこれを実行する
├── images.json         ← generate.py が自動生成（手動編集も可）
├── images/             ← ★ ここに写真を入れる
│   ├── work-01.jpg
│   ├── work-02.jpg
│   └── ...
├── .github/
│   └── workflows/
│       └── deploy.yml  ← GitHub Pages への自動デプロイ設定
└── README.md           ← このファイル
```

---

## 初回セットアップ

### 1. Python をインストールする

[https://www.python.org/downloads/](https://www.python.org/downloads/)

インストールできたか確認（コマンドプロンプトで）:
```
python --version
```
`Python 3.x.x` と表示されればOK。

---

### 2. generate.py を設定する

`generate.py` をメモ帳などで開いて、上部の作家情報を編集:

```python
ARTIST = {
    "name":      "常闇",           # ← サイトに表示される名前
    "name_en":   "tokoyami",       # ← 英語表記
    "tagline":   "a quiet archive",
    "twitter":   "あなたのXのID",   # ← @なし。例: tokoyami_photo
    "instagram": "あなたのIGのID",  # ← 例: tokoyami.photo
}
```

---

### 3. 写真を images/ フォルダに入れる

```
images/
  work-01.jpg
  work-02.jpg
  work-03.jpg
  ...
```

**ファイル名のルール:**
- 拡張子は小文字にする（`.jpg` ○ / `.JPG` ✕）
- スペースは使わない（`my photo.jpg` ✕ → `my-photo.jpg` ○）

---

### 4. generate.py を実行する

**Windowsの場合:**

`tokoyami` フォルダを開いて、アドレスバーに `cmd` と入力して Enter。

```
python generate.py
```

または、`generate.py` をダブルクリックして実行。

**Macの場合:**

ターミナルを開いて:

```bash
cd ~/Desktop/tokoyami   # tokoyamフォルダの場所に合わせて変更
python3 generate.py
```

実行すると `images.json` が自動生成されます。

---

### 5. GitHub にアップロードする

変更したファイルをすべてコミット&プッシュする:

```
images/ フォルダ（写真ファイル）
images.json
```

GitHub Desktop を使っている場合は「Commit to main」→「Push origin」。

---

### 6. GitHub Pages を有効化する（初回のみ）

1. リポジトリの **Settings → Pages**
2. Source を **GitHub Actions** に変更
3. 1〜2分でサイトが公開される

公開URL: `https://ユーザー名.github.io/リポジトリ名/`

---

## 写真を追加・更新するとき（いつもの手順）

```
① images/ に写真を追加（または削除）
② python generate.py を実行 → images.json が更新される
③ images/ と images.json を GitHub にアップ
④ 1〜2分でサイトに反映
```

---

## 画像が表示されないときのチェックリスト

| 確認項目 | 確認方法 |
|---|---|
| ファイルが GitHub にアップされているか | リポジトリの `images/` フォルダを確認 |
| ファイル名が一致しているか | `images.json` の `file` と実際のファイル名を比較 |
| 拡張子が小文字か | `.jpg` ○ / `.JPG` ✕ |
| Actions が完了しているか | GitHub の Actions タブで緑のチェックを確認 |
| ブラウザキャッシュ | `Ctrl + Shift + R` で強制リロード |

直接URLで画像にアクセスして確認する方法:
```
https://ユーザー名.github.io/リポジトリ名/images/work-01.jpg
```
このURLで画像が表示されれば、ファイルは正常にアップされています。

---

## 爆速化：WebP変換（強く推奨）

JPG/PNG をそのまま使うよりも、**WebP形式に変換するだけで読み込みが40〜60%速くなります**。
画質はほぼ変わりません（quality=95の高品質設定）。

### セットアップ（初回のみ）

```bash
pip install Pillow
```

### 使い方

```bash
python generate.py --webp
```

これだけ。実行すると：
1. `images/*.webp` — 高品質WebPを生成
2. `images/thumbs/*.jpg` — サムネ用の120px極小画像を生成
3. `images.json` を更新

GitHubには `images/*.webp` + `images/thumbs/` + `images.json` をアップするだけ。

> 💡 元の .jpg/.png はそのままローカルに残ります。削除したい場合は手動で。

### WebP変換後の効果

| ファイル | 変換前 | 変換後 |
|---|---|---|
| 1枚あたり（例） | 3MB | 1.2MB |
| サムネ | 読み込みなし | 3〜5KB/枚 |

30枚のポートフォリオなら、サムネバーだけで **90MB → 150KB** になります。

---

## よくある質問

**Q: generate.py を実行したら `python: command not found` と出た**
→ `python3 generate.py` で試してください（Mac/Linux）

**Q: images.json を手動で編集してもいいですか？**
→ OK です。ただし次回 `generate.py` を実行すると上書きされます。

**Q: タイトルや年を設定したい**
→ `images.json` を直接編集してください:
```json
{ "file": "work-01.jpg", "title": "息をひそめて", "year": "2023" }
```

**Q: 写真の枚数に制限はありますか？**
→ ありません。30枚以上でもサムネイルで絞り込めます。
