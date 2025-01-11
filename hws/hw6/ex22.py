string1 = input("enter 1 word: ")
string2 = input("enter 2word: ")

if sorted(string1.lower()) == sorted(string2.lower()):
    print("true")
else:
    print("false")
