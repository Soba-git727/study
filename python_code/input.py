name=str(input("what's your name:"))

with open("name.text","a") as file:
    file.write(f"{name}\n")
