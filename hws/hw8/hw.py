"""
Exercise-1: is_prime
Write a function "is_prime(n: int) -> bool" that takes an integer 'n' 
and checks whether it is prime. Function should return a boolean value.

Example:
is_prime(7) -> True
is_prime(10) -> False
"""

n = int(input("введи чиcло "))

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True



print(f"{n} — true." * is_prime(n) or f"{n} — false.")
 
pass


"""
Exercise-2: nth_fibonacci
Write a function "nth_fibonacci(n: int) -> int" that 
takes an integer 'n' and returns the nth number in the Fibonacci sequence.

Example:
nth_fibonacci(6) -> 5
nth_fibonacci(9) -> 21
"""

def nth_fibonacci(n: int) -> int:
 
 n = int(input("введи цифру "))

def nth_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    a = 0 
    b = 1
    for _ in range(2, n + 1):
        a, b = b, a + b  
    
    return b

print(nth_fibonacci(n))

pass

"""
Exercise-3: factorial
Write a function "factorial(n: int) -> int" that takes an integer 'n' and returns the factorial of 'n'.

Example:
factorial(5) -> 120
factorial(6) -> 720
"""

n = int(input("введи цифру "))

def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial(n))
    
pass

"""
Exercise-4: count_vowels
Write a function "count_vowels(s: str) -> int" that 
takes a string 's' and returns the number of vowels in the string.

Example:
count_vowels("hello") -> 2
count_vowels("world") -> 1
"""

s = input("введи слова ")

def count_vowels(s: str) -> int:
    vowels = "aeiouyAEIOUY"  
    count = 0
    
    for char in s:
        if char in vowels:  
            count += 1
    
    return count

print(f"{s}",f"{count_vowels(s)}")

pass

"""
Exercise-5: sum_of_digits
Write a function "sum_of_digits(n: int) -> int" that 
takes an integer 'n' and returns the sum of its digits.

Example:
sum_of_digits(12345) -> 15
sum_of_digits(98765) -> 35
"""
n = int(input("введи любое чисило "))

def sum_of_digits(n: int) -> int:
    n = abs(n)
    
    total = 0
    while n > 0:
        total = total + n % 10  
        n //= 10  
    
    return total

print(sum_of_digits(n))

  
pass


"""
Exercise-6: reverse_string
Write a function "reverse_string(s: str) -> str" that takes a string 's' and returns the string reversed.

Example:
reverse_string("hello") -> "olleh"
reverse_string("world") -> "dlrow"
"""

s = input("введи любое слово ")

def reverse_string(s: str) -> str:
    return s[::-1]

print(reverse_string(s))

pass


"""
Exercise-7: sum_of_squares
Write a function "sum_of_squares(n: int) -> int" that takes an integer 'n' and 
returns the sum of squares of all integers from 1 to 'n'.

Example:
sum_of_squares(4) -> 30
sum_of_squares(5) -> 55
"""

n = int(input("введи цифру "))

def sum_of_squares(n: int) -> int:
    total = 0 
    for i in range(1, n+1):
        if i > 0:
            total = total + i**2
    return total

print(sum_of_squares(n))

pass


"""
Exercise-8: collatz_sequence_length
Write a function "collatz_sequence_length(n: int) -> int" that takes an 
integer 'n' and returns the length of the Collatz sequence starting with 'n'.

Example:
collatz_sequence_length(6) -> 9
collatz_sequence_length(27) -> 112
"""
n = int(input("введи цифру "))

def collatz_sequence_length(n: int) -> int:
    lenght = 1
    while n !=1:
        if n % 2 == 0:
            n = n / 2
        else: 
            n = 3 * n +1 
        lenght += 1
    return  lenght 

print(collatz_sequence_length(n)) 

pass


"""
Exercise-9: is_leap_year
Write a function "is_leap_year(year: int) -> bool" that takes an 
integer 'year' and returns True if 'year' is a leap year, and False otherwise.

Example:
is_leap_year(2000) -> True
is_leap_year(1900) -> False
"""
year = int(input("введи цифру "))

def is_leap_year(year: int) -> bool:
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else: 
        return False
    
print(is_leap_year(year))

pass


"""
Exercise-10: count_words
Write a function "count_words(s: str) -> int" that takes a string 's' and 
returns the number of words in the string. Assume words are separated by spaces.

Example:
count_words("Hello world") -> 2
count_words("This is a test") -> 4
"""

word = input("введи слово: ")

def count_words(s: str) -> int:
    words = s.split()  
    return len(words)  

print(count_words(word))  

pass 


"""
Exercise-11: is_palindrome
Write a function "is_palindrome(s: str) -> bool" that takes a string 's' and 
checks if the string is a palindrome. The function should return True if the 
string is a palindrome, and False otherwise.

Example:
is_palindrome("racecar") -> True
is_palindrome("hello") -> False
"""

