# -*- coding: utf-8 -*-
import requests
import sys
import re
import math
import urllib
from lxml import html
from bs4 import BeautifulSoup

#**********#
#* README *#
#**********#
#? ver. 1.2
#? Script gets a word info from https://dictionary.goo.ne.jp explanatory dictionary
#? ### How to use ###
#? # To get a word info:
#? py get_jp_word_info.py WORD
#? # To search for a word:
#? py get_jp_word_info.py WORD -search
#? # To show search results from n-th page for a word:
#? py get_jp_word_info.py WORD -search PAGE_NUMBER
#? # To show more examples of a word usage:
#? py get_jp_word_info.py WORD -more-usage PAGE_NUMBER
#? # To show more idioms with a word:
#? py get_jp_word_info.py WORD -more-idioms PAGE_NUMBER
#? # Display help:
#? py get_jp_word_info.py -help
#! ### TO DO LIST ###
#! Add feature to get info about kanji

dictionary = {'あ': 'а', 
            'い': 'и', 
            'う': 'у', 
            'え': 'э', 
            'お': 'о', 
            'ゃ': 'я', 
            'ゅ': 'ю', 
            'ょ': 'ё',
            'おお': 'о:',
            'ああ': 'а:',
            'いい': 'и:',
            'ええ': 'э:',
            'か': 'ка', 
            'き': 'ки',
            'く': 'ку',
            'け': 'кэ',
            'こ': 'ко',
            'きゃ': 'кя',
            'きゅ': 'кю',
            'きょ': 'кё',
            'さ': 'са',
            'し': 'си',
            'す': 'су',
            'せ': 'сэ',
            'そ': 'со',
            'しゃ': 'ся',
            'しゅ': 'сю',
            'しょ': 'сё',
            'た': 'та',
            'ち': 'ти',
            'つ': 'цу',
            'て': 'тэ',
            'と': 'то',
            'ちゃ': 'тя',
            'ちゅ': 'тю',
            'ちょ': 'тё',
            'な': 'на',
            'に': 'ни',
            'ぬ': 'ну',
            'ね': 'нэ',
            'の': 'но',
            'にゃ': 'ня',
            'にゅ': 'ню',
            'にょ': 'нё',
            'は': 'ха',
            'ひ': 'хи',
            'ふ': 'фу',
            'へ': 'хэ',
            'ほ': 'хо',
            'ひゃ': 'хя',
            'ひゅ': 'хю',
            'ひょ': 'хё',
            'ま': 'ма',
            'み': 'ми',
            'む': 'му',
            'め': 'мэ',
            'も': 'мо',
            'みゃ': 'мя',
            'みゅ': 'мю',
            'みょ': 'мё',
            'ら': 'ра',
            'り': 'ри',
            'る': 'ру',
            'れ': 'рэ',
            'ろ': 'ро',
            'りゃ': 'ря',
            'りゅ': 'рю',
            'りょ': 'рё',
            'わ': 'ва',
            'ゐ': 'ви',
            'ゑ': 'вэ',
            'を': 'во',
            'ん': 'н',
            'が': 'га',
            'ぎ': 'ги',
            'ぐ': 'гу',
            'げ': 'гэ',
            'ご': 'го',
            'ぎゃ': 'гя',
            'ぎゅ': 'гю',
            'ぎょ': 'гё',
            'ざ': 'дза',
            'じ': 'дзи',
            'ず': 'дзу',
            'ぜ': 'дзэ',
            'ぞ': 'дзо',
            'じゃ': 'дзя',
            'じゅ': 'дзю',
            'じょ': 'дзё',
            'だ': 'да',
            'ぢ': 'дзи',
            'づ': 'дзу',
            'で': 'дэ',
            'ど': 'до',
            'ぢゃ': 'дзя',
            'ぢゅ': 'дзю',
            'ぢょ': 'дзё',
            'ば': 'ба',
            'び': 'би',
            'ぶ': 'бу',
            'べ': 'бэ',
            'ぼ': 'бо',
            'びゃ': 'бя',
            'びゅ': 'бю',
            'びょ': 'бё',
            'ぱ': 'па',
            'ぴ': 'пи',
            'ぷ': 'пу',
            'ぺ': 'пэ',
            'ぽ': 'по',
            'ぴゃ': 'пя',
            'ぴゅ': 'пю',
            'ぴょ': 'пё'
            }

