class HaiPhong:
    def __init__(self,Tinh_Cach,Do_tuoi):
        self.Tinh_cach=Tinh_Cach
        self.Do_tuoi=Do_tuoi

    def __str__(self):
        attrs=",".join(f"{k},{v}" for  k,v in self.__dict__.items())
        return f"[{self.__class__.__name__}]-> {attrs}"

    @classmethod
    def get(cls):
        Tinh_Cach=input("tinh cach:")
        Do_Tuoi=input("DO tuoi:")
        extra_att= cls.extra_info()

        return cls(Tinh_Cach,Do_Tuoi,*extra_att)
    @classmethod
    def extra_info(cls):
        return()

    @property
    def Tinh_cach (self):
        return self._Tinh_cach
    @Tinh_cach.setter
    def Tinh_cach (self,Tinh_cach):
        if Tinh_cach not in ("Gay","femboy"):
            raise ValueError("Invalid input")
        self._Tinh_cach= Tinh_cach
class Long_nghien(HaiPhong): #lONG Nghien
    def __init__(self, Tinh_Cach, Do_tuoi,Game):
        super().__init__(Tinh_Cach, Do_tuoi)
        self.Game=Game
    @classmethod
    def extra_info(cls):
        g=input("game:")
        return (g,)
class A_Theng(HaiPhong): #A thanh
    def __init__(self, Tinh_Cach, Do_tuoi,ia):
        super().__init__(Tinh_Cach, Do_tuoi)
        self.ia=ia
    @classmethod
    def extra_info(cls):
        i=input("ia:")
        return (i,)
    
   
   


def main():
    Char=A_Theng("femboy","25","Cuc to")
    print(Char.Do_tuoi)
    print (A_Theng.get())
        
        
    
    
main()



    
