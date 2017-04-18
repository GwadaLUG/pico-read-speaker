txt2wave
=========

This program converts a text file to a .wav file. For this linux software Pico2Wave is used. What Pico2Wave does is that it takes limited number of characters for text-to-speech conversion. This program solves this problem.

Prerequisites
==============

System : the compliant systems under linux kernels: Debian, Ubuntu, Maemo ...

The SVOX Pico engine is a software speech synthesizer for German, English (GB and US), Spanish, French and Italian.

Installation required :

    - svox (pico2wave) https://packages.debian.org/source/squeeze/svox

Svox package maemo dispnible on https://openrepos.net/

Installation order:

    - libttspico-data (https://openrepos.net/content/mickaelh/libttspico-data)
    - libttspico0 (https://openrepos.net/content/mickaelh/libttspico0)
    - libttspico-utils (https://openrepos.net/content/mickaelh/libttspico-utils)
    - libttspico-dev (https://openrepos.net/content/mickaelh/libttspico-dev)
    or
    - sudo apt-get install libttspico0 libttspico-utils libttspico-data

Usage
=======

There are options given for the command-line input, which would basically provide the user specifications of what type of speech does he/she wants. The options are as follows :

    Options:
        -i, --input_text_file   reads a text file
        -l, --lang  Language (default: default_lang)

    Options for languages :
        en-US   English
        en-GB   Great Britain
        de-DE   German
        es-ES   Spanish
        fr-FR   French
        it-IT   Italian

    Command-line Input Type:

    $ ./text2wav.py [-i|--input_text_file] <input text file name> [-l|--lang fr-FR]

    Help Option :
        -h, --Help  Show this message

NOTE:
the optional parameter [-l | --lang] by default = en-GB

In the current directory of "text2wav.py" it will generate the audio_book.wav file.
