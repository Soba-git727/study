import re
email=input ("what's your name:").strip()

username,domain=email.split("@")

if re.search(r"^.+@.+\.edu$",email):
    print("valid")
else:
    print("invalid")
