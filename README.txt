This project serves to lessen the manual labour needed when designing a Danish crossword.

HOW TO RUN
==========
In a bash terminal at the same directory as this file is located in, write:

  python wordjoin.py <string0> <string1>

where <string0> and <string1> are python strings following the rules on http://kryds.onlineordbog.dk/, e.g.  "k&?" and "l&*", where the special sign & denotes the common letter, and the other special signs represent the following:

Jokertegn
---------
? (spørgsmålstegn) erstatter præcis ét tegn
* (stjerne) ertatter nul eller flere tegn
# (kryds) erstatter en konsonant (gør søgning langsom)
@ (snabel-a) erstatter en vokal (gør søgning langsom)


IDEAS
=====
When the crossword is nearly done, e.g. the four corner words and several other full length words are done, it is relatively well constrained.
Perhaps this is the crucial first step at which to implement an automatic solver.
Development could begin at the end of a finished crossword.
Here the problem is very well constrained which eases the development.
Steps back can then be taken along with the process becomming more complex and automatic.

