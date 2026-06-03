"""ドメインエラー定義。"""


class DomainError(Exception):
    """ドメインエラーの基底クラス。"""


class TodoNotFoundError(DomainError):
    """指定した ToDo が見つからない場合のエラー。"""

    def __init__(self, todo_id: str) -> None:
        """エラーを初期化する。

        Args:
            todo_id: 見つからなかった ToDo の識別子。
        """
        super().__init__("指定したToDoが見つかりません。")
        self.todo_id = todo_id
