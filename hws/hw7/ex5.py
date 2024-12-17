char = input("enter char: ")

if char.lower() in 'a e i o u ' and len(char) == 1:
    result = "Гласная"
else:
    result = "Не гласная"

print(result)
