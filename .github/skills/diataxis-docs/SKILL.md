---
name: diataxis-docs
description: "Use when: ユーザー要件、Plan成果物、Reference Draft、ADR、作業手順書、既存docsをもとに、DiátaxisのTutorial / How-to / Reference / Explanationへ技術ドキュメントを分類・作成・レビュー・分割・再分類するとき。API仕様、スキーマ、エラー形式をReference Draftに整理するとき、実装タスクをHow-toまたはtasksに分解するとき、背景説明や設計意図をExplanationとして整理するとき、ADR候補を抽出するとき。"
argument-hint: "分類・作成・レビューしたい要件、Plan成果物、Reference Draft、ADR、作業手順書、または既存ドキュメント"
---

# Diátaxis Docs

このSkillは、ユーザー要件、Plan成果物、Reference Draft、ADR、作業手順書、既存ドキュメントをもとに、技術ドキュメントをDiátaxisの4分類に整理し、必要なドキュメントの下書き・レビュー・再分類・分割を支援するために使う。

実装コードは変更しない。ドキュメントの分類、作成、レビュー、分割、関連文書の提案に集中する。

## このSkillを使うべき場面

### 使う

- ユーザー要件から必要なドキュメントを分類するとき
- PlanフェーズでReference Draftを作るとき
- API仕様、スキーマ、エラー形式、設定値などをReferenceとして整理するとき
- 実装タスクをHow-toまたは`tasks/`に分解するとき
- 背景説明や設計意図をExplanationとして整理するとき
- 既存ドキュメントがDiátaxisの分類に合っているかレビューするとき
- Tutorial / How-to / Reference / Explanation が混ざっている文書を分割するとき
- ADR候補を見つけ、`adr-writing` skillにつなぐ必要があるとき

### 使わない

- 実装コードそのものを変更するとき
- 1つの後戻りしにくい設計判断をADRとして確定・記録するとき
- 単なる日次メモや一時的なTODOを書くとき
- ユーザー要件や設計判断を、根拠なしに勝手に確定するとき

## Diátaxisの基本分類

Diátaxisでは、技術ドキュメントを以下の4種類に分ける。

### Tutorial

- 学習のための文書
- 初学者を安全に成功体験へ導く
- 目的は「学ぶこと」
- 例: FastAPIで最初のToDo APIを作る

Tutorialでは、学習者が迷わず進められることを優先する。厳密な仕様一覧や多くの分岐はReferenceやHow-toへリンクする。

### How-to guide

- 実務上の具体的な作業を達成するための文書
- 目的は「特定の問題を解くこと」
- すでに基本を知っているユーザーを想定する
- 例: ToDoに締切日を追加する、テストを実行する

How-toでは、作業の流れ、確認方法、失敗時の対処に集中する。長い背景説明や完全な仕様一覧は含めない。

### Reference

- 正確な仕様・一覧・型・引数・戻り値・制約を記述する文書
- 目的は「確認すること」
- 手順や背景説明を混ぜない
- 例: APIエンドポイント一覧、リクエスト/レスポンススキーマ、エラーコード一覧

Referenceでは、事実と仕様を構造化して書く。なぜその仕様にしたかはExplanationまたはADRへ分ける。

### Explanation

- 背景・理由・概念・設計思想を説明する文書
- 目的は「理解を深めること」
- 直接の作業手順ではない
- 例: なぜこのディレクトリ構成なのか、なぜSQLiteから始めるのか

Explanationでは、背景理解や概念整理を扱う。ただし、1つの後戻りしにくい設計判断を扱っている場合はADR候補として扱う。

## Diátaxis Compassによる分類ルール

文書を分類するときは、以下の2つの問いを使う。

### Question 1

この文書は、ユーザーの行動を助けるものか、理解・確認を助けるものか？

- 行動を助ける: practical steps, doing
- 理解・確認を助ける: facts, concepts, thinking

### Question 2

