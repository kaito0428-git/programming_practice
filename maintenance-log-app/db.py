# データベース(SQLite)の処理をまとめたファイル
import sqlite3
from pathlib import Path

# データベースファイルの場所(このファイルと同じフォルダに作る)
DB_PATH = Path(__file__).parent / "maintenance.db"


def get_connection():
    """データベースに接続する"""
    conn = sqlite3.connect(DB_PATH)
    # 結果を「列名でアクセスできる形」で受け取る設定
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """テーブルがなければ作成する(アプリ起動時に毎回呼ぶ)"""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS work_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- 連番ID
                work_at     TEXT NOT NULL,   -- 作業日時
                customer    TEXT NOT NULL,   -- 顧客名
                device      TEXT NOT NULL,   -- 機器名
                symptom     TEXT,            -- 事象
                cause       TEXT,            -- 原因
                action      TEXT,            -- 処置内容
                remaining   TEXT,            -- 残課題
                status      TEXT NOT NULL,   -- ステータス(対応中/完了)
                created_at  TEXT DEFAULT (datetime('now', 'localtime'))  -- 登録日時
            )
            """
        )


def add_log(work_at, customer, device, symptom, cause, action, remaining, status):
    """作業記録を1件登録する"""
    with get_connection() as conn:
        # 「?」を使うと、入力値が安全にSQLへ埋め込まれる
        conn.execute(
            """
            INSERT INTO work_logs
                (work_at, customer, device, symptom, cause, action, remaining, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (work_at, customer, device, symptom, cause, action, remaining, status),
        )


def get_all_logs():
    """作業記録を新しい順にすべて取得する"""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM work_logs ORDER BY work_at DESC, id DESC"
        ).fetchall()
    # 扱いやすいように辞書のリストに変換して返す
    return [dict(row) for row in rows]
