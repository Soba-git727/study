list=[3,1,4,8,2]
i=int(input("i="))
for position,value in enumerate(list):
    if value==i:
        print(position)
if position==len(list):
        print("false")