ユーザーは学習中か、実務中か？

- 学習中: acquisition of skill
- 実務中: application of skill

### 分類

| 軸 | ユーザー状態 | 分類 |
|---|---|---|
| 行動を助ける | 学習中 | Tutorial |
| 行動を助ける | 実務中 | How-to guide |
| 理解/確認を助ける | 実務中 | Reference |
| 理解を助ける | 学習中 | Explanation |

## 実装前Planフェーズでの優先順位

実装前は、すべてのDiátaxis文書を作ろうとしない。

### 優先する

1. Reference Draft
   - 何を作るかを固定する
   - API仕様、スキーマ、エラー形式、設定値などを明確にする
   - 実装前は「契約の下書き」として扱う

2. 必要に応じたExplanation
   - 設計背景や全体像を説明する
   - ただし、重要な設計判断はADRに分ける

3. How-to / tasks
   - Copilotに渡す作業手順書として整理する
   - 実装タスク単位に分ける
   - 必要に応じて`tasks/*.md`へ分離する

### 後回しでよい

- Tutorial
  - 初学者向けの学習文書は、実装後に必要なら作る

## ADR Skillとの関係

このSkillはADRを直接作成するためのものではない。

ただし、以下を見つけたらADR候補として扱い、`adr-writing` skillの利用を提案する。

### ADR候補

- DB選定
- フレームワーク選定
- 認証方式
- ディレクトリ構成
- レイヤー構造
- データモデルの重要な選択
- API設計の後戻りしにくい判断
- セキュリティ、性能、保守性、テスト容易性に大きく影響する判断

### DiátaxisとADRの役割

- Reference: 何を作るか
- Explanation: 背景や概念
- ADR: なぜその設計判断にしたか
- How-to / tasks: どう作業するか

## 保存場所

以下のディレクトリを使う。

```text
docs/
  tutorials/
  how-to/
  reference/
  explanation/
  adr/

tasks/
```

### ファイル名

- 英語のkebab-caseにする
- 内容が分かる名前にする

例:

- `docs/reference/todo-api.md`
- `docs/how-to/add-due-date-to-todo.md`
- `docs/tutorials/build-first-todo-api.md`
- `docs/explanation/todo-architecture-overview.md`
- `tasks/001-create-todo-api.md`

## Reference Draft作成ルール

Referenceは、仕様を確認するための文書として書く。

### 含める

- APIエンドポイント
- HTTPメソッド
- パス
- Query parameters
- Request body
- Response body
- Status codes
- Error format
- Validation rules
- Pagination
- Sorting
- Filtering
- Authentication requirements
- Examples

### 書かない

- なぜその設計にしたか
- 長い背景説明
- 実装手順
- 学習用の長いチュートリアル
- Copilotへの作業指示

Reference Draftは、実装前は「契約の下書き」として扱う。実装後は、実装結果と照合して更新する。

## How-to作成ルール

How-toは、具体的な作業を達成するための文書として書く。

### 含める

- 目的
- 前提条件
- 手順
- 確認方法
- 失敗時の対処
- 関連Referenceへのリンク

### 書かない

- 長い設計背景
- API仕様の完全な一覧
- 初学者向けの基礎説明
- ADRに書くべき判断理由

## Tutorial作成ルール

Tutorialは、学習者を安全に成功体験へ導くための文書として書く。

### 含める

- 学習目標
- 完成イメージ
- 前提条件
- 手順
- 動作確認
- 次に読む文書

### 特徴

- 初学者が迷わないようにする
- 余計な分岐を入れすぎない
- まず成功体験を優先する
- 厳密な仕様一覧はReferenceへリンクする

## Explanation作成ルール

Explanationは、理解を深めるための文書として書く。

### 含める

- 背景
- 問題意識
- 概念説明
- 設計の全体像
- 他文書へのリンク
- 関連ADRへのリンク

### 書かない

