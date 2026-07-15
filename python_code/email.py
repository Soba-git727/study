import re
email=input("what's your email: ")
if re.search(r"^\w+@\w+\.(edu|com|net)$",email,re.IGNORECASE):
    print("valid")
else:
    print("invalid")