# Python Practice Programs

A collection of beginner practice programs converted from Java to Python. Each entry shows the Python code, the input logic, and sample output. Save a program as a `.py` file and run it with `python file.py`.

Programs that read input use `input()`; enter values at the prompt. Programs that operate on a fixed sample use a literal list so the logic is easy to read.

## Numbers

### Print 1 to N

```python
n = int(input("enter value of n: "))
for i in range(1, n + 1):
    print(i)
```

**Input logic:** Read `n`, then loop from `1` through `n` and print each value.

**Output:**
```text
enter value of n: 10
1
2
3
4
5
6
7
8
9
10
```

### Print N to 1

```python
n = int(input("enter value of n: "))
for i in range(n, 0, -1):
    print(i, end=" ")
print()
```

**Input logic:** Read `n`, then loop from `n` down to `1` with a step of `-1`.

**Output:**
```text
enter value of n: 10
10 9 8 7 6 5 4 3 2 1
```

### Sum of 1 to N

```python
n = int(input("enter value of n: "))
total = 0
for i in range(1, n + 1):
    total += i
print(total)
```

**Input logic:** Read `n` and add every number from `1` to `n` to an accumulator.

**Output:**
```text
enter value of n: 10
55
```

### Even or Odd

```python
n = int(input("enter the num: "))
if n % 2 == 0:
    print(f"{n} is even")
else:
    print(f"{n} is odd")
```

**Input logic:** Read a number and check the remainder after dividing by `2`.

**Output:**
```text
enter the num: 20
20 is even
```

### Prime Numbers from 1 to N

```python
n = int(input("enter number: "))
print(f"Prime numbers between 1 and {n}")
for i in range(2, n + 1):
    is_prime = True
    for j in range(2, int(i ** 0.5) + 1):
        if i % j == 0:
            is_prime = False
            break
    if is_prime:
        print(i, end=" ")
print()
```

**Input logic:** For each number from `2` to `n`, test divisibility by every integer up to its square root. `1` is not prime.

**Output:**
```text
enter number: 25
Prime numbers between 1 and 25
2 3 5 7 11 13 17 19 23
```

### Check Whether a Number Is Prime

```python
n = int(input("enter number: "))
if n < 2:
    print("not a prime")
else:
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            print("not a prime")
            break
    else:
        print("prime")
```

**Input logic:** Read `n`. Numbers below `2` are not prime; otherwise test divisors up to the square root. The `for ... else` runs only when no divisor was found.

**Output:**
```text
enter number: 17
prime
```

### Sum of Prime Numbers

```python
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


limit = int(input("Enter the range to print sum of prime Nos: "))
print(sum(i for i in range(2, limit + 1) if is_prime(i)))
```

**Input logic:** Read the upper limit, test each number from `2` to the limit, and add the primes.

**Output:**
```text
Enter the range to print sum of prime Nos: 10
17
```

### Multiplication Table

```python
n = int(input("enter value of n: "))
for i in range(1, 11):
    print(f"{n}*{i}={n * i}")
```

**Input logic:** Read `n` and multiply it by each number from `1` to `10`.

**Output:**
```text
enter value of n: 2
2*1=2
2*2=4
2*3=6
2*4=8
2*5=10
2*6=12
2*7=14
2*8=16
2*9=18
2*10=20
```

### Multiplication Tables

```python
n = int(input("enter value of n: "))
for i in range(1, n + 1):
    row = [f"{j}*{i}={j * i}" for j in range(1, 11)]
    print(" ".join(row))
```

**Input logic:** For each multiplier `i` from `1` to `n`, build one row of ten products.

**Output:**
```text
enter value of n: 5
1*1=1 2*1=2 3*1=3 4*1=4 5*1=5 6*1=6 7*1=7 8*1=8 9*1=9 10*1=10
1*2=2 2*2=4 3*2=6 4*2=8 5*2=10 6*2=12 7*2=14 8*2=16 9*2=18 10*2=20
...
```

### Perfect Number

A perfect number equals the sum of its proper divisors, for example `6 = 1 + 2 + 3`.

```python
num = int(input("enter a number: "))
if num < 2:
    print(f"{num} is not a Perfect number")
else:
    total = 1
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            total += i
    if total == num:
        print(f"{num} is a Perfect number")
    else:
        print(f"{num} is not a Perfect number")
```

**Input logic:** Read a number, start the divisor sum at `1`, add every divisor from `2` to `num // 2`, then compare the sum with the number.

**Output:**
```text
enter a number: 6
6 is a Perfect number
```

### Range of Perfect Numbers

```python
n = int(input("enter a number: "))
for num in range(2, n + 1):
    total = 1
    for i in range(2, num // 2 + 1):
        if num % i == 0:
            total += i
    if total == num:
        print(f"{num} is a Perfect number")
```

**Input logic:** Repeat the perfect-number test for every value from `2` to `n`.

**Output:**
```text
enter a number: 100
6 is a Perfect number
28 is a Perfect number
```

### Palindrome Number

```python
n = int(input("enter a number: "))
original = n
reverse = 0
while n != 0:
    reverse = reverse * 10 + (n % 10)
    n //= 10
print(f"{original} is a palindrome number" if reverse == original else f"{original} is not a palindrome number")
```

**Input logic:** Read a number, build its reverse digit by digit, and compare with the original.

**Output:**
```text
enter a number: 121
121 is a palindrome number
```

### Factorial

```python
n = int(input("enter the number: "))
fact = 1
for i in range(1, n + 1):
    fact *= i
print(fact)
```

**Input logic:** Read `n` and multiply every integer from `1` to `n`.

