from flask import jsonify, request, Flask
import pprint
from polyglot.detect import Detector
import json

pp = pprint.PrettyPrinter(indent=4)

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static'
    )


@app.route('/', methods=['POST'])
def root():

    data = request.json
    return scriptparser(data)

@app.route('/test/')
def test():
    with open("farsi-english-script.json") as file:
        return scriptparser(file.read())

def scriptparser(script):

    data = json.loads(script)

    ret = {}
    ret['script'] = []
    block = {}
    block['meta'] = []
    looking_for_end = False
    for d in data:
        d = d.strip()
        if d != "":
            try:
                lang = Detector(d, quiet=True).languages[0].name.lower()
            except UnknownLanguage:
                lang = "??"

            if is_meta(d):
                type = "meta"
                if looking_for_end:
                    ret['script'].append(block)
                    block = {}
                    block['meta'] = []
                    looking_for_end = False
            else:
                type = lang
                looking_for_end = True

            if type == "meta":
                block['meta'].append(d)
            else:
                if type in block:
                    block[type] += (" " + d)
                else:
                    block[type] = d

    return ret

def is_meta(text):
    if text.isupper():
        return True
    elif text[0:3].isupper() and '“' not in text:
        return True
    else:
        return False


if __name__ == "__main__":
    """
    Main entrypoint

    Launches the flask app when run with "python app.py"

    Args
    - None

    Returns
    - None
    """
    app.run(port=8080)
