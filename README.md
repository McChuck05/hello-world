# hello-world
## McChuck05's warehouse for [Esolang](https://esolangs.org/wiki/Main_Page) strangeness

Check out [Truttle1](https://www.youtube.com/c/Truttle1)'s esolang videos.

### [Subleq](https://esolangs.org/wiki/Subleq) derivatives

**OISC:2**  Obfuscated Indirect Subleq with Coprocessor: 2 word instructions.

**OISC:2bis** A much imporved version of OISC:2.

**Subleq+**  Subleq with negatives used for indirect addressing, inspired by [Lawrence Woodman](https://techtinkering.com/2009/05/15/improving-the-standard-subleq-oisc-architecture/).

**Subleq-improved** Can you tell I really enjoyed messing around with Subleq, and making improvements?

**OISC:3** 3 word instruction Subleq variant, much easier to use.

**Trichotomy** An even better Subleq variant.

### Forth/False/Factor derivatives

**False** An esolang from 1993.  It's a very simplified and yet somehow improved version of Forth-like, stack based, concatenative programming.

**Falsish** A remarkably useful variant of False, with local variable (and stack) scope inspired by the esolang "fish" ><>.

**Listack** Inspired by Falsish and [Factor][https://concatenative.org/wiki/view/Factor].  Listack is a postfix style, stack based, concatenative language, but allows prefix and infix variant operators for most functions.  It is impemented as a flat/stackless language - there are no call/return stacks.  All functions are simply pushed to the fronnt of the command queue.  It works somewhat like a Turing tape engine:  commands come in from the right, data goes out to the left.  Has local variables (A..Z) and scope.  Has global side stacks (a..z).  Allows user created local variables and global functions.  Can import program files.
