import os
from bs4 import BeautifulSoup


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Writer(metaclass=Singleton):
    def __init__(self):
        self.path = "./output"
        self.html_path = self.path + "/index.html"
        self.css_path = self.path + "/main.css"

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def loadfile(self):
        if os.path.exists(self.html_path):
            with open(self.html_path) as f:
                data = BeautifulSoup(f.read(), features="html.parser")
        else:
            with open("templates/base.html", "r") as f:
                data = BeautifulSoup(f.read(), features="html.parser")

            with open("templates/main.js", "r") as f:
                js_data = f.read()

            with open(self.path + "/main.js", "w+") as f:
                f.write(js_data)

            self.write_html(str(data))
            self.write_css("")

        return data

    def read_html(self):
        with open(self.html_path, "r") as f:
            return f.read()

    def write_html(self, html_content):
        with open(self.html_path, "w+") as f:
            f.write(str(html_content))

    def read_css(self):
        with open(self.css_path, "r") as f:
            return f.read()

    def write_css(self, css_content):
        with open(self.css_path, "a+") as f:
            f.write(css_content)
