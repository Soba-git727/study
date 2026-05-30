list=[3,1,4,8,2]
i=int(input("i="))
for value,position in enumerate(list):
    for value in list:
        if value==i:
            print(list[value])
        else:
            position +=1
if position==len(list):
        print("false")
