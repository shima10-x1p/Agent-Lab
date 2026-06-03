---
title: "ADR-0008: FastAPI Hexagonal Architecture for the Microservice"
status: "Proposed"
date: "2026-06-03"
authors: "Backend Team / Copilot"
tags: ["architecture", "decision", "fastapi", "hexagonal", "ddd", "openapi", "dependency-boundaries"]
supersedes: ""
superseded_by: ""
---

## Status

Accepted

## Context

このマイクロサービスは Python + FastAPI で実装されるが、API 入口、業務ルール、永続化、外部 API、生成コードが同じ層に混ざると、機能追加のたびに依存関係が壊れやすい。特に、OpenAPI 由来の DTO、SQLAlchemy などの技術詳細、業務ロジックを同じ場所に置くと、テスト容易性と変更容易性が低下する。

また、このプロジェクトでは OpenAPI を仕様の起点として扱い、実装はその契約に追従させる方針である。したがって、HTTP 入出力、ユースケース、ドメインルール、DB 実装を明確に分離し、依存方向を内側へ固定する必要がある。

- **CTX-001**: FastAPI は HTTP の入口としてのみ使い、業務ロジックの置き場にはしない必要がある。
- **CTX-002**: DB や外部 API などの技術詳細は、将来差し替え可能な形で隔離したい。
- **CTX-003**: OpenAPI 由来の生成コードは便利だが、ドメイン層へ流し込むと境界が崩れやすい。
- **CTX-004**: テストはレイヤーごとに分離しやすく、ユースケース単位で検証できる構造が望ましい。
- **CTX-005**: このリポジトリでは、既存の ADR で runtime、contract-first、persistence、error handling、non-functional boundaries を個別に定めているため、それらを束ねる構造的な決定が必要である。

## Decision

このマイクロサービスは、`domain` と `application` を中心に置くヘキサゴナルアーキテクチャで構成する。`presentation/fastapi` は HTTP 入出力と依存注入に限定し、`infrastructure` は DB 実装や外部連携を担当し、`bootstrap` はアプリケーション全体の組み立てを担当する。`generated/` は OpenAPI 由来の DTO の保管場所として扱い、`domain` と `application` から直接 import しない。

- **DEC-001**: 中心レイヤーは `domain` と `application` とする。
- **DEC-002**: `presentation/fastapi` に FastAPI ルーター、`Depends`、DTO 変換、例外ハンドリングを集約する。
- **DEC-003**: `application/ports` に repository などの interface を定義し、`infrastructure` で実装する。
- **DEC-004**: `infrastructure` に SQLAlchemy model、永続化実装、外部 API クライアント、clock 実装を配置する。
- **DEC-005**: `bootstrap` に設定読み込み、DI container、FastAPI app factory を集約し、`main.py` は薄く保つ。
- **DEC-006**: `generated/` のコードは DTO としてのみ扱い、業務ロジックの中心に置かない。

この構成により、FastAPI や DB の都合に業務ルールが引きずられにくくなり、変更の波及を外側に閉じ込めやすくなる。

## Consequences

### Positive

- **POS-001**: 業務ルールが `domain` に集約されるため、FastAPI や DB の変更に対して安定しやすい。
- **POS-002**: `application` がユースケース単位になるため、HTTP 以外の入口でも再利用しやすい。
- **POS-003**: repository interface と実装が分かれることで、永続化方式の差し替えやモック化が容易になる。
- **POS-004**: DTO と domain model の境界が明確になるため、生成コードの影響範囲を限定できる。
- **POS-005**: `bootstrap` に組み立てを集約することで、依存関係の把握と初期化順序の管理がしやすい。

### Negative

- **NEG-001**: 初期構成のファイル数が増え、単純な CRUD 実装でも見通しが悪く感じられる可能性がある。
- **NEG-002**: DTO、use case、domain model、repository 実装の間で変換処理が増える。
- **NEG-003**: 小規模な変更でも複数レイヤーにまたがるため、学習コストが上がる。
- **NEG-004**: 厳密に境界を守るため、短期的には実装速度がやや落ちる。
- **NEG-005**: 生成コードの扱いを誤ると、境界逸脱のレビュー負荷が発生する。

## Alternatives Considered

### 伝統的なレイヤード構成にする

- **ALT-001**: **説明**: `api / service / repository` のような単純なレイヤー分割にし、FastAPI と DB 実装を近い場所に置く。
- **ALT-002**: **不採用理由**: 技術詳細が中心に入りやすく、業務ルールと HTTP / DB の関心が混ざりやすい。

### FastAPI と SQLAlchemy を直接中心に置く

- **ALT-003**: **説明**: Router から直接 DB を操作し、モデルと API 変換も同一層で処理する。
- **ALT-004**: **不採用理由**: 実装は速いが、変更容易性とテスト容易性が低く、将来の差し替えに弱い。

### 何もしないで機能ごとに実装する

- **ALT-005**: **説明**: 明示的な構造を定めず、機能追加時に都度ファイル配置を決める。
- **ALT-006**: **不採用理由**: 一貫性が失われやすく、依存方向の逸脱を後から修正するコストが高い。

## Implementation Notes

- **IMP-001**: 新しい機能は `domain → application → infrastructure → presentation → bootstrap` の順で実装し、逆向きの import が入らないようにする。
- **IMP-002**: `generated/` のモデルは HTTP DTO としてのみ利用し、use case には必要なプリミティブ値だけ渡す。
- **IMP-003**: repository interface は `application/ports` に置き、use case はその interface のみに依存させる。
- **IMP-004**: `main.py` は `create_app()` を呼ぶだけにし、アプリ構成は `bootstrap/app_factory.py` と `bootstrap/container.py` に寄せる。
- **IMP-005**: 追加時には、router に業務ロジックが入っていないか、domain に Pydantic / FastAPI 依存がないかをレビュー観点に含める。
- **IMP-006**: 成功基準は、レイヤーごとの単体テストが書きやすく、依存方向の違反がレビューで即座に検出できる状態であることとする。

## References

- **REF-001**: `./adr-0001-runtime-and-package-management.md`
- **REF-002**: `./adr-0002-openapi-contract-first.md`
- **REF-003**: `./adr-0003-persistence-strategy.md`
- **REF-004**: `./adr-0004-todo-api-behavior.md`
- **REF-005**: `./adr-0005-date-and-time-conventions.md`
- **REF-006**: `./adr-0006-error-handling-and-response-normalization.md`
- **REF-007**: `./adr-0007-non-functional-boundaries.md`
- **REF-008**: `../spec/openapi.yaml`