**Output:**
```text
enter the number: 5
120
```

### Factorial of a Range

```python
def fact(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


limit = int(input("enter the factorial range number: "))
for i in range(1, limit + 1):
    print(f"{i}!---->{fact(i)}")
```

**Input logic:** Read a limit and print the factorial of every number from `1` to the limit.

**Output:**
```text
enter the factorial range number: 7
1!---->1
2!---->2
3!---->6
4!---->24
5!---->120
6!---->720
7!---->5040
```

### Strong Number

A strong number equals the sum of the factorials of its digits, for example `145 = 1! + 4! + 5!`.

```python
def fact(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


n = int(input("enter a number: "))
original = n
total = 0
while n != 0:
    total += fact(n % 10)
    n //= 10
print(f"{original} is a strong number" if total == original else f"{original} is not a strong number")
```

**Input logic:** Read a number, take each digit with `% 10`, add its factorial, and remove the digit with `// 10`.

**Output:**
```text
enter a number: 145
145 is a strong number
```

### Range of Strong Numbers

```python
def fact(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


limit = int(input("enter a Range: "))
for num in range(1, limit + 1):
    original = num
    total = 0
    while num != 0:
        total += fact(num % 10)
        num //= 10
    if total == original:
        print(f"{original} is a strong number")
```

**Input logic:** Test every number from `1` to the limit with the strong-number rule.

**Output:**
```text
enter a Range: 145
1 is a strong number
2 is a strong number
145 is a strong number
```

### Fibonacci Number

```python
def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


n = int(input("Enter the number: "))
print(fib(n))
```

**Input logic:** Read the position `n` and compute the Fibonacci value iteratively.

**Output:**
```text
Enter the number: 10
55
```

### Range of Fibonacci Numbers

```python
limit = int(input("enter the range: "))
a, b = 0, 1
print(a, b, end=" ")
while True:
    c = a + b
    if c > limit:
        break
    print(c, end=" ")
    a, b = b, c
print()
```

**Input logic:** Read an upper limit and print Fibonacci values that do not exceed it.

**Output:**
```text
enter the range: 50
0 1 1 2 3 5 8 13 21 34
```

### Reverse the Number

```python
num = int(input("enter the number: "))
reverse = 0
while num != 0:
    reverse = reverse * 10 + (num % 10)
    num //= 10
print(reverse)
```

**Input logic:** Build the reverse by taking the last digit and shifting the new value left by one decimal place.

**Output:**
```text
enter the number: 105
501
```

### GCD of Two Numbers

```python
def gcd(m, n):
    if m < n:
        return gcd(n, m)
    if n == 0:
        return m
    return gcd(n, m % n)


p = int(input("Enter the first number: "))
q = int(input("Enter the second number: "))
print(gcd(p, q))
```

**Input logic:** Use Euclid's algorithm: replace `(m, n)` with `(n, m % n)` until the remainder is zero.

**Output:**
```text
Enter the first number: 90
Enter the second number: 120
30
```

### Prime Palindrome

```python
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


n = int(input("enter a number: "))
if int(str(n)[::-1]) != n:
    print(f"{n} is not a prime palindrome number")
elif is_prime(n):
    print(f"{n} is a prime palindrome number")
else:
    print(f"{n} is not a prime palindrome number")
```

**Input logic:** Read a number, check whether it equals its reverse, and if so test whether it is prime.

**Output:**
```text
enter a number: 313
313 is a prime palindrome number
```

### Armstrong Number

An Armstrong number equals the sum of its digits raised to the power of the digit count, for example `153 = 1**3 + 5**3 + 3**3`.

```python
n = int(input("enter the number: "))
digits = len(str(n))
total = sum(int(d) ** digits for d in str(n))
print("Given num is Armstrong" if total == n else "Given num is not Armstrong")
```

**Input logic:** Count the digits, raise each digit to that count, and compare the sum with the original number.

**Output:**
```text
enter the number: 153
Given num is Armstrong
```

### Range of Armstrong Numbers

```python
limit = int(input("enter the number: "))
for i in range(limit + 1):
    digits = len(str(i))
    total = sum(int(d) ** digits for d in str(i))
    if total == i:
        print(f"{i} is Armstrong")
```

**Input logic:** Apply the Armstrong test to every number from `0` to the limit.

**Output:**
```text
enter the number: 300
0 is Armstrong
1 is Armstrong
2 is Armstrong
3 is Armstrong
4 is Armstrong
5 is Armstrong
6 is Armstrong
7 is Armstrong
8 is Armstrong
9 is Armstrong
153 is Armstrong
```

### Swap Two Numbers Without a Third Variable

```python
i = 10
j = 20
i = i + j
j = i - j
i = i - j
print(f"i={i}")
print(f"j={j}")
```

**Input logic:** Add the two values, then subtract to recover each original value.

**Output:**
```text
i=20
j=10
```

### Swap Two Numbers With a Third Variable

```python
i = 10
j = 20
k = i
i = j
j = k
print(f"i={i}")
print(f"j={j}")
```

**Input logic:** Copy one value into a temporary variable before overwriting it.

**Output:**
```text
i=20
j=10
```

### Binary to Decimal

```python
def binary_to_decimal(bits):
    decimal = 0
    for ch in bits:
        decimal = decimal * 2 + int(ch)
    return decimal


bits = input("enter the binary number: ")
print(f"decimal Equivalent: {binary_to_decimal(bits)}")
```

**Input logic:** Read the binary digits as text and accumulate `decimal * 2 + digit` for each digit.

**Output:**
```text
enter the binary number: 111100001111
decimal Equivalent: 3855
```

