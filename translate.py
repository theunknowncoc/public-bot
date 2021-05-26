from google_trans_new import google_translator
import pyperclip

def trans(inp, lang):
    translator = google_translator()
    translation = translator.translate(inp, lang_tgt=lang)
    if type(translation) == list:
        translation = translation[0]
    print(translation.capitalize())
    pyperclip.copy(translation.capitalize())

def rtrans():
    z = True
    while z:
        try:
            i = input('sen? ')
            j = input('lang? ')
            trans(i, j)
            if i == '' or j == '':
                z = False
        except:
            pass

if __name__ == '__main__':
    rtrans()