- 詳細なAPI一覧
- 実装手順だけの文章
- 1つの重要な設計判断だけを扱う文書

重要: 1つの後戻りしにくい設計判断を扱っている場合は、ExplanationではなくADRにする。

## 作業手順

このSkillが呼ばれたら、次の順番で作業する。

### Step 1: 入力を読む

次を確認する。

- ユーザー要件
- 既存`docs/`
- `docs/reference/`
- `docs/explanation/`
- `docs/how-to/`
- `docs/tutorials/`
- `docs/adr/`
- `tasks/`
- 既存コード構成

### Step 2: 必要な文書を洗い出す

次の観点で必要な文書を整理する。

- 仕様として残すべきもの
- 作業手順として残すべきもの
- 背景説明として残すべきもの
- 学習用に残すべきもの
- ADRに分けるべきもの

### Step 3: Diátaxis Compassで分類する

各文書候補について、次を判定する。

- 行動か、理解/確認か
- 学習中か、実務中か

### Step 4: 文書を作成またはレビューする

- Referenceなら仕様中心
- How-toなら作業中心
- Tutorialなら学習体験中心
- Explanationなら背景理解中心

### Step 5: 混ざっている文書を分割する

- Referenceの中に長い背景説明があればExplanationへ移す
- How-toの中にAPI仕様一覧があればReferenceへ移す
- Tutorialの中に実務上の分岐が多ければHow-toへ移す
- Explanationの中に後戻りしにくい決定事項があればADR候補として出す
- 1つの文書に複数のユーザーニーズが混ざっている場合は分割する

### Step 6: 出力する

以下を出力する。

- Proposed file path
- Document type
- Document content
- Why this belongs to this Diátaxis category
- Related documents
- ADR candidates, if any
- Open questions, if any

## 出力スタイル

- Markdownで出力する
- 実装コードは変更しない
- 設計判断を勝手に確定しない
- 不明点はOpen questionsに残す
- ユーザーが日本語で相談している場合、本文は日本語でよい
- ファイル名やディレクトリ名は英語のkebab-caseにする
- Referenceには事実・仕様を中心に書く
- How-toには行動手順を中心に書く
- Tutorialには学習体験を中心に書く
- Explanationには背景理解を中心に書く

## テンプレート

- Reference: [templates/reference-template.md](./templates/reference-template.md)
- How-to: [templates/how-to-template.md](./templates/how-to-template.md)
- Tutorial: [templates/tutorial-template.md](./templates/tutorial-template.md)
- Explanation: [templates/explanation-template.md](./templates/explanation-template.md)
- 分類チェックリスト: [templates/doc-classification-checklist.md](./templates/doc-classification-checklist.md)

## サンプル

- Reference Draft: [examples/reference-todo-api.md](./examples/reference-todo-api.md)
- How-to: [examples/how-to-add-due-date-to-todo.md](./examples/how-to-add-due-date-to-todo.md)
- Tutorial: [examples/tutorial-build-first-todo-api.md](./examples/tutorial-build-first-todo-api.md)
- Explanation: [examples/explanation-todo-architecture-overview.md](./examples/explanation-todo-architecture-overview.md)

## 品質チェック

成果物を作成またはレビューした後、次を自己チェックする。

- `SKILL.md` に`name`と`description`がある
- `name`は`diataxis-docs`になっている
- `description`に「いつ使うべきか」が書かれている
- Tutorial / How-to / Reference / Explanation の違いが明確
- Diátaxis Compassの分類ルールがある
- Reference DraftをPlanフェーズで優先する方針がある
- ADRとDiátaxisの役割が混ざっていない
- ADR候補を検出したら`adr-writing` skillへつなぐルールがある
- 実装コードを変更しないルールがある
- templatesが4分類分ある
- examplesが4分類分ある
- 混ざった文書を分割するルールがある
- Referenceには仕様、How-toには作業、Tutorialには学習、Explanationには背景を書くルールがある