### Decimal to Binary

```python
def decimal_to_binary(n):
    if n == 0:
        return "0"
    bits = ""
    while n > 0:
        bits = str(n % 2) + bits
        n //= 2
    return bits


n = int(input("enter the decimal number: "))
print(f"Binary Equivalent: {decimal_to_binary(n)}")
```

**Input logic:** Repeatedly take the remainder after dividing by `2`, prepend it, and divide the number.

**Output:**
```text
enter the decimal number: 3855
Binary Equivalent: 111100001111
```

### Octal to Decimal

```python
def octal_to_decimal(digits):
    decimal = 0
    for ch in digits:
        decimal = decimal * 8 + int(ch)
    return decimal


digits = input("enter the octal number: ")
print(f"decimal Equivalent: {octal_to_decimal(digits)}")
```

**Input logic:** Accumulate `decimal * 8 + digit` for each octal digit.

**Output:**
```text
enter the octal number: 763
decimal Equivalent: 499
```

### Decimal to Octal

```python
def decimal_to_octal(n):
    if n == 0:
        return "0"
    digits = ""
    while n > 0:
        digits = str(n % 8) + digits
        n //= 8
    return digits


n = int(input("enter the decimal number: "))
print(f"Octal Equivalent: {decimal_to_octal(n)}")
```

**Input logic:** Repeatedly take the remainder after dividing by `8` and prepend it.

**Output:**
```text
enter the decimal number: 56
Octal Equivalent: 70
```

### Decimal to Hexadecimal

```python
def decimal_to_hex(n):
    digits = "0123456789ABCDEF"
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = digits[n % 16] + result
        n //= 16
    return result


n = int(input("enter the decimal number: "))
print(f"Hexadecimal Equivalent: {decimal_to_hex(n)}")
```

**Input logic:** Use the digit table `0123456789ABCDEF` and prepend the remainder after dividing by `16`.

**Output:**
```text
enter the decimal number: 469
Hexadecimal Equivalent: 1D5
```

### Decimal to Any Base

```python
def convert(num, base):
    digits = "0123456789ABCDEF"
    if num == 0:
        return "0"
    result = ""
    while num > 0:
        result = digits[num % base] + result
        num //= base
    return result


n = int(input("enter the number: "))
base = int(input("enter the base: "))
print(f"{base} base equivalent: {convert(n, base)}")
```

**Input logic:** Read a number and a base, then reuse the remainder method with the digit table.

**Output:**
```text
enter the number: 469
enter the base: 16
16 base equivalent: 1D5
```

### Hexadecimal to Decimal

```python
def hex_to_decimal(text):
    decimal = 0
    for ch in text.upper():
        value = int(ch) if "0" <= ch <= "9" else ord(ch) - ord("A") + 10
        decimal = decimal * 16 + value
    return decimal


text = input("enter the Hexa dec number: ")
print(f"Decimal Equivalent: {hex_to_decimal(text)}")
```

**Input logic:** Convert each hex character to its value (`A`–`F` become `10`–`15`) and accumulate in base `16`.

**Output:**
```text
enter the Hexa dec number: 1D5
Decimal Equivalent: 469
```

## Star Patterns

### Equilateral Triangle

```python
n = int(input("enter the number: "))
for i in range(n):
    print(" " * (n - i - 1) + "* " * (i + 1))
```

**Input logic:** For each row, print leading spaces followed by one more star-and-space pair.

**Output:**
```text
enter the number: 7
      *
     * *
    * * *
   * * * *
  * * * * *
 * * * * * *
* * * * * * *
```

### Inverted Triangle

```python
n = int(input("enter the number: "))
for i in range(n):
    print(" " * i + "*" * (2 * (n - i) - 1))
```

**Input logic:** Each row adds one leading space and removes two stars.

**Output:**
```text
enter the number: 4
*******
 *****
  ***
   *
```

### Filled Box

```python
n = int(input("enter value of n: "))
for _ in range(n):
    print("*" * n)
```

**Input logic:** Print `n` rows, each containing `n` stars.

**Output:**
```text
enter value of n: 7
*******
*******
*******
*******
*******
*******
*******
```

### Hollow Box

```python
n = int(input("enter value of n: "))
for i in range(n):
    row = ""
    for j in range(n):
        if i in (0, n - 1) or j in (0, n - 1):
            row += "*"
        else:
            row += " "
    print(row)
```

**Input logic:** Print a star on the border rows or border columns; print a space elsewhere.

**Output:**
```text
enter value of n: 7
*******
*     *
*     *
*     *
*     *
*     *
*******
```

### Box with a Cross Inside

```python
n = int(input("enter value of n: "))
for i in range(n):
    row = ""
    for j in range(n):
        if i in (0, n - 1) or j in (0, n - 1) or i == j or i + j == n - 1:
            row += "*"
        else:
            row += " "
    print(row)
```

**Input logic:** Draw the border plus both diagonals (`i == j` and `i + j == n - 1`).

**Output:**
```text
enter value of n: 7
*******
**   **
* * * *
*  *  *
* * * *
**   **
*******
```

### Cross Mark

```python
n = int(input("enter value of n (odd): "))
for i in range(n):
    row = ""
    for j in range(n):
        row += "*" if i == j or i + j == n - 1 else " "
    print(row)
```

**Input logic:** Print a star only where the row and column are equal or mirrored.

**Output:**
```text
enter value of n (odd): 7
*     *
 *   *
  * *
   *
  * *
 *   *
*     *
```

### Right Angle Triangle

```python
n = int(input("enter value of n: "))
for i in range(1, n + 1):
    print("*" * i)
```

