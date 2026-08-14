import random

omikuji = random.randint(0, 3)
if omikuji == 0:
    print("大吉")
elif omikuji == 1:
    print("中吉")
else:
    print("小吉")#

names = ["oda", "toyotomi","tokugawa"]
for name in names:
    print(name)

for i in range(5):
    print(i)

for i in range(1, 10, 2):
    print(i)


for i in range (1, 10):
    for j in range(1,10):
        print(f"{i} x {j} = { i * j }")

from PIL import Image