char = input("Введите букву: ")

if char.lower() in 'a e i o u а е ё и о у ы э ю я' and len(char) == 1:
    result = "Гласная"
else:
    result = "Не гласная"

print(result)
