---
title: "ADR-0003: Persistence Strategy and Entity Identifiers"
status: "Proposed"
date: "2026-06-03"
authors: "Backend Team / Copilot"
tags: ["architecture", "decision", "persistence", "sqlite", "sqlalchemy", "alembic", "uuid"]
supersedes: ""
superseded_by: ""
---

## Status

Accepted

## Context

ToDo API は小規模でも、データ永続化は将来の拡張や検証を考えると無視できない。今回の要件では認証は不要だが、作成・更新・削除があるため、状態を安定して保持できる層が必要である。

- **CTX-001**: 開発初期はシンプルさが重要だが、実装の交換可能性は残したい。
- **CTX-002**: 永続化方式は、学習用途の軽さとマイクロサービスとしての実用性のバランスを取る必要がある。
- **CTX-003**: ID は仕様例の文字列形式を踏まえつつ、実運用で衝突しにくいものが望ましい。

## Decision

開発・初期運用の永続化には SQLite を採用し、データアクセス層は SQLAlchemy 2.x、スキーマ管理は Alembic を使う。エンティティ ID は UUID を採用し、DB は永続化専用の責務に絞る。

- **DEC-001**: 永続化は SQLite から始める。
- **DEC-002**: ORM は SQLAlchemy 2.x を採用する。
- **DEC-003**: マイグレーションは Alembic で管理する。
- **DEC-004**: ToDo の識別子は UUID を使う。

SQLite は導入が簡単で、ローカル開発とテストに向いている。一方で、データ層を SQLAlchemy + Alembic に分けておけば、将来 PostgreSQL へ移行する際もアプリケーション層の変更を最小限に抑えられる。UUID を使うことで、クライアントに推測しやすい連番を露出せず、将来の分散化にも耐えやすい。

## Consequences

### Positive

- **POS-001**: SQLite により、セットアップが簡単でローカル開発が速い。
- **POS-002**: SQLAlchemy 2.x により、SQL を隠しすぎず、かつ実装の交換可能性を保てる。
- **POS-003**: Alembic により、スキーマ変更履歴を追跡できる。
- **POS-004**: UUID は衝突リスクが低く、ID 採番の中心化を避けられる。
- **POS-005**: DB 方針を明確にしたことで、テスト用のデータ準備が安定する。

### Negative

- **NEG-001**: SQLite は本番の高並行ワークロードには適さず、将来 PostgreSQL への移行が必要になる可能性が高い。
- **NEG-002**: SQLAlchemy と Alembic により、軽量実装よりも初期の構成要素が増える。
- **NEG-003**: UUID は文字列表現が長く、仕様例の `todo_001` より読みやすさが下がる。
- **NEG-004**: 将来 DB を差し替える際に、方言差分の調整が必要になる。

## Alternatives Considered

### PostgreSQL を最初から使う

- **ALT-001**: **説明**: 本番前提の堅牢な DB を最初から採用する。
- **ALT-002**: **不採用理由**: 今回の開始段階では過剰であり、ローカル開発の重さと運用コストが増える。

### インメモリ永続化にする

- **ALT-003**: **説明**: アプリ内メモリだけで ToDo を保持する。
- **ALT-004**: **不採用理由**: 再起動でデータが消え、CRUD API として最低限の永続性を満たせない。

### SQLModel を使う

- **ALT-005**: **説明**: ORM と Pydantic の統合がしやすい SQLModel を使う。
- **ALT-006**: **不採用理由**: 現時点では SQLAlchemy 2.x + Alembic の分離が、将来の明示的な制御と移行性に向いている。

### 仕様例どおりの採番 ID にする

- **ALT-007**: **説明**: `todo_001` のような連番文字列で ID を振る。
- **ALT-008**: **不採用理由**: 実装は簡単だが、並行処理や将来の分散構成で採番管理が複雑になる。

## Implementation Notes

- **IMP-001**: DB セッションはリクエスト単位で管理し、ユースケース層から直接 DB の詳細に依存しすぎない。
- **IMP-002**: Alembic で初期スキーマを定義し、以後の変更はマイグレーションとして記録する。
- **IMP-003**: UUID は外部公開 ID としてそのまま返し、内部採番との二重管理は避ける。
- **IMP-004**: 将来 PostgreSQL へ移行する場合に備え、SQLite 固有の SQL に依存しすぎない。

## References

- **REF-001**: `../spec/openapi.yaml`
- **REF-002**: ADR-0001: Python Runtime and Package Management
- **REF-003**: ADR-0004: Todo API Behavior and Pagination Rules
