Pico_read_speaker
=================

Using Pico2wave to ease from the recovery text to the clipboard or a file so unlimited.

Pico2wave takes into account a limited number of characters, my program solves this problem.

Why this script: I love listening to my book on my mobile N900 while I
    drove on the road to work


Auteur : Mickaelh
version : 1.0.0
Licence : GPL v3

required
========

System : the compliant systems under linux kernels: Debian, Ubuntu, Maemo ...

The SVOX Pico engine is a software speech synthesizer for German, English (GB
 and US), Spanish, French and Italian.

Installation required :

    - svox (pico2wave) https://packages.debian.org/source/squeeze/svox
    - Python install gtk: $ sudo apt-get install python-gtk2-dev

Svox package maemo dispnible on https://openrepos.net/

installation order:

    - libttspico-data (https://openrepos.net/content/mickaelh/libttspico-data)
    - libttspico0 (https://openrepos.net/content/mickaelh/libttspico0)
    - libttspico-utils (https://openrepos.net/content/mickaelh/libttspico-utils)
    - libttspico-dev (https://openrepos.net/content/mickaelh/libttspico-dev)

How to use this script
======================

selected your text and copy (ctrl+c) and executed a command terminal

    $ ./text2wav.py [-l|--lang en-US]
    or
    $ ./text2wav.py -i <input text file> [-l|--lang en-US]

In the current directory of "text2wav.py" it will generate the article1.wav file article2.wav ...

Good listening.
