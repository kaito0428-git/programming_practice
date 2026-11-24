# 保守作業記録アプリの画面部分
# 起動方法: streamlit run app.py
from datetime import datetime

import streamlit as st

import db

# ページの基本設定
st.set_page_config(page_title="保守作業記録", layout="wide")

# 起動時にテーブルを準備する
db.init_db()
# データベースが空ならサンプル記録を入れる(公開デモ用)
db.seed_sample_data()



def make_report(log):
    """作業記録1件から、顧客向けの作業報告書の文章を作る"""
    # 「2026-11-24 10:00」を「11月24日 10時00分」の形に変換する
    work_at = datetime.strptime(log["work_at"], "%Y-%m-%d %H:%M")
    when = f"{work_at.month}月{work_at.day}日 {work_at.hour}時{work_at.minute:02d}分"

    # 1文目: いつ・誰の・何について・どんな事象か
    if log["symptom"]:
        lines = [f"{when}、{log['customer']}様の{log['device']}について、{log['symptom']}の事象を確認しました。"]
    else:
        lines = [f"{when}、{log['customer']}様の{log['device']}について、作業を行いました。"]

    # 2文目: 原因と処置(空の項目は文に入れない)
    cause = log["cause"]
    action = log["action"]
    if cause and action:
        lines.append(f"原因は{cause}で、{action}を実施しました。")
    elif cause:
        lines.append(f"原因は{cause}でした。")
    elif action:
        lines.append(f"{action}を実施しました。")

    report = "\n".join(lines)

    # 残課題があれば「今後の対応」として追記する
    if log["remaining"]:
        report += f"\n\n【今後の対応】\n{log['remaining']}"

    return report


st.title("保守作業記録")
st.warning("デモ用アプリです。実在の顧客情報は入力しないでください。")

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

    # 絞り込み条件の入力欄(横に並べる)
    col1, col2 = st.columns(2)
    status_filter = col1.selectbox("ステータス", ["すべて", "対応中", "完了"])
    device_keyword = col2.text_input("機器名キーワード")

    logs = db.get_logs(status_filter, device_keyword.strip())

    if not logs:
        st.info("条件に合う記録がありません。")
    else:
        st.write(f"{len(logs)} 件")
        st.caption("行の左端をクリックして選ぶと、下に作業報告書の文章が表示されます。")

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
        # on_select="rerun" で行を選べるようにし、選んだ結果を event で受け取る
        event = st.dataframe(
            table,
            width="stretch",  # 画面の横幅いっぱいに表示
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )

        # 行が選ばれていれば、その記録の報告書を表示する
        selected_rows = event.selection.rows
        if selected_rows:
            log = logs[selected_rows[0]]
            st.subheader("作業報告書")
            # st.code は右上にコピーボタンが付くので、そのまま貼り付けに使える
            st.code(make_report(log), language=None, wrap_lines=True)