**Input logic:** Row `i` contains `i` stars.

**Output:**
```text
enter value of n: 7
*
**
***
****
*****
******
*******
```

### Reverse Triangle

```python
n = int(input("enter value of n: "))
for i in range(n):
    print("*" * (n - i))
```

**Input logic:** Start with `n` stars and remove one per row.

**Output:**
```text
enter value of n: 7
*******
******
*****
****
***
**
*
```

### Mirror Right Angle Triangle

```python
n = int(input("enter value of n: "))
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * i)
```

**Input logic:** Pad each row on the left so the stars align to the right.

**Output:**
```text
enter value of n: 7
      *
     **
    ***
   ****
  *****
 ******
*******
```

### Downward Mirror Right Angle Triangle

```python
n = int(input("enter value of n: "))
for i in range(n, 0, -1):
    print(" " * (n - i) + "*" * i)
```

**Input logic:** Start with the widest row and shift each row right while removing a star.

**Output:**
```text
enter value of n: 7
*******
 ******
  *****
   ****
    ***
     **
      *
```

### Diamond

```python
n = int(input("enter odd number: "))
mid = n // 2
for i in range(n):
    stars = 2 * i + 1 if i <= mid else 2 * (n - 1 - i) + 1
    spaces = abs(mid - i)
    print(" " * spaces + "*" * stars)
```

**Input logic:** Expand the star count until the middle row, then shrink it; center each row with spaces.

**Output:**
```text
enter odd number: 7
   *
  ***
 *****
*******
 *****
  ***
   *
```

### Hollow Diamond

```python
n = int(input("enter odd number: "))
mid = n // 2
for i in range(n):
    stars = 2 * i + 1 if i <= mid else 2 * (n - 1 - i) + 1
    spaces = abs(mid - i)
    if stars == 1:
        print(" " * spaces + "*")
    else:
        print(" " * spaces + "*" + " " * (stars - 2) + "*")
```

**Input logic:** Build the diamond outline by printing stars only at the edges of each row.

**Output:**
```text
enter odd number: 7
   *
  * *
 *   *
*     *
 *   *
  * *
   *
```

### Numbers in Diamond Shape

```python
n = int(input("enter odd number: "))
mid = n // 2
for i in range(n):
    stars = 2 * i + 1 if i <= mid else 2 * (n - 1 - i) + 1
    spaces = abs(mid - i)
    k = 1
    row = ""
    for j in range(stars):
        row += str(k)
        if j < stars // 2:
            k += 1
        else:
            k -= 1
    print(" " * spaces + row)
```

**Input logic:** Build an ascending-then-descending number sequence sized to each diamond row.

**Output:**
```text
enter odd number: 7
   1
  121
 12321
1234321
 12321
  121
   1
```

### Characters in Diamond Shape

```python
n = int(input("enter odd number: "))
mid = n // 2
for i in range(n):
    stars = 2 * i + 1 if i <= mid else 2 * (n - 1 - i) + 1
    spaces = abs(mid - i)
    k = 0
    row = ""
    for j in range(stars):
        row += chr(ord("A") + k)
        if j < stars // 2:
            k += 1
        else:
            k -= 1
    print(" " * spaces + row)
```

**Input logic:** Same shape as the number diamond, using letters starting at `A`.

**Output:**
```text
enter odd number: 7
   A
  ABA
 ABCBA
ABCDCBA
 ABCBA
  ABA
   A
```

### M Pattern

```python
spaces = 8
for i in range(1, 6):
    print("*" * i + " " * spaces + "*" * i)
    spaces -= 2
```

**Input logic:** Print two star blocks per row and reduce the gap by two each time.

**Output:**
```text
*        *
**      **
***    ***
****  ****
**********
```

### Numbers in Triangle Format

```python
n = int(input("enter the rows: "))
k = 0
for i in range(1, n + 1):
    row = []
    for _ in range(i):
        k += 1
        row.append(str(k))
    print(" ".join(row))
```

**Input logic:** Keep one running counter and print `i` consecutive values on row `i`.

**Output:**
```text
enter the rows: 5
1
2 3
4 5 6
7 8 9 10
11 12 13 14 15
```

## Strings

### Anagram

An anagram is a word or phrase formed by rearranging the letters of another, such as `silent` and `listen`.

```python
def normalize(text):
    return sorted(text.replace(" ", "").lower())


first = input("Enter the first string: ")
second = input("Enter the second string: ")
print("string is anagram" if normalize(first) == normalize(second) else "not an anagram")
```

**Input logic:** Remove spaces, convert to lowercase, sort the characters, and compare the results.

**Output:**
```text
Enter the first string: Mother in law
Enter the second string: Hitler woman
string is anagram
```

### Pangram

A pangram is a sentence containing every letter of the alphabet.

```python
def is_pangram(text):
    letters = set(text.lower())
    return all(chr(code) in letters for code in range(ord("a"), ord("z") + 1))


text = input("enter the string: ")
print(f"{text}\n{'is a pangram' if is_pangram(text) else 'is not pangram'}")
```

**Input logic:** Lowercase the text, collect its characters in a set, and check that every letter `a`–`z` is present.

**Output:**
```text
enter the string: the quick brown fox jumps over a lazy dog
the quick brown fox jumps over a lazy dog
is a pangram
```

### Palindrome String

```python
text = input("enter the string: ")
cleaned = text.replace(" ", "").lower()
print(f"{text} string is palindrome" if cleaned == cleaned[::-1] else f"{text} string is not palindrome")
```

**Input logic:** Remove spaces, ignore case, and compare the text with its reverse.

