import json
import os
import random
from random import randint
import argparse


def password_generator(letters=True, symbols=False, numbers=False, duplicates=False, pass_length=8):
    """
    letters - приймає True або False, за замовчуванням True (відповідає за наявність літер в паролі верхнього і нижнього регістру)
    symbols - приймає True або False, за замовчуванням False (відповідає за наявність символів(!@#$%^&*()+) в паролі)
    numbers - приймає True або False, за замовчуванням False (відповідає за наявність цифр в паролі)
    duplicates - приймає True або False, за замовчуванням False(відповідає за наявність дублікатів символів)
    pass_length - приймає ціле число, за замовчуванням 8 (довжина паролю)
    """

    letters_data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols_data = "!@#$%^&*()+"
    numbers_data = "0123456789"
    compared_data = letters_data + symbols_data + numbers_data
    resulted_password = ""

    if pass_length < 8:
        return f"Your password is too short, symbols = {len(pass_length)}"

    # generating random letters with length = pass_length
    if letters:
        for i in range(pass_length):
            resulted_password += letters_data[randint(0, len(letters_data) - 1)]

    # generating random symbols with length = pass_length
    if symbols:
        for i in range(pass_length):
            resulted_password += symbols_data[randint(0, len(symbols_data) - 1)]

    # generating random numbers with length = pass_length
    if numbers:
        for i in range(pass_length):
            resulted_password += numbers_data[randint(0, len(numbers_data) - 1)]

    # choose random letters, symbols, numbers with length = pass_length
    resulted_password = random.sample(resulted_password, pass_length)

    # checking current letter and next one, if they are duplicated I choose and replace current symbol to new one
    # from compared_data string
    if duplicates:
        for i in range(len(resulted_password) - 1):
            if resulted_password[i] == resulted_password[i + 1]:
                resulted_password[i] = compared_data[randint(0, len(compared_data) - 1)]

    return ''.join(resulted_password)

def save_to_json_file(data):
    existing_data = []
    # check if data.json exists and not empty and read all info from file
    if os.path.exists("data.json") and os.path.getsize("data.json") != 0:
        with open("data.json", "r") as json_file:
            existing_data = json.load(json_file)

    # add new info to old info
    existing_data.append(data)

    # Write JSON to a file
    json_data = json.dumps(existing_data, indent=4)
    with open("data.json", "w") as json_file:
        json_file.write(json_data)


def get_all_data_from_json():
    existing_data = []
    # read all data from json file
    if os.path.exists("data.json") and os.path.getsize("data.json") != 0:
        with open("data.json", "r") as json_file:
            existing_data = json.load(json_file)
    return existing_data


def get_data_by_title(find_by_title):
    for each_data in get_all_data_from_json():
        if each_data["title"] == find_by_title:
            print(f"title:{each_data['title']}")
            print(f"login:{each_data['login']}")
            print(f"password:{each_data['password']}")


parser = argparse.ArgumentParser(description='Input your data')
parser.add_argument('--title', dest='title', type=str, help='Input your title')
parser.add_argument('--login', dest='login', type=str, help='Input your login')
parser.add_argument('--password', dest='password', type=str, help='Input your password')

parser.add_argument('--letters', dest='letters', nargs='?', type=str, help='Do you want letters in your password?')
parser.add_argument('--symbols', dest='symbols', nargs='?', type=str, help='Do you want symbols in your password?')
parser.add_argument('--numbers', dest='numbers', nargs='?', type=str, help='Do you want numbers in your password?')
parser.add_argument('--duplicates', dest='duplicates', nargs='?', type=str, help='Do you want duplicate symbols in your password?')
parser.add_argument('--length', dest='length', nargs='?', type=int, help='What password length should be?')


parser.add_argument('--get', dest='get', nargs='?', type=str, help='Get data from database')
args = parser.parse_args()

if args.title and args.login and args.password:
    if args.password != "random":
        save_to_json_file({
            "title": args.title,
            "login": args.login,
            "password": args.password,
        })
    else:
        if args.letters is not None and args.symbols is not None and args.numbers is not None and args.duplicates is not None and args.length is not None:
            save_to_json_file({
                "title": args.title,
                "login": args.login,
                "password": password_generator(args.letters, args.symbols, args.numbers, args.duplicates, args.length),
            })
        else:
            save_to_json_file({
                "title": args.title,
                "login": args.login,
                "password": password_generator(),
            })

if args.get:
    get_data_by_title(args.get)


# commands I have used for tests
# python main.py --title fb --login vlad --password random
# python main.py --title inst --login vlad --password 123456
# python main.py --title fb ------- shouldn't write data because it's not full
# python main.py --get fb
# python main.py --title fb --login vlad --password random --letters False ------- shouldn't write data because not all args was written
# python main.py --title fb --login vlad --password random --letters False --symbols False ------- shouldn't write data because not all args was written
# python main.py --title fb --login vlad --password random --letters False --symbols False --numbers False --duplicates False --length 10