def double_sound(substring, length):
    
    if length == 2:
        output_substring = dictionary[substring[0]+substring[1]][0] + dictionary[substring[0]+substring[1]]
    elif length ==1:
        output_substring = dictionary[substring[0]][0] + dictionary[substring[0]]
    
    return output_substring

def make_transcription(string):
    
    output_string = ' '
    
    n = 0
    while n < len(string):

        if string[n:n+2] in dictionary.keys():
            output_string += dictionary[string[n]+string[n+1:n+2]]
            n+=2
        elif string[n] == 'う':
            if output_string[-1] in ['у', 'о', 'ё', 'ю']:
                output_string += ':'
                n+=1
            elif output_string[-1] not in ['у', 'о', 'ё', 'ю']:
                output_string += dictionary[string[n]]
                n+=1
        elif string[n] in dictionary.keys():
            output_string += dictionary[string[n]]
            n+=1
        elif string[n] == 'っ':
            if string[n+1:n+3] in dictionary.keys() and len(string[n+1:n+3]) == 2:
                output_string += double_sound(string[n+1:n+3], 2)
                n+=3
            elif string[n+1:n+2] in dictionary.keys() and len(string[n+1:n+2]) == 1:
                output_string += double_sound(string[n+1:n+2], 1)
                n+=2
            elif string[n+1:n+2] == ' ':
                output_string += ' '
                n+=1
            else:
                output_string += ''
                n+=1
        elif string[n] == ' ':
            output_string += ' '
            n+=1
        else:
            output_string += ''
            n+=1
    
    if output_string[-1] == 'у' and (output_string[-2] in ['у', 'о', 'ё', 'ю']):
        output_string = output_string[:-1]
        output_string += ':'
    
    output_string = output_string.lstrip()

    # ^(ха)\s|(?<=[ \t])(ха)(?=[ \t])|\s(ха)$|^(ха)$
    output_string = re.sub(r'^(ха)\s', 'ва ', output_string)
    output_string = re.sub(r'\s(ха)$', ' ва', output_string)
    output_string = re.sub(r'^(ха)$', 'ва', output_string)
    output_string = re.sub(r'(?<=[ \t])(ха)(?=[ \t])', ' ва ', output_string)

    return output_string

# <--- Debug function for checking if the page exists
# def page_is_found(url):

#     page = requests.get(url)
#     html = page.text
#     soup = BeautifulSoup(html, 'lxml')
    
#     if re.search(r'404', soup.title.text).group(0) is True:
#         return False
#     else:
#         return True
# --->

def show_help():
    print("""
                                                                                            
.oPYo.          o      o  .oPYo.                               8    o        d'b        
8    8          8      8  8    8                               8             8          
8      .oPYo.  o8P     8 o8YooP'   o   o   o .oPYo. oPYo. .oPYo8   o8 odYo. o8P  .oPYo. 
8   oo 8oooo8   8      8  8        Y. .P. .P 8    8 8  `' 8    8    8 8' `8  8   8    8 
8    8 8.       8      8  8        `b.d'b.d' 8    8 8     8    8    8 8   8  8   8    8 
`YooP8 `Yooo'   8    oP'  8         `Y' `Y'  `YooP' 8     `YooP'    8 8   8  8   `YooP' 
:....8 :.....:::..:::...::..:::::::::..::..:::.....:..:::::.....::::....::..:..:::.....:
:::::8 :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::..:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    About: Script gets a word info from https://dictionary.goo.ne.jp explanatory dictionary
    Version: 1.2

    ### How to use ###

    # To get a word info:
    py get_jp_word_info.py WORD
    
    # To search for a word:
    py get_jp_word_info.py WORD -search

    # To show search results from n-th page for a word:
    py get_jp_word_info.py WORD -search PAGE_NUMBER

    # To show more examples of a word usage:
    py get_jp_word_info.py WORD -more-usage PAGE_NUMBER

    # To show more idioms with a word:
    py get_jp_word_info.py WORD -more-idioms PAGE_NUMBER

    # Display help:
    py get_jp_word_info.py -help
    """)

def IsInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def get_word_type(string):
    word_type = ''
    if re.search(r'(kanji)', string).group(1) == 'kanji':
        word_type += 'Kanji'
    else:
        word_type += 'Word'
    
    return word_type


