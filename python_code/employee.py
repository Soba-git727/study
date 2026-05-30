class maxfinder:
  def __init__(self,numbers):
    self.numbers=numbers
    
  def find(self):
    n=max(self.numbers)
    if n not in self.numbers:
      print("empty")
    print (f"The largest number is {n}" )
    
def main ():
 num=maxfinder([2,3,4,5,6])
 num.find()
main()