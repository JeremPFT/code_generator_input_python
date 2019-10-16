#+TITLE: Code Generator, python implementation. README for Tests
#+STARTUP: showeverything
#+OPTIONS: ^:{}

* Test 1

** Description

Create a project named =test_1= in directory  =~/tests/test_1=

Input file is =code_generator_py/tests/test_1.dsl=

Template file is =code_generator_py/tests/test_1.template=

Expected file is =code_generator_py/tests/test_1.expected=

/note: directory =~/tests= is created at the beginning of the test, deleted at the end/

** Validation

- directories created:
  - =~/tests/test_1=
  - =~/tests/test_1/src=
- files created:
  - =~/tests/test_1/test_1.gpr=

: with "../common/shared.gpr";
:
: library project Test_1 is
:
:   for Create_Missing_Dirs use "True";
:
:   Src_Lst := ();
:   Src_Lst := Src_Lst & "./src_lib";
:   for Source_Dirs use Src_Lst;
:
:   Exc_Src_Lst := ();
:   for Excluded_Source_Files use Exc_Src_Lst;
:
:   for Object_Dir use Shared.Object_Dir;
:   for Library_Dir use Shared.Library_Dir;
:
:   for Library_Name use "test_1";
:   for Library_Kind use "static";
:
:   package Compiler renames Shared.Compiler;
:
:   package Builder renames Shared.Builder;
:
: end Test_1;

** some things to add later

*** a README.org file for git repository

- A brief description of the project, which will be the title of the README file.
- A little longer description, which will be the 'Brief' section of the README file.
- The readme should have the following model:

: #+TITLE:	README for Code Generator project, Model module
: #+AUTHOR:	Jeremy Piffret
: #+EMAIL:	j.piffret@gmail.com
: #+DATE:		2019-09-06
: #+STARTUP:	content
:
: * Brief
:
: Model module defines the objects used as abstraction to generate a project from
: a specification.

* Test 002

* COMMENT Local Variables
# Local Variables:
# mode:org
# coding: utf-8-unix
# End:
