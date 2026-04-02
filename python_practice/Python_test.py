name = "Taro"
age = 20

print(f"こんにちは！私の名前は{name}です。")
print(f"年齢は{age}歳です。")

a = 15
b= 4

#足し算
c = a + b
print(c)
#引き算
d = a - b
print(d)
#掛け算
e = a * b
print(e)
#割り算
f = a / b
print(f)

first_name = "Hanako"
last_name = "Yamada"
h = first_name + last_name

print(h)
print(len(h))




score = 75
if score >= 60:
    print("合格")
else:
    print("不合格")

num = -1
if num > 0:
    print("正の数")
elif num < 0:
    print("負の数")
else:
    print("ゼロ")

n = 15
if n % 3 == 0 and n % 5 ==0:
    print("FizzBuzz")
elif n % 3 == 0:
    print("Fizz")
elif n % 5 == 0:
    print("Buzz")
else:
    print(n)

for i in range(1,11):
    print(i)

total = 0
for i in range(1, 101):
    total = total + i
print("合計:", total)

fruits = ["りんご", "バナナ", "みかん", "ぶどう"]
for fruit in fruits:
    print(f"{fruit}が好きです。")



def greet(name):
    print(f"こんにちは、{name}さん！")
greet("Taro")
greet("Hanako")

def add(a, b):
    return a + b
result = add(3, 7)
print(result)
print(add(10, 25))


def my_max(a,b,c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c
    
print(my_max(3, 7, 2))
print(my_max(10, 5, 8))
print(my_max(1, 1, 1))