#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Transforme le texte en audio
#exec : text2wav.py

u"""
Auteur : Mickaelh
Licence : GPL v3

Description : Using pico2wave to ease from the recovery text to the
    clipboard or a file so unlimited.

System : the compliant systems under linux kernels: Debian, Ubuntu, Maemo ...

Installation required :
    - svox (pico2wave) http://packages.debian.org/source/sid/svox
    - Python install gtk (sudo apt-get install python-gtk2-dev)

Why this script: I love listening to my book on my mobile N900 while I
    drove on the road to work


How to use this script:
    - selected your text and copy (ctrl + c) and executed a command terminal
    $ ./text2wav.py

In the current directory of text2wav.py it will generate the article1.wav file article2.wav ...
good listening.

TODO:
    Development of the text file part and manage multiple text file so
    ilimiter vocalize books completely.
"""


 
import os, sys, gtk, getopt

limit_char = 30000

def text_clipboard():
    clipboard = gtk.clipboard_get()
    return clipboard.wait_for_text()

def text_file(arg):
    try:
        f = open(arg, 'r')
    except IOError:
        return "Erreur: le fichier est introuvable"
    return f.read()

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

def text_to_speech(txt):
    txt = txt.replace('"','')
    total_letter = len(txt)
    if total_letter > 1:
        list_txt = txt.split('.')
        list_txt = filter(None, list_txt)
    else:
        list_txt = []
        list_txt = u"Pas de texte trouvé."
    
    if list_txt:
        position = casier_txt(list_txt)
        
    else:
        return "pas de phrase"
        
    os.system('rm article*.wav')
    for index,value in enumerate(position):
        value =' '.join(value)
        print "Traduction en cours..."
        os.system('pico2wave -l fr-FR -w article%d.wav "%s"' % (index+1,value))
        print "Création du fichier : article%d.wav" % (index+1)
        
    return "Votre traduction est terminée"
    

def main(argv):
    text_file = ''
    try:
      opts, args = getopt.getopt(argv,"hi:",["help","input_text_file="])
    except getopt.GetoptError:
      print 'lecture_audio.py -i <input text file>'
      sys.exit(2)

    if opts:
        for opt, arg in opts:
          if opt in ('-h','--help'):
             print 'lecture_audio.py -i <input text file>'
             sys.exit()
          elif opt in ("-i", "--input_text_file"):
             txt = text_file(arg)
    else:
        txt = text_clipboard()
        
    print text_to_speech(txt)

if __name__ == "__main__":
   main(sys.argv[1:])