**Output:**
```text
enter the string: Malayalam
Malayalam string is palindrome
```

### Reverse a String

```python
text = input("enter the string: ")
print(f"Reversed string is: {text[::-1]}")
```

**Input logic:** Read a string and slice it with a step of `-1`.

**Output:**
```text
enter the string: rama and laxmana
Reversed string is: anamxal dna amar
```

### Count Characters in a String

```python
text = input("Enter a string: ")
count = sum(1 for ch in text if ch.isalnum())
print(f"No of Characters={count}")
```

**Input logic:** Count letters and digits, ignoring spaces and punctuation.

**Output:**
```text
Enter a string: adkvdh dodksk
No of Characters=12
```

### Sum of Numbers in an Alphanumeric String

```python
text = input("enter the alpha numeric string: ")
print(sum(int(ch) for ch in text if ch.isdigit()))
```

**Input logic:** Add the value of every digit character and ignore everything else.

**Output:**
```text
enter the alpha numeric string: 139y1d5801
28
```

### Characters in Each Word

```python
text = input("enter the string: ")
for word in text.split():
    print(f"{word} {len(word)}", end=" ")
print()
```

**Input logic:** Split the sentence into words and print each word with its length.

**Output:**
```text
enter the string: rama and laxmana
rama 4 and 3 laxmana 7
```

### Occurrences of Each Character

```python
text = input("Enter the String: ")
counts = {}
for ch in text:
    counts[ch] = counts.get(ch, 0) + 1
for ch, count in counts.items():
    print(f"{ch} occurred {count} times")
```

**Input logic:** Build a dictionary that counts each character while preserving first-seen order.

**Output:**
```text
Enter the String: Malayalam
M occurred 1 times
a occurred 4 times
l occurred 2 times
y occurred 1 times
m occurred 1 times
```

### Count Character Types

```python
text = input("enter the string: ")
upper = lower = digits = spaces = special = 0
for ch in text:
    if ch.isupper():
        upper += 1
    elif ch.islower():
        lower += 1
    elif ch.isdigit():
        digits += 1
    elif ch == " ":
        spaces += 1
    else:
        special += 1
print(f"no of upper case letter {upper}")
print(f"no of lower case letter {lower}")
print(f"no of decimal number {digits}")
print(f"no of spaces {spaces}")
print(f"no of special characters {special}")
```

**Input logic:** Classify each character and increment the matching counter.

**Output:**
```text
enter the string: PramoD123$@gmail.com
no of upper case letter 2
no of lower case letter 12
no of decimal number 3
no of spaces 0
no of special characters 3
```

### Number into Words

```python
ones = ["", "one", "two", "three", "four", "five", "six", "seven",
        "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "", "twenty", "thirty", "forty", "fifty",
        "sixty", "seventy", "eighty", "ninety"]


def below_hundred(n):
    if n < 20:
        return ones[n]
    return tens[n // 10] + (" " + ones[n % 10] if n % 10 else "")


def number_to_words(num):
    if num == 0:
        return "zero"
    parts = []
    crore, num = divmod(num, 10000000)
    lakh, num = divmod(num, 100000)
    thousand, num = divmod(num, 1000)
    hundred, num = divmod(num, 100)
    if crore:
        parts.append(below_hundred(crore) + " crore")
    if lakh:
        parts.append(below_hundred(lakh) + " lakh")
    if thousand:
        parts.append(below_hundred(thousand) + " thousand")
    if hundred:
        parts.append(ones[hundred] + " hundred")
    if num:
        parts.append(("and " if parts else "") + below_hundred(num))
    return " ".join(parts)


num = int(input("enter the number: "))
print(number_to_words(num))
```

**Input logic:** Break the number into crore, lakh, thousand, hundred, and remainder parts, then convert each part.

**Output:**
```text
enter the number: 999999
nine lakh ninety nine thousand nine hundred and ninety nine
```

### Reverse the Sentence

```python
text = input("enter the sentence: ")
print("The reverse sentence is: " + " ".join(reversed(text.split())))
```

**Input logic:** Split into words, reverse the word order, and join with spaces.

**Output:**
```text
enter the sentence: rama and laxmana
The reverse sentence is: laxmana and rama
```

### Reverse the Words in a Sentence

```python
text = input("enter the sentence: ")
print("The reversed words of sentence is: " + " ".join(word[::-1] for word in text.split()))
```

**Input logic:** Reverse each word individually while keeping the word order.

**Output:**
```text
enter the sentence: rama and laxmana
The reversed words of sentence is: amar dna anamxal
```

### Initcap Words

```python
text = input("enter the string: ")
print("enter the string in it cap: " + " ".join(word.capitalize() for word in text.split()))
```

**Input logic:** Capitalize the first letter of each word and lowercase the rest.

**Output:**
```text
enter the string: pramod reddy pavan chandu
enter the string in it cap: Pramod Reddy Pavan Chandu
```

### Toggle Case

```python
text = input("enter the string: ")
print("converted String in Case: " + text.swapcase())
```

**Input logic:** Swap uppercase letters to lowercase and lowercase letters to uppercase.

**Output:**
```text
enter the string: PraMoD ReddY GoPi RedDY
converted String in Case: pRAmOd rEDDy gOpI rEDdy
```

### Substring Without Built-in Functions

```python
main = input("enter the main string: ")
sub = input("enter the sub string: ")
found = 0
for i in range(len(main)):
    k, j = i, 0
    while k < len(main) and j < len(sub) and main[k] == sub[j]:
        k += 1
        j += 1
    if j == len(sub):
        found += 1
        print(f"{found} times {sub} present between {i} to {k} indexes")
if found == 0:
    print("not found")
```

