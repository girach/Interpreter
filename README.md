# Interpreter
An interpreter for an self-defined language..
Language Syntax: 
-Similar to Bash script for loops,Decision making.
-Can handle functionalities like printing,Taking user's input,expression handling to C.
-For printing ... same syntax as of python2 .. compatible to print string-literals,numericals and combinations of them.
-To take user's input -- fromterminal:
Ex: "q = fromterminal:" --> this statement without quotes will assign the input given to q(even if it is not initialised) :) 

Check in test_interpretor.txt for sample code in defined language which covers all possible syntactical terms and see the output by running interpretor.py3 ... similar for toy_prof.py3.

Main difference between toy_prof.py3 and interpretor.py3 is the way they execute the code.. Former does it in HTML fashion.. it will execute until the code is correct without any syntactical errors and terminates immidiately as it encounters an error..while the latter .. will not execute until the code is syntactically correct  if it is error free .. it will execute automatically ... as in High-level languages like python.
