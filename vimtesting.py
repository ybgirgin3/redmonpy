def main(a: int):
    b = a * 10
    print(b)
    return b


import random

num = random.randint(0, 10)


ret = main(num)
print(ret)
