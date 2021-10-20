import tinycss

with open("main.css", "r") as f:
    css_text = f.read()
parser = tinycss.make_parser("page3")
stylesheet = parser.parse_stylesheet_bytes(css_text.encode("utf-8"))
print(stylesheet)
