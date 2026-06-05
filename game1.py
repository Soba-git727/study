import random
import sys
n=str(input("what's your name:"))
print("good luck",n)
worlds=["Long","SOVA","Khoi"]
word=random.choice(worlds).lower()   
print("GUEST THE WORLD")
answer=""
turn=12
true=0
print(word)
while turn >0:
    for char in word:
        guessed=input("choose a char:").lower()
        if guessed in char:
            print ("there's a",guessed)
            true+=1
            answer+=guessed
        else:
            print("wrong")
            turn-=1
        if turn == 0:
            print("you losed")
            sys.exit(1)
        
        if true == len(word):
            print ("you win")
            print ( "the word is ", answer)
            sys.exit(2)


