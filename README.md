Waveshaper
==========

WORK IN PROGRESS!

A simple proof of concept implementation of a tool that draws waveforms, done in python.
This is a simple way to play around with architecture before implementing the thing in
a stricter language.

It draws huge inspiration (wave shapes, drawing methodology) from the tikz-timing package by Martin Scharrer.

Executables
===========

* test.py: just there to play around
* create\_overview.py: creates overview.html which contains all symbols and
  transitions

Grammar
=======

    LHLHLHLHL
    2L2H
    2{LH}
    D(0xAA)
    O(LH,HL)
    LH{[grey]HLHLHL}

    symbol ::= [a-zA-Z]
    identifier ::= [a-zA-Z_]+
    value ::= identifier
    string ::= '"' [^"]+ '"' | [a-zA-Z0-9]+
    natural ::= [0-9]+
    float ::= number ('.' number)? | '.' number
    parameter ::= '{' sequence '}' | string
    parameters ::= parameter ( "," parameter )*
    instruction ::=   float? symbol ( '(' parameters ')')? 
                    | '[' ( indentifier '=' )? value ']'
    sequence ::= number? '{' instruction+ '}' | instruction+

TODO
====

* much that is not on this list
* metastable symbol?
* pattern for X
* weak H/L symbols?