word = input("введи слово: ")

def is_palindrome(s: str) -> bool:
    s = s.replace(" ", "").lower()
    if s == s[::-1]:
        return True 
    else:
        return False  
    
print(is_palindrome(word))  

pass 
"""
Exercise-12: sum_of_multiples
Write a function "sum_of_multiples(n: int, x: int, y: int) -> int" that 
takes three integers 'n', 'x', and 'y', and returns the sum of all the 
numbers from 1 to 'n' (inclusive) that are multiples of 'x' or 'y'.

Example:
sum_of_multiples(10, 3, 5) -> 33
sum_of_multiples(20, 7, 11) -> 168
"""
n = int(input("введи число "))
x = int(input("введи число "))
y = int(input("введи число "))

def sum_of_multiples(n: int, x: int, y: int) -> int:
    total = 0 
    for i in range(1, n+1) :
        if i % x ==0 or i % y == 0: 
            total += i
    return total

print (sum_of_multiples(n, x, y)) 

pass


"""
Exercise-13: gcd
Write a function "gcd(a: int, b: int) -> int" that takes two integers 'a' and 'b', 
and returns their greatest common divisor (GCD).

Example:
gcd(56, 98) -> 14
gcd(27, 15) -> 3
"""
a = int(input("введи число "))
b = int(input("введи число "))

def gcd(a: int, b: int) -> int:
    if b == 0: 
        return a
    else:
        return gcd(b,a%b)

print(gcd(a, b))

pass

"""
Exercise-14: lcm
Write a function "lcm(a: int, b: int) -> int" that takes two integers 'a' and 'b', 
and returns their least common multiple (LCM).

Example:
lcm(5, 7) -> 35
lcm(6, 8) -> 24
"""

def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)

a = int(input("Введите число a: "))
b = int(input("Введите число b: "))

print("НОК чисел", a, "и", b, "равен:", lcm(a, b))

pass


"""
Exercise-15: count_characters
Write a function "count_characters(s: str, c: str) -> int" that 
takes a string 's' and a character 'c', and returns the number of occurrences of 'c' in 's'.

Example:
count_characters("hello world", "l") -> 3
count_characters("apple", "p") -> 2


"""
def count_characters(s: str, c: str) -> int:

    return s.count(c)

s = input("Введите строку: ")
c = input("Введите символ: ")

print(count_characters(s, c))

pass


"""
Exercise-16: digit_count
Write a function "digit_count(n: int) -> int" that takes an 
integer 'n' and returns the number of digits in 'n'.

Example:
digit_count(123) -> 3
digit_count(4567) -> 4
"""

n = int(input("input n "))
def digit_count(n: int) -> int:
    return len(str(abs(n)))

print(digit_count(n))
   
    
pass


"""
Exercise-17: is_power_of_two
Write a function "is_power_of_two(n: int) -> bool" that takes an integer 'n' 
and returns True if 'n' is a power of 2, and False otherwise.

Example:
is_power_of_two(8) -> True
is_power_of_two(10) -> False
"""

import math

n = int(input("input n "))
def is_power_of_two(n: int) -> bool:
    if n <= 0:
        return False
    else:
        log_value = math.log(n, 2)
        return log_value.is_integer()

print(is_power_of_two(n))

pass


"""
Exercise-18: sum_of_cubes
Write a function "sum_of_cubes(n: int) -> int" that takes an integer 'n' 
and returns the sum of the cubes of all numbers from 1 to 'n'.

Example:
sum_of_cubes(3) -> 36
sum_of_cubes(4) -> 100
"""

n = int(input("input n "))

def sum_of_cubes(n: int) -> int: 
    total = 0 
    
    for i in range (1, n+1):
        total += i**3
    return total 

print(sum_of_cubes(n))

pass


"""
Exercise-19: is_perfect_square
Write a function "is_perfect_square(n: int) -> bool" that takes an 
integer 'n' and returns True if 'n' is a perfect square, and False otherwise.

Example:
is_perfect_square(9) -> True
is_perfect_square(10) -> False
"""

import math 

n = int(input("input n "))

def is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    root = math.sqrt(n)
    return root.is_integer()

print(is_perfect_square(n))
    
pass


"""
Exercise-20: is_armstrong_number
Write a function "is_armstrong_number(n: int) -> bool" that takes an 
integer 'n' and returns True if 'n' is an Armstrong number, and False otherwise.

Example:
is_armstrong_number(153) -> True
is_armstrong_number(370) -> True
"""
n = int(input("input n "))

def is_armstrong_number(n: int) -> bool:
    digits = str(n)
    num_digits = len(digits)
    
    sum_of_powers = sum(int(digit) ** num_digits for digit in digits)
    
    return sum_of_powers == n

print(is_armstrong_number(n))

pass