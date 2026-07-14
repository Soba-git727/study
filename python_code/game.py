import random
import sys
n=str(input("what's your name:"))
print("good luck",n)
worlds=["Miku","Teto","Kaito","Luka","Rin","Len"]
word=random.choice(worlds).lower()   
print("GUEST THE WORLD")
answer=""
turn=12
while turn>0:
    for char in word:
        if char in answer:
            print(f"{char}"+"", end="")
        else:
            print("_"+"")
    #player chọn chữ
    selected_char=str(input("Choose a character: ")).lower()


        