def get_word_info(string):
    
    url = 'https://dictionary.goo.ne.jp/word/'+string
    
    word = ''
    hiragana_from_title = ''
    hiragana_ru_transcription_from_title = ''
    usage_list = []
    idioms_list = []

    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, 'lxml')

    try:
        # <--- Writing and hiragana section
        word = re.search(r'([^（]+)', soup.title.text).group(0)
        hiragana_from_title = re.search(r'\（(.+)\）', soup.title.text).group(1)
        hiragana_ru_transcription_from_title = make_transcription(hiragana_from_title)

        print("[WORD]: ", word)
        print("[HIRAGANA]: ", hiragana_from_title)
        print("[HIRAGANA RU_TRANSCRIPTION]: ", hiragana_ru_transcription_from_title)
        print('')
        # --->

        # <--- Meaning section
        print('====================')
        print("=== WORD MEANING ===")
        print('====================')
        meaning = soup.find('div', class_ = 'content-box contents_area meaning_area p10')
        print(meaning.get_text())
        print('')
        # --->

        # <--- Usage section
        url_usage = 'https://dictionary.goo.ne.jp/word/'+string+'/example/'
        page_usage = requests.get(url_usage)
        html_usage = page_usage.text
        soup = BeautifulSoup(html_usage, 'lxml')

        print('==================')
        print("=== WORD USAGE ===")
        print('==================')
            
        try:
            usage_list = soup.find('div', class_ = 'example_sentence').find_all('li')
            for usage in usage_list:
                usage = usage.find('p', class_ = 'text').text
                print("---> ", usage)
            print('')
        except:
            print("[HMMM...] NO USAGE FOUND!")
            print('')
        # --->
        
        # <--- Idioms section
        url_idioms = 'https://dictionary.goo.ne.jp/word/'+string+'/idiom/'
        page_idioms = requests.get(url_idioms)
        html_idioms = page_idioms.text
        soup = BeautifulSoup(html_idioms, 'lxml')

        print('==============')
        print("=== IDIOMS ===")
        print('==============')
  
        try:
            idioms_list = soup.find('div', class_ = 'example_sentence').find_all('li')
            for idiom in idioms_list:
                idiom_title = idiom.find('p', class_ = 'title').text
                idiom = idiom.find('p', class_ = 'text').text
                print('')
                print("---> ", idiom)
                print("SOURCE: ", idiom_title)
            print('')
        except:
            print("[HMMM...] NO IDIOMS FOUND!")
            print('')
        # --->
   
    except:
        print("[OOOPS!] NO SUCH WORD IN DICTIONARY!")
        print("[NO WORD INFO FOUND!]")
        print(">>>--------> [HINT] >>>-------->")
        print("A little search can help! To find your word (maybe), please, execute:")
        print("python3 get_jp_word_info.py %s -search" % string)


def search_word(string, page='1'):

    try:
        url_search = 'https://dictionary.goo.ne.jp/srch/jn/'+string+'/m0p'+page+'u/'
        url_search_all = 'https://dictionary.goo.ne.jp/srch/all/'+string+'/m0u/'

        page = requests.get(url_search)
        html = page.text
        soup = BeautifulSoup(html, 'lxml')

        search_page_number = re.search(r'm0p(\d+)u', url_search).group(1)

        print('======================')
        print("??? SEARCH RESULTS ???")
        print('======================')
        print('======= PAGE %s =======' % search_page_number)
        print('')
        print('[QUERY WORD]: ', string)
        print('')

        # <--- Extract total results count
        page_temp = requests.get(url_search_all)
        html_temp = page_temp.text
        soup_temp = BeautifulSoup(html_temp, 'lxml')

        total_search_results_object = soup_temp.section.h2.text
        total_search_results_number = re.search(r'\((\d+)\)', total_search_results_object).group(1)
        print('[TOTAL SEARCH RESULTS]: ', total_search_results_number)
        print('[TOTAL SEARCH RESULTS PAGES]: ', math.ceil(int(total_search_results_number)/10))
        print('')
        # --->

        search_results_list = soup.find('div', class_ = 'example_sentence').find_all('li')

        result_line = 1
        for search_result in search_results_list:
            search_result_title = search_result.find('p', class_ = 'title').text
            search_result_text = search_result.find('p', class_ = 'text').text
            print('(%i) --->' % result_line)
            print("[WORD TITLE]: ", search_result_title)
            print("[WORD]: ", urllib.parse.unquote(re.search(r'kanji\/(.+)\/|word\/(.+)\/', search_result.a['href']).group(2)))
            try:
                if get_word_type(search_result.a['href']) == 'Kanji':
                    print("[WORD TYPE]: Kanji")
            except:
                print("[WORD TYPE]: Word")
            print("[SHORT INFO]", search_result_text)
            result_line += 1

    except:
        print("[OOOPS!] WRONG SEARCH RESULTS PAGE NUMBER!")


