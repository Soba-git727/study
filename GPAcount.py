tinchitichluy=0
diemtichluy=0
count=1
final=0

while True:
    #Nhap input
    while True:
        try:
            print(f"mon thu {count}:")
            QTH=float(input("Diem qua trinh hoc: ")).strip()
            THI=float(input("Diem thi: ")).strip()
            TINCHI=float(input("Tin chi mon hoc: ")).strip()
            break
        except ValueError:
            print("ERROR, please try again")
    #Tinh toan
    if QTH >=0 and THI>=0 and TINCHI>0:
        tinchitichluy=tinchitichluy+TINCHI
        TONG =(QTH + THI)/2
        if TONG >= 8.5:
            TONG=4.0
        elif TONG >= 8.0:
            TONG=3.5
        elif TONG>=7.0:
            TONG=3.0
        elif TONG>=6.5:
            TONG=2.5
        elif TONG>=5.5:
            TONG=2.0
        elif TONG>=5.0:
            TONG=1.5
        elif TONG>=4.0:
            TONG=1.0
        elif TONG >4.0:
            TONG=0
        DIEM=(TONG*TINCHI)
        diemtichluy=diemtichluy+DIEM
        
        while True:
            ask=str(input("done?(an YES neu xong hoac NO neu chua xong): ")).strip().lower()
            #in ket qua
            if ask =="yes":
                print("GPA cua ban la: ",diemtichluy/tinchitichluy)
                print("TONG TIN CHI DAT DUOC:",tinchitichluy)
                final=1
                break
            elif ask=="no":
                count+=1
                break
            else:
                print("ERROR,please try again")
        if final==1:
            break
            
    else:
        print("ERROR,please try again")
    
