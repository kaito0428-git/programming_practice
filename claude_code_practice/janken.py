import random

HANDS = {"1": "グー", "2": "チョキ", "3": "パー"}


def get_player_hand():
    """プレイヤーの手を入力させる。q なら None を返す。"""
    while True:
        try:
            choice = input("手を選んでください (1:グー 2:チョキ 3:パー q:終了): ")
        except EOFError:
            return None
        choice = choice.strip().lstrip("﻿")
        if choice.lower() == "q":
            return None
        if choice in HANDS:
            return choice
        print("1, 2, 3, q のいずれかを入力してください。")


def get_cpu_hand():
    return random.choice(list(HANDS))


def judge(player, cpu):
    """'draw' / 'win' / 'lose' を返す。"""
    result = (int(player) - int(cpu)) % 3
    return {0: "draw", 2: "win", 1: "lose"}[result]


def main():
    stats = {"win": 0, "lose": 0, "draw": 0}
    streak = 0
    max_streak = 0
    messages = {"win": "あなたの勝ち！", "lose": "あなたの負け…", "draw": "あいこ"}

    while True:
        player = get_player_hand()
        if player is None:
            break
        cpu = get_cpu_hand()
        result = judge(player, cpu)
        stats[result] += 1
        # あいこでは連勝は途切れない
        if result == "win":
            streak += 1
            max_streak = max(max_streak, streak)
        elif result == "lose":
            streak = 0
        print(f"あなた: {HANDS[player]} / CPU: {HANDS[cpu]} → {messages[result]}")
        print(f"現在 {streak}連勝中\n")

    print(f"戦績: {stats['win']}勝 {stats['lose']}敗 {stats['draw']}分")
    print(f"最大連勝数: {max_streak}")


if __name__ == "__main__":
    main()
