class square:
    def __init__(self,width=0,length=0):
        self.width=width
        self.length=length
    
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self,value):
            if isinstance(value,int):
                self._width=value
        
    
    @property
    def length(self):
        return self._length
    @length.setter
    def length(self,value):
            if isinstance(value,int):
                self._length=value
        
    def get_width(self):
        n=int(input("square's width:"))
        self.width=n
        
    
    def get_length(self):
        n=int(input("square's length:"))
        self.length=n
        
        
def main():
    box=square()
    box.get_length()
    box.get_width()
    print (f"square's length:{box._length}")
    print (f"square's width:{box._width}")

if __name__=="__main__":
    main()
    

        
        
            
        

