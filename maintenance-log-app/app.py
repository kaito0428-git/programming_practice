# 保守作業記録アプリの画面部分
# 起動方法: streamlit run app.py
from datetime import datetime

import streamlit as st

import db

# ページの基本設定
st.set_page_config(page_title="保守作業記録", layout="wide")

# 起動時にテーブルを準備する
db.init_db()

st.title("保守作業記録")

# サイドバーで画面を切り替える
page = st.sidebar.radio("メニュー", ["新規登録", "一覧表示"])


# ---------- 新規登録画面 ----------
if page == "新規登録":
    st.header("作業記録の登録")

    # st.form を使うと「登録」ボタンを押すまで画面が再実行されない
    # clear_on_submit=True で登録後に入力欄を空に戻す
    with st.form("log_form", clear_on_submit=True):
        # 作業日時(日付と時刻を横に並べる)
        col1, col2 = st.columns(2)
        work_date = col1.date_input("作業日")
        work_time = col2.time_input("作業時刻")

        customer = st.text_input("顧客名 *")
        device = st.text_input("機器名 *")
        symptom = st.text_area("事象")
        cause = st.text_area("原因")
        action = st.text_area("処置内容")
        remaining = st.text_area("残課題")
        status = st.radio("ステータス", ["対応中", "完了"], horizontal=True)

        submitted = st.form_submit_button("登録")

    # 登録ボタンが押されたときの処理
    if submitted:
        # 必須項目のチェック(空白だけの入力も未入力とみなす)
        if not customer.strip() or not device.strip():
            st.error("顧客名と機器名は必須です。")
        else:
            # 日付と時刻を1つの文字列にまとめる(例: 2026-11-24 14:30)
            work_at = datetime.combine(work_date, work_time).strftime("%Y-%m-%d %H:%M")
            db.add_log(
                work_at,
                customer.strip(),
                device.strip(),
                symptom,
                cause,
                action,
                remaining,
                status,
            )
            st.success("登録しました。")


# ---------- 一覧表示画面 ----------
elif page == "一覧表示":
    st.header("作業記録の一覧")

    logs = db.get_all_logs()

    if not logs:
        st.info("まだ記録がありません。「新規登録」から登録してください。")
    else:
        st.write(f"全 {len(logs)} 件")

        # 表に表示するため、列名を日本語に置き換える
        column_names = {
            "id": "ID",
            "work_at": "作業日時",
            "customer": "顧客名",
            "device": "機器名",
            "symptom": "事象",
            "cause": "原因",
            "action": "処置内容",
            "remaining": "残課題",
            "status": "ステータス",
            "created_at": "登録日時",
        }
        table = [
            {column_names[key]: value for key, value in log.items()}
            for log in logs
        ]
        st.dataframe(table, use_container_width=True, hide_index=True)
