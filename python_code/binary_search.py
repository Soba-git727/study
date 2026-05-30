
def binary_search(low,high,condition):
    while low<=high:
        mid=(low+high)//2
        result=condition(mid)
        if result == "found":
            return mid      
        elif result=="right":
            low=mid+1
        elif result=="left":
            high=mid-1
    return -1
def first_position(num_list,query):
    def condition(mid):
        if num_list[mid]==query:
            if num_list[mid]>0 and num_list[mid-1]==query:
                return "left"
            else:
                return "found"
        elif num_list[mid]>query:
            return "left"
        else:
            return "right"
    return binary_search(0,len(num_list-1),condition)
def last_position(num_list,query):
    def condition(mid):
        if num_list[mid]==query:
            if num_list[mid]<len(num_list-1) and num_list[mid+1]==query:
                return "right"
            else:
                return "found"
        elif num_list[mid]>query:
            return "left"
        else:
            return "right"
    return binary_search(0,len(num_list-1),condition)
def first_and_last_position(num_list,query):
    return first_position(num_list,query),last_position(num_list,query)
                
    
