#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Transform text in wav audio
#exec : text2wav.py

import os, sys, getopt, wave

reload(sys)
sys.setdefaultencoding('utf8')

#limit char of pico2wave
limit_char = 30000
#choose default language between: 'en-US','en-GB','de-DE','es-ES','fr-FR','it-IT'
default_lang = 'en-GB'

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

def joinwavs(outfile = "audio_book.wav"):
    infiles = []

    for root, dirs, files in os.walk(os.getcwd()):
        for f in files:
            if f.startswith('voice_clips') and f.endswith('.wav'):
                infiles.append(f)

    infiles = sorted(infiles)

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

    os.system('rm voice_clips*.wav')

    return outfile

def wav2mp3(infile = "audio_book.wav"):
    outfile = ' %s.mp3' % infile[:-4]
    os.system('ffmpeg -i %s %s' % (infile, outfile))
    os.system('rm %s' % infile)
    return outfile

# execute command line pico2wave
def text_to_speech(txt, lang):
    list_lang = ['en-US', 'en-GB', 'de-DE', 'es-ES', 'fr-FR', 'it-IT']
    if lang not in list_lang:
        lang = default_lang

    txt = txt.replace('"', '')
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

    os.system('ln -s /dev/stdout /tmp/out.wav')
    for index,value in enumerate(position):
        if value:
            value =' '.join(value)
            print("Vocalising in %s ..." % (lang))
            os.system('pico2wave -l %s -w /tmp/out.wav "%s" | ffmpeg -i - -ar 48000 -ac 1 -ab 64k -f mp3 %d.mp3 -y' % (lang, value, index + 1))
            os.system('cat %d.mp3 >> audio_book.mp3 && rm %d.mp3' % (index + 1, index + 1))

    #outfile = joinwavs()
    #If you have ffmpeg installed:
    #outfile = wav2mp3()

def print_usage():
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
-h,--help   show this message''' % default_lang)

def main(argv):
    lang = ''
    input_text_file = ''

    try:
        opts, args = getopt.getopt(argv, "hi:l:", ["help", "input_text_file=", "lang="])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l', '--lang'):
            lang = arg
        else:
            lang = default_lang

        if opt in ('-h', '--help'):
            print_usage()
            sys.exit()
        elif opt in ('-i', '--input_text_file'):
            input_text_file = arg
            txt = text_file(input_text_file)

    print(text_to_speech(txt,lang))

    input_text_file = input_text_file[:-4]
    os.system('mv audio_book.mp3 %s.mp3' % input_text_file)

    print('Output file = %s.mp3' % input_text_file)

if __name__ == "__main__":
    main(sys.argv[1:])
