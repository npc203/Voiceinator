from bs4 import BeautifulSoup

from recognise import mic
from utils import *
from writer import Writer


def process_speech(speech, data):
    for command in commands:
        if command in speech:
            return commands[command](speech, command, data)


commands = {
    "save": Writer().write_html,
    "image": add_asset,
    "database": db_make,
    "add": getitem,
    "create": getitem,
    "background": bg,
    "move": moveitem,
    "respons": resp,
}


def main_loop():

    pen = Writer()

    data = pen.loadfile()

    while True:

        # Getting text in 3 tries
        for _ in range(3):
            response = mic.recognize_speech()
            if response["success"]:
                speech = response["transcription"]
                break
        else:
            print("Too many errors stopping")
            break

        print("you said:", speech)
        if speech:
            if "exit" == speech:
                break
            if valid_edit := process_speech(speech, data):
                data = valid_edit
        else:
            print("retry")


def test_loop(gen):
    pen = Writer()
    data = pen.loadfile()

    for speech in gen:
        if valid_edit := process_speech(speech, data):
            data = valid_edit


if __name__ == "__main__":
    # main_loop()
    test_loop(
        [
            "can you add navbar",
            "add title with content Voiceinator",
            "move title to center",
            "create login page",
            "change background to pink",
            #"make it responsive",
        ]
    )
