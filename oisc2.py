# OISC2b has an updated coprocessor.
# It has very limited error testing.  Buyer beware.
# McChuck, April 18, 2022

import sys
import math
try:
    from getch import getch, getche         # Linux
except ImportError:
    from msvcrt import getch, getche        # Windows

def coprocessor(a, b, c, mode):
    try:
        if mode == 1:
            c = ~b
        elif mode == 2:
            c = b & a
        elif mode == 3:
            c = b | a
        elif mode == 4:
            c = b ^ a
        elif mode == 5:
            c = b << a
        elif mode == 6:
            c = b >> a
        elif mode == 7:                 # sign of b +1, 0, -1
            c = (b > 0) - (b < 0)
        elif mode == 8:
            c = int(math.floor(b))
        elif mode == 9:
            c = int(math.trunc(b))      # round down
        elif mode == 10:
            c = b - a
        elif mode == 11:
            c = b + a
        elif mode == 12:
            c = b * a
        elif mode == 13:                # integer division
            if a == 0:
                raise ValueError
            else:
                c = b // a
        elif mode == 14:                # b mod a
            if a == 0:
                raise ValueError
            else:
                c = b % a
        elif mode == 15:
            if a == 0:
                raise ValueError
            else:
                c = b / a
        elif mode == 16:                # b to power a
            if b == math.e:
                c = math.exp(a)
            else:
                c = b ** a
        elif mode == 17:                 # a root of b
            if a == 0:
                raise ValueError
            else:
                if b == 0:
                    c = 1
                else:
                    if a == 2:
                        c = math.sqrt(b)
                    else:
                        c = b ** (1 / a)
        elif mode == 18:                # logarithm
            if (b == 0) or (a == 0):
                raise ValueError
            else:
                if b == 10:
                    c = math.log10(a)
                elif b == 2:
                    c = math.log2(a)
                elif b == math.e:
                    c = math.log(a)
                else:
                    c = math.log(b, a)
        elif mode == 19:
            c = math.sin(b)
        elif mode == 20:
            c = math.cos(b)
        elif mode == 21:
            c = math.tan(b)
        elif mode == 22:
            c = math.asin(b)
        elif mode == 23:
            c = math.acos(b)
        elif mode == 24:
            c = math.atan(b)
        elif mode == 25:
            c = math.sinh(b)
        elif mode == 26:
            c = math.cosh(b)
        elif mode == 27:
            c = math.tanh(b)
        elif mode == 28:
            c = math.asinh(b)
        elif mode == 29:
            c = math.acosh(b)
        elif mode == 30:
            c = math.atanh(b)
        elif mode == 31:
            c = math.hypot(b, a)        # hypotenuse c**2 = a**2 + b**2
        elif mode == 32:
            a = math.pi
            b = math.e
            c = (1 + sqrt(5)) / 2       # phi golden ration
        elif mode == 33:
            c = math.radians(b)
        elif mode == 34:
            c = math.degrees(b)
        elif mode == 35:
            c = math.gcd(b, a)          # gretest common divisor
        elif mode == 36:
            c = math.perm(b, a)         # permutations a items from set size b (unique)
        elif mode == 37:
            c = math.comb(b, a)         # combinations a items from set size b (not unique)
        elif mode == 38:
            c = math.factorial(b)
        elif mode == 39:                # summation from 0 to b
            if type(b) != int:
                raise ValueError
            else:
                if b > 0:
                    c = (b * (b + 1)) // 2
                elif b == 0:
                    c = 0
                else:
                    c = (b * (b - 1)) // -2
        else:
            pass

        return([a, b, c])

    except (ValueError, IndexError):
        print("\nCoprocessor aborted at: ", mem[IP])
        print("A: ", a, "B: ", b)
        print(mem)
    except KeyboardInterrupt:
        print("\nCoprocessor interrupted at: ", mem[IP])
        print("A: ", a, "B: ", b)
        print(mem)

def direct_mem_check(ip, direct, maxmem):
    if abs(direct) > maxmem:
        print("Memory out of bounds at: ", ip, " : ", direct, "\n")
        raise ValueError

def indirect_mem_check(ip, indirect, maxmem, minmem):
    if indirect > maxmem or indirect < minmem:
        print("Memory out of bounds at: ", ip, " --> ", indirect, "\n")
        raise ValueError


