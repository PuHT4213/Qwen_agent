import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.chinese_character_detector import is_chinese_char


def split_text(text):
    '''
    For texts like "我想对你说：“I love You”。"，return["我", "想", "对", "你", "说", "“" ,"I", "love", "You", "”" , "。"]
    Which means split the text into words and special symbols.
    '''
    text = text.strip()
    if len(text) == 0:
        return []
    result = []
    i = 0
    while i < len(text):
        if is_chinese_char(text[i]):
            result.append(text[i])
            i += 1
        elif re.match(u'[a-zA-Z0-9]', text[i]):
            word = ""
            while i < len(text) and re.match(u'[a-zA-Z0-9]', text[i]):
                word += text[i]
                i += 1
            result.append(word)
        elif text[i] == ' ':
            i += 1
        else:
            result.append(text[i])
            i += 1

    return result

def main():
    text = "我想对你说：“I love You for 1000 times”。"
    print(split_text(text))

if __name__ == '__main__':
    main()