# データベース(SQLite)の処理をまとめたファイル
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

# データベースファイルの場所(このファイルと同じフォルダに作る)
DB_PATH = Path(__file__).parent / "maintenance.db"

# 日本時間(UTC+9時間)。日本はサマータイムがないので固定でよい
JST = timezone(timedelta(hours=9))


def now_jst():
    """現在の日本時間を返す(公開サーバーがUTCでも日本時間になる)"""
    return datetime.now(JST)


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


def seed_sample_data():
    """データベースが空のときだけ、デモ用のサンプル記録を3件登録する
    (顧客名・機器名はすべて架空のもの)
    """
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM work_logs").fetchone()[0]
    # すでに記録があれば何もしない(重複して登録しないため)
    if count > 0:
        return

    # (作業日時, 顧客名, 機器名, 事象, 原因, 処置内容, 残課題, ステータス)
    samples = [
        ("2026-11-10 10:00", "株式会社みどり商会", "複合機 MX-3000",
         "印刷時の紙詰まり", "給紙ローラーの摩耗",
         "給紙ローラーの交換とテスト印刷による動作確認", "", "完了"),
        ("2026-11-14 14:30", "あおば運輸株式会社", "業務用ハンディ端末 HT-500",
         "バーコードの読み取り不良", "読み取り部のレンズの汚れ",
         "レンズの清掃と読み取りテストによる動作確認", "", "完了"),
        ("2026-11-20 09:15", "さくら食品株式会社", "ネットワークスイッチ SW-24",
         "一部ポートでの通信断", "ポートの故障の疑い",
         "予備ポートへの配線変更と通信の復旧確認",
         "交換用スイッチを手配中。到着後に交換作業を実施", "対応中"),
    ]
    for sample in samples:
        # 「*」でタプルの中身を1つずつ引数として渡す
        add_log(*sample)


def add_log(work_at, customer, device, symptom, cause, action, remaining, status):
    """作業記録を1件登録する"""
    with get_connection() as conn:
        # 「?」を使うと、入力値が安全にSQLへ埋め込まれる
        conn.execute(
            """
            INSERT INTO work_logs
                (work_at, customer, device, symptom, cause, action, remaining, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (work_at, customer, device, symptom, cause, action, remaining, status,
             # 登録日時は日本時間で保存する(例: 2026-11-24 14:30:05)
             now_jst().strftime("%Y-%m-%d %H:%M:%S")),
        )


def get_logs(status="すべて", device_keyword=""):
    """作業記録を新しい順に取得する(条件を指定すると絞り込む)

    status: 「すべて」「対応中」「完了」のどれか
    device_keyword: 機器名に含まれる文字(空なら絞り込まない)
    """
    sql = "SELECT * FROM work_logs WHERE 1=1"  # 1=1 は条件を後ろに足しやすくするための書き方
    params = []

    # ステータスで絞り込む(「すべて」のときは何もしない)
    if status != "すべて":
        sql += " AND status = ?"
        params.append(status)

    # 機器名の部分一致で絞り込む(% は「任意の文字」の意味)
    if device_keyword:
        sql += " AND device LIKE ?"
        params.append(f"%{device_keyword}%")

    sql += " ORDER BY work_at DESC, id DESC"

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    # 扱いやすいように辞書のリストに変換して返す
    return [dict(row) for row in rows]
