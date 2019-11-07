#+TITLE: Code generator made using Python

#+OPTIONS: ^:{} toc:nil
#+TOC: headlines 1
#+STARTUP: content

* Brief
The aim is to generate most repetitive code using a higher level langage.

* References

** [1] UML_2-4-1_Infrastructure_formal-11-08-05.pdf
available [[https://www.omg.org/spec/UML/2.4.1/About-UML/][here]]

** [2] UML_2-4-1_Superstructure_formal-11-08-06.pdf
available [[https://www.omg.org/spec/UML/2.4.1/About-UML/][here]]

** tutos:
- https://www.dabeaz.com/ply/ply.html
- https://developer.ibm.com/tutorials/au-lexyacc/
- http://www.cs.man.ac.uk/~pjj/cs2111/ex5_hint.html
- https://riptutorial.com/fr/python/example/31585/partie-2--analyse-d-entrees-tokenized-avec-yacc

* Implementation
** Model
The model should be able to represent any element of a header file.

The model is a subset of UML langage.

The reference documentation used to implement the model are [[*%5B1%5D UML_2-4-1_Infrastructure_formal-11-08-05.pdf][{1}]] and [[*%5B2%5D UML_2-4-1_Superstructure_formal-11-08-06.pdf][{2}]]

The adopted coding rules of a class are:
- __init__ parameters are the attributes defined in section 7.3 (Class Description of )
- the associations are defined inside __init__
- each field is private and available through a =@property=. The setter is also
  private and controls the type and value of the parameter.

** Input parser
