OISC:2
Obfuscated Indirect Subleq with Coprocessor: 2 word instructions

As the name implies, OISC:2 is a variant of Subleq.  However, it has been both extended and obfuscated by using the trichotomy of numbers to have different effects based on the positive, negative, or zero value of each of the two words per instruction.

OISC:2 accepts a mandatory positive and an optional negative memory file.  The coprocessor is activated by sending data to the Mode address (-7).
Positive memory is loaded as integers only.  Jumps to negative memory Halt.  Negative memory can be addressed by indirection, but instructions are only in positive memory.

The sample code (posmem.o2c and negmem.o2c) prints the sign of a memory word, inputs and prints a keyobard character, and prints "Hello, world!" using direct and then indirect addressing.


Two word instruction:  A B

If A & B are both positive: [B]=[B]-[A]
If A & B are both negative: [[B]]=[[B]]-[[A]]

If A is positive and B is negative: IF [A] <= 0 Jump to |B|
If A is negative and B is positive: IF [[A]] <= 0 Jump to B

If A is 0 and B is positive: STDIN --> [B]
If A is 0 and B is negative: STDIN --> [[B]]

If A is positive and B is 0: [A] --> STDOUT
If A is negative and B is 0: [[A]] --> STDOUT

If A & B are both 0: HALT


Negative Memory
Address        Function
-1             IP (initially 0)
-2             NEXT (always IP+3)
-3             RETURN (initially 0, set to NEXT before any jump.)
-4             Register a
-5             Register b
-6             Register c
-7             Mode (activates a, b, c; then resets to 0)
-8             MaxPos memory size
-9             MaxNeg memory size
-10...         Data (user address computation: start from 0, add 10, negate)


Coprocessor
Mode      Function
0         NOP
1         c = ~b (bitwise not)
2         c = b & a (bitwise and)
3         c = b | a (bitwise or)
4         c = b ^ a (bitwise xor)
5         c = b << a (shift b left by a bits)
6         c = b >> a (shift b right by a bits)
7         sign of b   (+1, 0, -1)
8         floor of b (integer)
9         truncate b (round down, integer)
10        c = b - a
11        c = b + a
12        c = b * a
13        c = b // a (integer division)
14        c = b % a (mod, integer remainder)
15        c = b / a
16        c = b to power of a
17        c = a root of b
18        c = log base b of a
19        c = sin(b)
20        c = cos(b)
21        c = tan(b)
22        c = asin(b)
23        c = acos(b)
24        c = atan(b)
25        c = sinh(b)
26        c = cosh(b)
27        c = tanh(b)
28        c = asinh(b)
29        c = acosh(b)
30        c = atanh(b)
31        c = sqrt(b**2 + a**2)  (hypotenuse)
32        a = pi, b = e, c = phi (golden ration)
33        c radians <-- b degrees
34        c degrees <-- b radians
35        c = greatest common divisor of b and a
36        c = a permutations of b items (unique)
37        c = a combinations of b items (not unique)
38        c = b! (integer factorial)
39        c = sum of 0..b (integers, works with negatives)

