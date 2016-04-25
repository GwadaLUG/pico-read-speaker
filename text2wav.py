#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Transform text in wav audio
#exec : text2wav.py

u"""
Auteur  : Mickaelh
version : 1.1.0
Licence : GPL v3

Description : Using pico2wave to ease from the recovery text to the
    clipboard or a file so unlimited.
    pico2wave takes into account a limited number of characters, my program solves this problem.

System : the compliant systems under linux kernels: Debian, Ubuntu, Maemo ...

Installation required :
    - svox (pico2wave) https://packages.debian.org/source/squeeze/svox
    - Python install gtk : $ sudo apt-get install python-gtk2-dev

Svox package maemo dispnible on https://openrepos.net/
installation order:
    - libttspico-data (https://openrepos.net/content/mickaelh/libttspico-data)
    - libttspico0 (https://openrepos.net/content/mickaelh/libttspico0)
    - libttspico-utils (https://openrepos.net/content/mickaelh/libttspico-utils)
    - libttspico-dev (https://openrepos.net/content/mickaelh/libttspico-dev)


Why this script: I love listening to my book on my mobile N900 while I
    drove on the road to work


How to use this script:
    - selected your text and copy (ctrl + c) and executed a command terminal
    $ ./text2wav.py

In the current directory of text2wav.py it will generate only one file, named chapter.wav
I you want it in mp3 and you have ffmpeg installed, uncomment line 155
Good listening.

TODO:
    Development of the text file part and manage multiple text file so
    ilimiter vocalize books completely.
"""



import os, sys, gtk, getopt, wave

#limit char of pico2wave
limit_char = 30000
#choose default language between: 'en-US','en-GB','de-DE','es-ES','fr-FR','it-IT'
default_lang = 'en-US'

# get text from (ctrl + c)
def text_clipboard():
    clipboard = gtk.clipboard_get()
    return clipboard.wait_for_text()

#get text from file
def text_file(arg):
    try:
        f = open(arg, 'r')
    except IOError:
        return "Error: file not found"
    return f.read()

#cut the text by sentence
def casier_txt(list_txt):
    current_letter=0
    list_sentence = []
    list_chapter = []

    for sentence in list_txt:
        current_letter += len(sentence)
        if limit_char < current_letter:
            if list_sentence:
                list_chapter.append(list_sentence)
                list_sentence = []
            else:
                list_sentence.append(u'%s.' % sentence)
                list_chapter.append(list_sentence)
                list_sentence = []
            current_letter = 0
        else:
            list_sentence.append(u'%s.' % sentence)

    if list_sentence:
        list_chapter.append(list_sentence)

    return list_chapter

def joinwavs(outfile = "chapter.wav"):
    infiles = []

    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if f.startswith('article') and f.endswith('.wav'):
                infiles.append(f)

    if len(infiles) > 1:
        data = []
        for infile in infiles:
            w = wave.open(infile, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()

        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        for params,frames in data:
            output.writeframes(frames)
        output.close()
    else:
        os.system('rm %s' % outfile)
        os.system('mv %s %s' % (infiles[0], outfile))
    return outfile

def wav2mp3(infile = "chapter.wav"):
    outfile = ' %s.mp3' % infile[:-4]
    os.system('ffmpeg -i %s %s' % (infile, outfile))
    os.system('rm %s' % infile)
    return outfile

# execute command line pico2wave
def text_to_speech(txt,lang):
    list_lang = ['en-US','en-GB','de-DE','es-ES','fr-FR','it-IT']
    if lang not in list_lang:
        lang = default_lang

    txt = txt.replace('"','')
    total_letter = len(txt)
    if total_letter > 1:
        list_txt = txt.split('.')
        list_txt = filter(None, list_txt)
    else:
        list_txt = []
        list_txt = u"No text found."

    if list_txt:
        position = casier_txt(list_txt)

    else:
        return "No sentence"

    os.system('rm article*.wav')
    for index,value in enumerate(position):
        if value:
            value =' '.join(value)
            print("Translating in %s ..." % (lang))
            os.system('pico2wave -l %s -w article%02d.wav "%s"' % (lang, index+1, value))
            print("File Creation: article%02d.wav" % (index+1))

    outfile = joinwavs()
    #If you have ffmpeg installed:
    #outfile = wav2mp3()

    return "Speech complete!. The result is in: %s" % outfile

def main(argv):
    lang = ''
    try:
        opts, args = getopt.getopt(argv,"hi:l:",["help","input_text_file=","lang="])
    except getopt.GetoptError:
        sys.exit(2)

    if opts:
        for opt, arg in opts:
            if opt in ('-l','--lang'):
                lang = arg
            else:
                lang = default_lang

            if opt in ('-h','--help'):
                print(
'''Usage: text2wav.py [option] [-i|--input_text_file text_file]

Without -i option verifies if there is a text copied to clipboard

Options:
    -i, --input_text_file   reads a text file
    -l, --lang  Language (default: "%s")

Options lang:
    en-US   English
    en-GB   Great Britain
    de-DE   German
    es-ES   Spanish
    fr-FR   French
    it-IT   Italian

Help option:
    -h,--help   show this message'''
                % default_lang )
                sys.exit()
            elif opt in ('-i', '--input_text_file'):
                txt = text_file(arg)
            else:
                txt = text_clipboard()
    else:
        txt = text_clipboard()

    print(text_to_speech(txt,lang))

if __name__ == "__main__":
   main(sys.argv[1:])
