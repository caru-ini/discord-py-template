# discord-py-template

Language in: [[English](README.md)] [[日本語](README_ja.md)]

## 概要

リッチなログと機能を兼ね備えた、高い拡張性を持つDiscord Botテンプレート。
デフォルトでデータベース( SQLite + Prisma )が組み込まれており、簡単にデータの永続化が可能です。

## 機能

- リッチなログ出力
- 標準搭載のデータベース
- Cogベースの拡張性

## スクリーンショット

![Screenshot](/screenshot.png)

## Table of Contents

- [discord-py-template](#discord-py-template)
  - [概要](#概要)
  - [機能](#機能)
  - [スクリーンショット](#スクリーンショット)
  - [Table of Contents](#table-of-contents)
  - [インストール方法](#インストール方法)
    - [必要なもの](#必要なもの)
    - [クローン \& インストール](#クローン--インストール)
    - [Botの設定](#botの設定)
  - [Prismaの使用方法](#prismaの使用方法)
  - [Cogの追加](#cogの追加)
    - [.pyファイルでCogを追加](#pyファイルでcogを追加)
    - [フォルダでCogを追加](#フォルダでcogを追加)
  - [To Do](#to-do)
  - [ライセンス](#ライセンス)
  - [コントリビューション](#コントリビューション)

## インストール方法

### 必要なもの

- Python 3.8 or later
- Discordアカウント
- Git

### クローン & インストール

```bash
git clone https://github.com/caru-ini/discord-py-template.git
cd discord-py-template
pip install -r requirements.txt
```

### Botの設定

`.env.example`をコピーして`.env`を作成します。それぞれの値を設定してください。

```bash
cp .env.example .env
```

- `DATABASE_URL`: データベースのURL
    基本的にそのままで問題ありません。データベースの種類を変更する場合はPrismaの設定変更が必要です。
- `TOKEN`: Discord Botのトークン
    もし持っていない場合は[Discord Developer Portal](https://discord.com/developers/applications)から新しいBotを作成してください。
    Botの設定からIntentsを全て有効にしてください。

`config.json`には`Cog`の設定が記述されます。初期設定は不要です。

これでBotの準備が完了しました。以下のコマンドでBotを起動できます。

```bash
python main.py
```

## Prismaの使用方法

Prismaはデータベースの操作を簡単にするためのORMです。詳細は[Prismaの公式ドキュメント](https://www.prisma.io/docs/)を参照してください。

Tips: データベースを確認するには以下のコマンドを実行します。

```bash
prisma studio
```

`localhost:5555`にアクセスするとデータベースを確認できます。

## Cogの追加

### .pyファイルでCogを追加

`cogs`ディレクトリに新しい`.py`ファイルを作成します。以下のような形式でCogを追加できます。

Cogの使い方は[こちらの記事](https://zenn.dev/nano_sudo/articles/a00db1a55d6c4c)が参考になります。

### フォルダでCogを追加

フォルダでセットアップする場合は、通常の手順に加えて`__init__.py`を作成します。

`cogs/<Cog_name>/__init__.py`:

```python
try:
    from . import main
    setup = main.setup
except ImportError:
    raise ImportError("Function 'setup' must be implemented in the main module of the cog")
```

`cogs/<Cog_name>/main.py`に.pyファイルの手順と同様にCogを作成します。

## To Do

- [ ] Add Cog Examples
- [ ] Add UI & Embed Presets
- [ ] Add more logging options
- [ ] Add usage of prisma
- [ ] i18n support

## ライセンス

MIT License

## コントリビューション

IssueやPull Requestは大歓迎です。気軽に投稿してください。
テンプレートは特にありませんが、PRの場合は以下のルールを守ってください。

- コードの変更はPEP8に準拠していること
- 形アノテーションを記入すること
- 文字列にはダブルクォーテーションを使用すること
- テンプレートリテラルはf-stringを使用すること