def search_more_usage(string, page):
    
    try:
        print('======================')
        print("??? SEARCH RESULTS ???")
        print('===== MORE USAGE =====')
        print('======= PAGE %s =======' % page)
        print('')
        print('[QUERY WORD]: ', string)
        print('')

        url_usage = 'https://dictionary.goo.ne.jp/word/'+string+'/example/'+page+'/'
        page_usage = requests.get(url_usage)
        html_usage = page_usage.text
        soup = BeautifulSoup(html_usage, 'lxml')

        total_more_usage_results_object = soup.find('div', class_= 'basic_title nolink l-pgTitle').h1.text
        total_more_usage_results_number = re.search(r'\((\d+)\)', total_more_usage_results_object).group(1)
        print('[TOTAL SEARCH RESULTS (MORE USAGE)]: ', total_more_usage_results_number)
        print('[TOTAL SEARCH RESULTS PAGES (MORE USAGE)]: ', math.ceil(int(total_more_usage_results_number)/10))
        print('')

        usage_list = soup.find('div', class_ = 'example_sentence').find_all('li')
        for usage in usage_list:
            usage = usage.find('p', class_ = 'text').text
            print("---> ", usage)
        print('')

    except:
        print("[HMMM...] NO MORE USAGE EXAMPLES FOUND!")
        print('')


def search_more_idioms(string, page):
    
    try:
        print('======================')
        print("??? SEARCH RESULTS ???")
        print('===== MORE IDIOMS ====')
        print('======= PAGE %s =======' % page)
        print('')
        print('[QUERY WORD]: ', string)
        print('')

        url_idioms = 'https://dictionary.goo.ne.jp/word/'+string+'/idiom/'+page+'/'
        page_idioms = requests.get(url_idioms)
        html_idioms = page_idioms.text
        soup = BeautifulSoup(html_idioms, 'lxml')

        total_more_idioms_results_object = soup.find('div', class_= 'basic_title nolink l-pgTitle').h1.text
        total_more_idioms_results_number = re.search(r'\((\d+)\)', total_more_idioms_results_object).group(1)
        print('[TOTAL SEARCH RESULTS (MORE IDIOMS)]: ', total_more_idioms_results_number)
        print('[TOTAL SEARCH RESULTS PAGES (MORE IDIOMS)]: ', math.ceil(int(total_more_idioms_results_number)/10))
        print('')

        idioms_list = soup.find('div', class_ = 'example_sentence').find_all('li')
        for idiom in idioms_list:
            idiom_title = idiom.find('p', class_ = 'title').text
            idiom = idiom.find('p', class_ = 'text').text
            print('')
            print("---> ", idiom)
            print("SOURCE: ", idiom_title)
        print('')

    except:
        print("[HMMM...] NO MORE IDIOM EXAMPLES FOUND!")
        print('')


if len(sys.argv) == 2:
    if sys.argv[1] == '-help':
        show_help()
    else:
        get_word_info(sys.argv[1])

elif len(sys.argv) == 3:
    if sys.argv[2] == '-search':
        search_word(sys.argv[1])
    else:
        print("[ERROR!] INVALID ARGUMENTS!")

elif len(sys.argv) == 4:
    if sys.argv[2] == '-search' and (IsInt(sys.argv[3]) is True):
        search_word(sys.argv[1], str(sys.argv[3]))
    elif sys.argv[2] == '-more-usage' and (IsInt(sys.argv[3]) is True):
        search_more_usage(sys.argv[1], str(sys.argv[3]))
    elif sys.argv[2] == '-more-idioms' and (IsInt(sys.argv[3]) is True):
        search_more_idioms(sys.argv[1], str(sys.argv[3]))
    else:
        print("[ERROR!] INVALID ARGUMENTS!")
else:
    print("[ERROR!] INVALID ARGUMENTS!")