**Input logic:** At every starting position, compare characters until the substring ends or a mismatch occurs.

**Output:**
```text
enter the main string: PramodReddy
enter the sub string: Reddy
1 times Reddy present between 6 to 11 indexes
```

### String to Integer Without `int()`

```python
def string_to_int(text):
    if not text.isdigit():
        return None
    number = 0
    for ch in text:
        number = number * 10 + (ord(ch) - ord("0"))
    return number


text = input("enter the String: ")
value = string_to_int(text)
if value is None:
    print("not valid string")
else:
    print(f"{value} is in integer type")
```

**Input logic:** Validate that every character is a digit, then accumulate `number * 10 + digit` using character codes.

**Output:**
```text
enter the String: 3306
3306 is in integer type
```

## Searching and Sorting

### Linear Search

```python
def linear_search(arr, target):
    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1


arr = [3, 46, 76, 4, 89, 7, 27]
print(linear_search(arr, 4))
print(linear_search(arr, 78))
```

**Input logic:** Check each element in order and return its index, or `-1` if it is absent.

**Output:**
```text
3
-1
```

### Binary Search

Binary search requires a sorted array.

```python
def binary_search(arr, target):
    first, last = 0, len(arr) - 1
    while first <= last:
        middle = (first + last) // 2
        if arr[middle] == target:
            return middle
        if target > arr[middle]:
            first = middle + 1
        else:
            last = middle - 1
    return -1


arr = sorted([10, 49, 67, 90, 40, 86])
print(binary_search(arr, 49))
```

**Input logic:** Sort the data, then repeatedly halve the search range by comparing with the middle element.

**Output:**
```text
2
```

### Bubble Sort

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


arr = [5, 8, 1, 6, 9, 2]
bubble_sort(arr)
for value in arr:
    print(value)
```

**Input logic:** Compare adjacent pairs and swap them until the largest values bubble to the end.

**Output:**
```text
1
2
5
6
8
9
```

## Arrays

### Insert Elements into an Array

```python
length = int(input("enter the size: "))
print(f"enter the {length} elements")
arr = [int(input()) for _ in range(length)]
for i, value in enumerate(arr):
    print(f"arr[{i}] ----> {value}")
```

**Input logic:** Read the size, then read that many integers into a list.

**Output:**
```text
enter the size: 5
enter the 5 elements
2
3
5
8
64
arr[0] ----> 2
arr[1] ----> 3
arr[2] ----> 5
arr[3] ----> 8
arr[4] ----> 64
```

### Reverse the Elements of an Array

```python
length = int(input("enter the size: "))
print(f"enter the {length} elements")
arr = [int(input()) for _ in range(length)]
print("Before Reverse of an Array")
for i, value in enumerate(arr):
    print(f"arr[{i}] ----> {value}")