def oisc2(posmem, negmem):
    posmem = posmem + [0, 0, 0, 0, 0, 0]  # Pad to ensure Halt.
    negmem = [0, 2, 0, 0, 0, 0, 0, 0, 0] + negmem + [0, 0, 0, 0, 0, 0]
    # IP, Next, Return, Reg a, Reg b, Reg c, Mode, MaxPosMem, MAxNegMem
    # To compute negmem addresses for user data, count from 0, add 10 and negate
    IP = -1
    NEXT = -2
    RET = -3
    rega = -4
    regb = -5
    regc = -6
    mode = -7
    maxpos = -8
    maxneg = -9
    negmem.reverse()
    mem = posmem+negmem
    mem[maxpos] = len(posmem) - 1
    mem[maxneg] = -len(negmem)
    print(mem[maxpos], mem[maxneg])
    try:
        while mem[IP] >= 0 and mem[IP] <= mem[maxpos]:
            a = mem[mem[IP]]
            b = mem[mem[IP]+1]
            mem[NEXT] = mem[IP]+2
            direct_mem_check(mem[IP], a, mem[maxpos])
            direct_mem_check(mem[IP]+1, b, mem[maxpos])
            if a > 0:
                if b > 0:
                    mem[b] -= mem[a]
                elif b == 0:
                    print(chr(mem[a]), end="", flush=True)
                else:
                    if mem[a] <= 0:
                        mem[RET] = mem[NEXT]
                        mem[NEXT] = abs(b)
            elif a == 0:
                if b > 0:
                    mem[b] = ord(getche())   # ord(sys.stdin.read(1))
                elif b == 0:
                    mem[NEXT] = -1
                else:
                    indirect_mem_check(mem[IP]+1, mem[abs(b)], mem[maxpos], mem[maxneg])
                    mem[mem[abs(b)]] = ord(getche()) #  ord(sys.stdin.read(1))
            else:
                indirect_mem_check(mem[IP], mem[abs(a)], mem[maxpos], mem[maxneg])
                if b > 0:
                    if mem[mem[abs(a)]] <= 0:
                        mem[RET] = mem[NEXT]
                        mem[NEXT] = b
                elif b == 0:
                    indirect_mem_check(mem[IP], mem[abs(a)], mem[maxpos], mem[maxneg])
                    print(chr(mem[mem[abs(a)]]), end="", flush=True)
                else:
                    indirect_mem_check(mem[IP]+1, mem[abs(b)], mem[maxpos], mem[maxneg])
                    mem[mem[abs(b)]] -= mem[mem[abs(a)]]
            mem[IP] = mem[NEXT]

            if mem[mode] != 0:
                answer = coprocessor(mem[rega], mem[regb], mem[regc], mem[mode])
                mem[rega] = answer[0]
                mem[regb] = answer[1]
                mem[regc] = answer[2]
                mem[mode] = 0

        print("\nOISC2 completed successfully.")

    except (ValueError, IndexError):
        print("\nOISC2 aborted at: ", mem[IP])
        print("A: ", a, "B: ", b)
        print(mem)
    except KeyboardInterrupt:
        print("\nOISC2 interrupted at: ", mem[IP])
        print("A: ", a, "B: ", b)
        print(mem)

    finally:
        print("\nFinished.")



def load_posdata(pf):
    mem = []
    for line in pf:
        a = line.replace(",", "").split()
        mem.extend(a)
    mem = [int(elm) for elm in mem]
    return(mem)

def load_negdata(nf):
    mem = []
    tmem = []
    for line in nf:
        a = line.replace(",", "").split()
        tmem.extend(a)
    for elm in tmem:
        fv = float(elm)
        iv = int(fv)
        if iv == fv:
            mem.extend([iv])
        else:
            mem.extend([fv])
    return(mem)

def main(args):
#    print(args)
    posmem = []
    negmem = []
    if len(args) < 1 or len(args) > 2:
        print("usage:  python oisc2.py posmem [negmem]")
    else:
        with open(args[0], 'r') as posf:
            posmem = load_posdata(posf)
            posf.close()
        if len(args) == 2:
            with open(args[1], 'r') as negf:
                negmem = load_negdata(negf)
                negf.close()
        oisc2(posmem, negmem)


if __name__ == '__main__':
    print("\nOISC2 starting up.\n")
    try:
        main(sys.argv[1:])
    except IndexError:
        print("usage:  python oisc2.py posmem [negmem]")
    finally:
        print("\nOISC2 shutting down.\n")




# 0 Z, Coprocessor     # You can't jump back to 0, so have to pad the beginning.
# 2 Start: L, -Cont
# 4 L, 0              # Print "Hello, world!" directly
# 6 M1, Start
# 8 M1, Start+2
# 10 Z, -Start
# 12 Z: . 0
# 13 M1: . -1
# 14 L: "Hello, world!\n"
# 29 LP: . L
# 30 Cont: -LP Halt
# 32 -LP 0            # Now print it again, but indirectly
# 34 -M1P -LPP
# 36 -M1P Cont
# 38 Halt: 0 0
# 40 M1P: . M1
# 41 LPP: . LP
# 42 RegA: . -4
# 43 RegB: . -5
# 44 RegC: . -6
# 45 Mode: . -7
# 46 T: . 0
# 47 TP: . T
# 48 Ans: . 0
# 49 Ret: . -3
# 50 RetP: . Ret
# 51 BackP: . Back  # unused 0
# 52 Asc0:   . -48
# 53 Asc-:  . 45
# 54 Coprocessor: CodePosition, T  # Print sign of code at CodePosition, cannot choose 0!
# 56 -TP -RegB
# 58 T T
# 60 -SignP -TP
# 62 -TP -Mode          # executes sign(RegB) --> RegC, should be -1
# 64 T T
# 66 -RegC -TP          # T = opposite sign
# 68 T Ans              # Ans = sign
# 70 T -PrintPos
# 72 Asc- 0
# 74 Asc0 T
# 76 T 0
# 78 27 0
# 80 T T
# 82 Z -ReturnToStart
# 84 PrintPos: T T
# 86 Asc0 Ans
# 88 Ans 0
# 90 27, 0
# 92 ReturnToStart: Ans Ans
# 94 27 0
# 96 Asc? 0
# 98 0 T
# 100 27 0
# 102 T 0
# 104 27 0
# 106 T T
# 108 Z -Start
# 110 Asc?: . 63
# 111 SignP: . -17      # negmem reference

