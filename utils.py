import json
import os

import pyttsx3
from bs4 import BeautifulSoup

from css_edits import *
from recognise import mic
from writer import Writer

# META RULES
# 1) Functions follow the signature: function(speech, command, data)

cache_dir = "templates/snippets/"
tts = pyttsx3.init()
tts.setProperty("rate", 125)


def speak(text):
    tts.say(text)
    tts.runAndWait()


# tag mapper
with open("map_tags.json", "r") as f:
    tag_mapper = json.load(f)


def getitem(speech, command, data):
    parse_count = 0
    istag = 1
    tag = None

    # default tags
    for item in tag_mapper:
        if item in speech:
            parse_count = speech.find(item)
            tag = data.new_tag(tag_mapper[item])
            break
    else:
        # snippets
        items = os.listdir(cache_dir)
        for item in items:
            word = item.split(".")[0]
            if word in speech:
                parse_count = speech.find(word)
                with open(cache_dir + item, "r") as f:
                    tag = BeautifulSoup(f.read(), features="html.parser")
                    istag = 0
                break

    if not tag:
        speak("Invalid command")
        return data

    # Strip unecessary words
    speech = speech[parse_count:].split()

    # If default tag eg: make heading with class bootstrap-heading and content somethign something
    if istag:
        check_content = speech.index("content")
        tag.string = speech[check_content + 1]
        check_class = speech.index("class")
        class_ = speech[check_class + 2]
        tag["class"] = class_

    # Add tag to body
    data.body.append(tag)
    savefile(data)
    speak("Sucessfully added to the html")
    return data


def add_asset(speech, command, data):
    items = os.listdir("assets/")
    speak("Paste your assets into the assets folder and speak out the file name")
    for i in range(3):
        response = mic.recognize_speech()
        if response["success"]:
            result = response["transcription"]
            print("you said", result)
            for img in items:
                if img.startswith("test"):
                    tag = data.new_tag("img", src=f"assets/{img}", height="10%", width="10%")
                    data.append(tag)
                    if data:
                        data.body.append(tag)
                        savefile(data)
                    return
        else:
            print("Retry...")


def moveitem(speech, command, data):
    # if "centre" in speech or "center" in speech: (title hardcoded)
    data = center()
    savecss(data)


def bg(speech, command, data):
    try:
        speech = speech.split()
        check_color = speech.index(command)
        savecss(background_css(speech[check_color + 2]))
        speak(f"Changed background to {speech[check_color + 2]}")
    except ValueError:
        pass


def db_make(speech, command, data):
    with open("templates/base.php", "r") as f:
        with open("main.php", "w") as fp:
            fp.write(f.read())


def savefile(data):
    Writer().write_html(str(data))


def savecss(data):
    Writer().write_css(str(data))


def resp(speech, command, data):
    wrapper = data.new_tag("div", **{"class": "container"})
    body_children = list(data.body.children)[1:]  # NAVBAR AA
    data.body.clear()
    data.body.append(wrapper)
    for child in body_children:
        wrapper.append(child)
    savefile(data)
    speak("You webapp is responsive now")
