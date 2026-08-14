import random
1

janken =random.randint(0, 9)
if janken == 0:
    print("グーで勝ち")

elif janken == 1:
    print("チョキで勝ち")

elif janken == 2:
    print("パーで勝ち")

elif janken == 3:
    print("グーで負け")

elif janken == 4:
    print("チョキで負け")

elif janken == 5:
    print("パーで負け")

else:
    print("あいこ")

    2
zanken = random.randint(0, 9)
if zanken > 5:
    print("勝ち")
elif zanken == 5:
    print("あいこ")
elif zanken <= 4:
    print("負け")

