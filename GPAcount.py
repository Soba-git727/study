tinchitichluy=0
diemtichluy=0


while True:
    #Nhap input
    while True:
        try:
            QTH=float(input("Diem qua trinh hoc: "))
            THI=float(input("Diem thi:"))
            TINCHI=int(input("Tin chi mon hoc"))
            break
        except ValueError:
            print("ERROR, please try again")
    #Tinh toan
    if QTH >=0 and THI>=0:
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

        ask=input("done?(an yes neu xong hoac an ngau nhien 1 phim neu chua xong)").strip().lower()
        #in ket qua
        if ask =="yes":
            print("GPA cua ban la: ",diemtichluy/tinchitichluy)
            print("TIN CHI TICH Luy",tinchitichluy)
            print("diem tich luy :",diemtichluy)
            print("tong",TONG)
            break
        else:
            raise("ERROR")
    
