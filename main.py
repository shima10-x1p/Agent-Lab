"""ローカル開発用の起動エントリーポイント。"""

import uvicorn

from agent_lab.main import app


def main() -> None:
    """開発用サーバーを起動する。"""
    uvicorn.run(app, host="127.0.0.1", port=3000)


if __name__ == "__main__":
    main()
