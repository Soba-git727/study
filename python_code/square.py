def square_test():
    test_case=int(input("test case: "))
    for _ in range(test_case):
        a, b, c, d=map(int, input().split())
        if a==b==c==d:
            print("YES")
        else:
            print("NO")
                
square_test()