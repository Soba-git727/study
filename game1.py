import random
import sys
import re
n=str(input("what's your name:"))
print("good luck",n)
worlds=[
    "cat", "dog", "sun", "moon", "star", "tree", "book", "game", "code", "play",
    "love", "life", "time", "home", "work", "city", "fish", "bird", "lion", "king",
    "queen", "fire", "water", "wind", "earth", "ship", "boat", "car", "bike", "road"
    "python", "java", "script", "coding", "program", "hacker", "system", "network",
    "server", "client", "database", "matrix", "cypher", "robot", "engine", "device",
    "screen", "mouse", "keyboard", "laptop", "mobile", "pixel", "vector", "binary",
    "logic", "circuit", "hardware", "software", "website", "internet",
   
    "apple", "banana", "orange", "grape", "melon", "flower", "garden", "forest",
    "stream", "river", "ocean", "beach", "desert", "castle", "palace", "temple",
    "bridge", "tunnel", "market", "school", "office", "doctor", "driver", "worker",
    "player", "winner", "shadow", "spirit", "ghost", "dragon",

    "computer", "keyboard", "language", "software", "hardware", "internet", "security",
    "universe", "galaxy", "astronaut", "spaceship", "adventure", "journey", "mountain",
    "beautiful", "wonderful", "dangerous", "mysterious", "chocolate", "elephant",
    "dinosaur", "crocodile", "butterfly", "lightning", "hurricane", "tomorrow",
    "yesterday", "calendar", "dictionary", "education", "university", "champion",
    
    "hello", "world", "happy", "smile", "coffee", "music", "guitar", "piano", "artist", "camera",
    "nature", "summer", "winter", "spring", "autumn", "clouds", "shadow", "silver", "golden", "diamond",
    "crystal", "energy", "future", "history", "science", "physics", "hunter", "wizard", "warrior", "knight",
    "secret", "puzzle", "riddle", "legend", "mythos", "planet", "comet", "meteor", "rocket", "island",
    "jungle", "safari", "valley", "canyon", "palace", "museum", "cinema", "studio", "canvas", "sketch"


]
word=random.choice(worlds).lower()   
print("GUEST THE WORLD")
print("you have 12 turns left")
answer=''
turn=12
true=0

while turn >0:
    for char in word:
        
        if char in answer:
            print(char )
            
        else:
            print("_")
    if true == len(word):
                print ("you win")
                print ( "the word is",word)
                sys.exit(2)
    while True:    
        guessed=input("choose a char:").lower()
        if re.search(r"^[a-z]{1}$",guessed):
            answer+=guessed
            break
        else:
            print("only choose 1 character")

        
    multiple_correct_choices=word.count(guessed)
    
    if guessed in word:
        print (f"there's {multiple_correct_choices}",guessed)
        true+=multiple_correct_choices
            
    if guessed not in word:
        print("wrong")
        turn-=1
        print (f"you have {turn} turn left ")
        
    if turn == 0:
        print("you losed")
        print("the word is",word)
        sys.exit(1)
    
        
    