for i in range(len(arr) // 2):
    j = len(arr) - 1 - i
    arr[i], arr[j] = arr[j], arr[i]
print("After Reverse of an Array")
for i, value in enumerate(arr):
    print(f"arr[{i}] ----> {value}")
```

**Input logic:** Swap the first and last elements, then move inward until the middle.

**Output:**
```text
enter the size: 5
enter the 5 elements
1
5
6
8
9
Before Reverse of an Array
arr[0] ----> 1
arr[1] ----> 5
arr[2] ----> 6
arr[3] ----> 8
arr[4] ----> 9
After Reverse of an Array
arr[0] ----> 9
arr[1] ----> 8
arr[2] ----> 6
arr[3] ----> 5
arr[4] ----> 1
```

### Insert an Element at a Position

```python
length = int(input("enter the length: "))
print(f"enter the {length} elements")
arr = [int(input()) for _ in range(length)]
print(f"length of array before inserting ---> {len(arr)}")
index = int(input("enter the index: "))
element = int(input("enter the element to insert: "))
if 0 <= index <= len(arr):
    arr.insert(index, element)
    print(f"length of array after inserting ---> {len(arr)}")
    for i, value in enumerate(arr):
        print(f"{i}------->{value}")
else:
    print("invalid index")
```

**Input logic:** Validate the index, then insert the value and shift later elements right.

**Output:**
```text
enter the length: 5
enter the 5 elements
2
8
6
7
88
length of array before inserting ---> 5
enter the index: 3
enter the element to insert: 62
length of array after inserting ---> 6
0------->2
1------->8
2------->6
3------->62
4------->7
5------->88
```

### Delete an Element at a Position

```python
length = int(input("enter the length: "))
print(f"enter the {length} elements")
arr = [int(input()) for _ in range(length)]
print(f"length of array before deleting ---> {len(arr)}")
for i, value in enumerate(arr):
    print(f"{i}------->{value}")
index = int(input("enter the index to delete: "))
if 0 <= index < len(arr):
    arr.pop(index)
    print(f"length of array after deleting ---> {len(arr)}")
    for i, value in enumerate(arr):
        print(f"{i}------->{value}")
else:
    print("invalid index")
```

**Input logic:** Validate the index, remove that element, and shift later elements left.

**Output:**
```text
enter the length: 6
enter the 6 elements
5
5
9
8
6
2
length of array before deleting ---> 6
0------->5
1------->5
2------->9
3------->8
4------->6
5------->2
enter the index to delete: 5
length of array after deleting ---> 5
0------->5
1------->5
2------->9
3------->8
4------->2
```

### Search an Element in an Array

```python
def search(arr, element):
    for i, value in enumerate(arr):
        if value == element:
            return i
    return -1


arr = [22, 11, 23, 11, 15, 19]
index = search(arr, 15)
for i, value in enumerate(arr):
    print(f"{i}------->{value}")
print(f"your element found at index {index}" if index >= 0 else "not valid")
```

**Input logic:** Return the index of the first match, or `-1` when the value is absent.

**Output:**
```text
0------->22
1------->11
2------->23
3------->11
4------->15
5------->19
your element found at index 4
```

### Biggest and Smallest Element

```python
length = int(input("enter the length: "))
print(f"enter the {length} elements")
arr = [int(input()) for _ in range(length)]
biggest = arr[0]
smallest = arr[0]
for value in arr:
    if value > biggest:
        biggest = value
    if value < smallest:
        smallest = value
print(f"biggest element is ----> {biggest}")
print(f"smallest element is ----> {smallest}")
```

**Input logic:** Initialize both values from the first element, then compare each remaining element once.

**Output:**
```text
enter the length: 5
enter the 5 elements
1
8
99
66
75
biggest element is ----> 99
smallest element is ----> 1
```

### First and Second Biggest Element

```python
arr = [23, 12, 14, 56, 22, 28, 13]
first_big = second_big = float("-inf")
for value in arr:
    if value > first_big:
        second_big = first_big
        first_big = value
    elif value > second_big:
        second_big = value
print(f"first biggest element is {first_big}")
print(f"second biggest element is {second_big}")
```

**Input logic:** Track the largest and second largest values in one pass, shifting the old largest down when a new maximum appears.

**Output:**
```text
first biggest element is 56
second biggest element is 28
```

### Second Occurrence of an Element

```python
def second_occurrence(arr, element):
    count = 0
    for i, value in enumerate(arr):
        if value == element:
            count += 1
            if count == 2:
                return i
    return -1


arr = [22, 11, 23, 11, 15, 19, 11]
index = second_occurrence(arr, 11)
for i, value in enumerate(arr):
    print(f"arr[{i}]------->{value}")
print(f"second time occurred element found at the index {index}" if index >= 0 else "not valid")
```

**Input logic:** Count matches and return the index when the count reaches two.

**Output:**
```text
arr[0]------->22
arr[1]------->11
arr[2]------->23
arr[3]------->11
arr[4]------->15
arr[5]------->19
arr[6]------->11
second time occurred element found at the index 3
```

### Position of the Nth Occurrence

```python
def occurrence(arr, element, order):
    count = 0
    for i, value in enumerate(arr):
        if value == element:
            count += 1
            if count == order:
                return i
    return -1


arr = [22, 11, 23, 11, 15, 19, 11]
index = occurrence(arr, 11, 2)
for i, value in enumerate(arr):
    print(f"{i}------->{value}")
print(f"your element found at index {index}" if index >= 0 else "not valid")
```

**Input logic:** Count matches and return the index of the requested occurrence number.

**Output:**
```text
0------->22
1------->11
2------->23
3------->11
4------->15
5------->19
6------->11
your element found at index 3
```

### Count How Many Times an Element Occurs

```python
arr = [22, 11, 23, 11, 15, 19, 11]
count = arr.count(11)
for i, value in enumerate(arr):
    print(f"{i}------->{value}")
print(f"your element occurred {count}")
```

**Input logic:** Compare every element with the target and count matches.

**Output:**
```text
0------->22
1------->11
2------->23
3------->11
4------->15
5------->19
6------->11
your element occurred 3
```

### Missing Elements in a Sorted Array

```python
arr = [8, 15, 21, 24, 30, 37]
print("Missing elements in given array are:")
for i in range(len(arr) - 1):
    for value in range(arr[i] + 1, arr[i + 1]):
        print(value, end=" ")
print()
```

**Input logic:** For each adjacent pair, print every value strictly between them.

**Output:**
```text
Missing elements in given array are:
9 10 11 12 13 14 16 17 18 19 20 22 23 25 26 27 28 29 31 32 33 34 35 36
```

### Highest Contiguous Sum of Two Elements

```python
arr = [21, 12, 15, 32, 16, 17, 22]
big = arr[0] + arr[1]
index = 0
for i in range(1, len(arr) - 1):
    if arr[i] + arr[i + 1] > big:
        big = arr[i] + arr[i + 1]
        index = i
print(f"sum of two elements -----> {big}")
print(f"the first element ---> {arr[index]}")
print(f"the second element ---> {arr[index + 1]}")
```

**Input logic:** Compare each adjacent pair and remember the pair with the largest sum.

**Output:**
```text
sum of two elements -----> 48
the first element ---> 32
the second element ---> 16
```

### Common Elements Between Two Arrays

```python
arr1 = [12, 13, 23, 15, 11, 16]
arr2 = [53, 26, 23, 15, 18, 13]
print("common elements are:")
for value in arr1:
    if value in arr2:
        print(value)
```

**Input logic:** Print each value from the first array that also appears in the second.

**Output:**
```text
common elements are:
13
23
15
```

### Exchange the Halves of an Array

```python
arr = [21, 12, 15, 32, 16, 17, 22]
print("BEFORE EXCHANGE OF ARRAY")
for value in arr:
    print(value)
n = len(arr) // 2 + len(arr) % 2
for i in range(len(arr) // 2):
    arr[i], arr[n + i] = arr[n + i], arr[i]
print("AFTER EXCHANGE OF ARRAY")
for value in arr:
    print(value)
```

**Input logic:** Split at the middle (rounding up for odd lengths) and swap matching positions between the halves.

**Output:**
```text
BEFORE EXCHANGE OF ARRAY
21
12
15
32
16
17
22
AFTER EXCHANGE OF ARRAY
16
17
22
32
21
12
15
```

### Distinct Elements from Two Arrays

```python
arr1 = [12, 13, 23, 15, 11, 16]
arr2 = [53, 26, 23, 15, 18, 13]
print("Distinct elements from given two arrays")
for value in arr1:
    if value not in arr2:
        print(value)
for value in arr2:
    if value not in arr1:
        print(value)
```

**Input logic:** Print values that appear in only one of the two arrays.

**Output:**
```text
Distinct elements from given two arrays
12
11
16
53
26
18
```

### Merge Two Arrays

```python
arr1 = [12, 13, 23, 15, 11, 16]
arr2 = [53, 26, 23, 15, 18, 13]
merged = arr1 + arr2
print("MERGED ARRAY")
for value in merged:
    print(value)
```

**Input logic:** Concatenate the two lists in order.

**Output:**
```text
MERGED ARRAY
12
13
23
15
11
16
53
26
23
15
18
13
```

### Combine Two Arrays in Zigzag Order

```python
arr1 = [12, 13, 23, 15, 11, 16]
arr2 = [53, 26, 23, 15, 18, 13, 23, 45]
merged = []
i = j = 0
while i < len(arr1) or j < len(arr2):
    if i < len(arr1):
        merged.append(arr1[i])
        i += 1
    if j < len(arr2):
        merged.append(arr2[j])
        j += 1
print("ZIGZAG ARRAY IS")
for value in merged:
    print(value)
```

**Input logic:** Alternate taking one value from each array until both are exhausted.

**Output:**
```text
ZIGZAG ARRAY IS
12
53
13
26
23
23
15
15
11
18
16
13
23
45
```

### Palindrome Numbers in an Array

```python
arr = [232, 12, 78, 898, 34543, 45]
count = 0
for value in arr:
    if value == int(str(value)[::-1]):
        count += 1
print(f"number of palindrome: {count}")
```

**Input logic:** Compare each number with its reversed digits.

**Output:**
```text
number of palindrome: 3
```

## Matrices

### Read and Display a Matrix

```python
m = int(input("enter rows: "))
n = int(input("enter columns: "))
print(f"enter {m * n} elements")
matrix = [[int(input()) for _ in range(n)] for _ in range(m)]
print("Entered Matrix:")
for row in matrix:
    print(" ".join(str(value) for value in row))
```

**Input logic:** Read the order, then build one list per row.

**Output:**
```text
enter rows: 2
enter columns: 2
enter 4 elements
9
6
5
1
Entered Matrix:
9 6
5 1
```

### Biggest Element in Each Row and Column

```python
m = int(input("enter rows: "))
n = int(input("enter columns: "))
print(f"enter {m * n} elements")
matrix = [[int(input()) for _ in range(n)] for _ in range(m)]
for i, row in enumerate(matrix, start=1):
    print(f"{i} row biggest element {max(row)}")
for j in range(n):
    print(f"{j + 1} column biggest element {max(matrix[i][j] for i in range(m))}")
```

**Input logic:** Use `max()` on each row, then on each column built by fixing the column index.

**Output:**
```text
enter rows: 2
enter columns: 2
enter 4 elements
5
6
8
9
1 row biggest element 6
2 row biggest element 9
1 column biggest element 8
2 column biggest element 9
```

### Row and Column Sums

```python
m = int(input("enter rows: "))
n = int(input("enter columns: "))
print(f"enter {m * n} elements")
matrix = [[int(input()) for _ in range(n)] for _ in range(m)]
for i in range(m):
    print(f"{i + 1} row sum is: {sum(matrix[i])}")
for j in range(n):
    print(f"{j + 1} column sum is: {sum(matrix[i][j] for i in range(m))}")
```

**Input logic:** Sum each row, then sum each column by fixing the column index.

**Output:**
```text
enter rows: 2
enter columns: 2
enter 4 elements
6
5
7
9
1 row sum is: 11
1 column sum is: 13
2 row sum is: 16
2 column sum is: 14
```

## Special Programs

### Leap Year

```python
year = int(input("Enter the year: "))
if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    print("it is a leap year")
else:
    print("not a leap year")
```

**Input logic:** A year is a leap year if it is divisible by `4` and not by `100`, or divisible by `400`.

**Output:**
```text
Enter the year: 2016
it is a leap year
```

### Days Between Two Dates

```python
from datetime import date

d1 = date(
    int(input("Enter yyyy: ")),
    int(input("Enter mm: ")),
    int(input("Enter dd: ")),
)
d2 = date(
    int(input("Enter yyyy: ")),
    int(input("Enter mm: ")),
    int(input("Enter dd: ")),
)
print(f"Number of Days between {d1} and {d2} is: {abs((d1 - d2).days)}")
```

**Input logic:** Read two dates, subtract them, and take the absolute value of the day difference.

**Output:**
```text
Enter yyyy: 2016
Enter mm: 8
Enter dd: 31
Enter yyyy: 2016
Enter mm: 9
Enter dd: 5
Number of Days between 2016-08-31 and 2016-09-05 is: 5
```

## Notes on the Conversion

- Python lists replace Java arrays and handle resizing automatically.
- `range()` replaces the Java `for` loop form; `range(n, 0, -1)` counts down.
- Python's `//` is integer division, matching Java's integer `/`.
- Use `str.isdigit()`, `str.isalpha()`, and `str.isalnum()` instead of comparing character codes.
- Where the original Java program had a logic bug (for example, `1` reported as prime or perfect, or a wrong biggest element), these versions use the corrected result.
- For large inputs, prefer built-in helpers such as `max()`, `min()`, `sum()`, `sorted()`, and `list.insert()` over hand-written loops.
