---
name: adr-writing
description: "Use when: Architecture Decision Record（ADR）を作成・レビューする、ADR候補を抽出する、ユーザー要件・Plan成果物・Reference Draft・既存設計から後戻りしにくい設計判断を記録する必要があるとき。"
argument-hint: "ADRにしたい要件、Plan成果物、Reference Draft、既存設計、またはレビュー対象ADR"
---

# ADR Writing

このSkillは、ユーザー要件・Plan成果物・Reference Draft・既存設計をもとに、重要な設計判断をArchitecture Decision Record（ADR）として整理・作成・レビューするために使う。

ADRは実装手順書ではなく、「なぜその判断をしたのか」を後から追跡できるようにする判断の記録である。

## このSkillを使うべき場面

### 使う

- フレームワーク、DB、認証方式、API設計、データモデル、ディレクトリ構成、レイヤー構造などを決めるとき
- 保守性、拡張性、セキュリティ、性能、テスト容易性、運用コストに影響する判断があるとき
- 後から変更するとコストが大きい判断があるとき
- 複数の選択肢があり、判断理由を残す価値があるとき
- Reference Draftや作業手順書に影響する判断があるとき
- Planning AgentがPlan成果物を作る途中で、設計判断の記録が必要になったとき
- 既存ADRをレビューし、判断・根拠・影響・未確定事項が十分に書かれているか確認するとき

### 使わない

- 一時的なTODO
- 今日だけの作業メモ
- 関数名・変数名レベルの細かい実装判断
- 単純なバグ修正
- 実装手順そのもの
- まだ判断材料が足りない曖昧な思いつき

## ADR作成時の原則

- 1つのADRには1つの設計判断だけを書く。
- 複数の判断が混ざっている場合は、複数のADRに分ける。
- ADRは実装手順書ではなく、判断の記録として書く。
- `Context` には、なぜその判断が必要になったのかを書く。
- `Decision` には、何を採用するのかを明確に書く。
- `Consequences` には、良い結果だけでなく、悪い結果やトレードオフも書く。
- `Considered Options` には、検討した代替案とPros/Consを書く。
- 不明点や未確定事項がある場合は、勝手に確定せず明記する。
- 新規ADRの `Status` は原則 `Proposed` にする。
- ユーザーが明示的に決定済みと言った場合だけ `Accepted` にする。
- `Accepted` 済みADRは原則として内容変更しない。
- 判断が変わる場合は新しいADRを作り、古いADRを `Superseded` として扱う。
- 既存ADRがある場合は、先に `docs/adr/` を確認する。
- 関連するReference Draft、作業手順書、既存ADRがあればリンクする。

## ADRの保存場所とファイル名

### 保存場所

ADRは原則として `docs/adr/` に保存する。

### ファイル名

ファイル名は、連番 + kebab-case にする。

例:

- `docs/adr/0001-use-sqlite-for-initial-database.md`
- `docs/adr/0002-use-layered-architecture.md`
- `docs/adr/0003-use-status-enum-for-todo-state.md`

### 連番の決め方

- `docs/adr/` に既存ADRがある場合は、最大番号の次を使う。
- 既存ADRがない場合は `0001` から始める。
- ファイル名には判断内容が分かる短い英語を使う。

## ADRテンプレート

ADRを書くときは、[adr-template.md](./adr-template.md) の構成に従う。

必ず含める主な項目:

- `Status`
- `Date`
- `Context`
- `Decision Drivers`
- `Considered Options`
- `Decision`
- `Consequences`
- `Confidence`
- `Revisit When`
- `Related Documents`

## 作業手順

### Step 1: 入力を確認する

次の入力を確認する。

- ユーザー要件
- Reference Draft
- 既存ADR
- 既存ディレクトリ構成
- 作業手順書
- 実装予定の変更内容

不足している情報があり、ADRの判断に影響する場合は、勝手に補完せずユーザーに確認する。

### Step 2: ADR候補を抽出する

次の観点でADR候補を探す。

- 後戻りしにくい判断があるか
- 複数の選択肢がある判断があるか
- Reference Draftに影響する判断があるか
- 作業手順書だけでは理由が残らない判断があるか
- 保守性、拡張性、セキュリティ、性能、テスト容易性、運用コストに影響するか

### Step 3: ADRにするか判定する

ADRにする価値がある場合だけ作成する。

ADR不要の場合は、理由を短く説明する。

ADR不要になりやすい例:

- 判断が一時的である
- 実装手順の説明にすぎない
- 代替案が実質的にない
- 変更コストや設計影響が小さい

### Step 4: 1判断1ADRに分割する

複数の判断が含まれている場合は、ADRを分ける。

例:

- DB選定
- 認証方式
- レイヤー構造
- APIバージョニング

これらが同時に議論されていても、判断が独立している場合は別ADRにする。

### Step 5: ADRを書く

[adr-template.md](./adr-template.md) に従ってADRを書く。

書くときの注意:

- `Context` には、判断の背景と制約を書く。
- `Decision Drivers` には、重視する判断軸を書く。
- `Considered Options` には、採用案だけでなく代替案も書く。
- `Decision` には、採用する選択肢を明確に書く。
- `Consequences` には、Positive / Negative / Neutral or Trade-offs を分けて書く。
- `Confidence` が `Low` または `Medium` の場合は、その理由を書く。
- `Revisit When` には、判断を見直す条件を書く。
- `Related Documents` には、関連するReference Draft、既存ADR、作業手順書、tasksをリンクする。

### Step 6: 出力する

ADR作成時は、次を出力する。

- Proposed file path
- ADR content
- Why this deserves an ADR
- Related documents
- Open questions, if any

## 出力スタイル

- ADR本文はMarkdownで出力する。
- 実装コードは変更しない。
- 実装タスクが必要な場合は、`tasks/*.md` に書くべき内容として提案するだけにする。
- 断定しすぎず、判断材料が不足している箇所は `Open questions` に残す。
- ユーザーが日本語で相談している場合、ADR本文も日本語でよい。
- ファイル名やディレクトリ名は英語のkebab-caseにする。

## 既存ADRレビュー時の観点

既存ADRをレビューするときは、次を確認する。

- 1つのADRに1つの設計判断だけが書かれているか。
- `Status` が妥当か。
- `Accepted` 済みADRを直接書き換えようとしていないか。
- 判断が変わる場合に、新ADRと `Superseded` の関係で扱っているか。
- `Context` に判断が必要になった背景があるか。
- `Decision` が明確か。
- `Considered Options` に代替案とPros/Consがあるか。
- `Consequences` に悪い影響やトレードオフが含まれているか。
- `Confidence` と `Revisit When` があるか。
- Reference Draft、tasks、既存ADRなどの関連文書にリンクしているか。

## 品質チェック

ADRまたはSkill成果物を作成した後、次を自己チェックする。

- `SKILL.md` に `name` と `description` がある。
- `description` は「いつ使うべきか」が分かる文になっている。
- ADRと作業手順書の役割が混ざっていない。
- 1判断1ADRの原則が明記されている。
- `Proposed` / `Accepted` / `Superseded` の扱いが明記されている。
- `Accepted` 済みADRを直接書き換えないルールがある。
- 代替案とPros/Consを書くルールがある。
- `Consequences` に悪い影響やトレードオフを書くルールがある。
- `Confidence` と `Revisit When` がある。
- Reference Draftやtasksとの関連づけがある。
- サンプルADRが2つある。
