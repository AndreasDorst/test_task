#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import chardet
from sys import getdefaultencoding

CODING = 'utf-8'


def out_color_text(text, color):
    if color == 'red':
        return f"\033[31m{text}\033[0m"
    elif color == 'yellow':
        return f"\033[33m{text}\033[0m"
    elif color == 'green':
        return f"\033[32m{text}\033[0m"
    else:
        return text


def recursive_traversal(path, level=1):
    '''
    Recursively convert folders and files to lowercase and convert all files to utf-8.
    '''
    print(f'Level: {level}\nContent: {os.listdir(path)}')
    for i in os.listdir(path):
        current_path = path + '\\' + i
        file_oldname = os.path.join(path, i)
        file_new_name = os.path.join(path, i.lower())
        os.rename(file_oldname, file_new_name)
        if os.path.isdir(current_path):
            print(out_color_text(f'going down to {current_path}', 'yellow'))
            recursive_traversal(current_path, level + 1)
            print(out_color_text(f'going back to {path}', 'yellow'))
        elif os.path.isfile(current_path):
            encoding_converter(current_path)


def encoding_converter(file_path):
    with open(file_path, 'rb') as f:
        text = f.read()
        enc = chardet.detect(text).get('encoding')
        print(f'{file_path} encoding: {enc}')
        if enc and enc.lower() != CODING:
            text = text.decode(enc)
            text = text.encode(CODING)
            with open(file_path, 'wb') as f:
                f.write(text)
                print(out_color_text(f'{file_path} - encoding complited ({CODING})', 'green'))
        else :
            print(out_color_text(f'{file_path} is in right encoding', 'green'))


recursive_traversal('Test_Recursive_start')

# if __name__ == "__main__":
#     print('Running recursive_traversal')
#     recursive_traversal(sys.argv[2])
