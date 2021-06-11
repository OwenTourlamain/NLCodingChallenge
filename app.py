from flask import jsonify, request, Flask
from polyglot.detect import Detector
import json


app = Flask(__name__)


@app.route('/', methods=['POST'])
def root():
    """
    Grabs a list of strings from a POST request and passes them to scriptparser,
    returning the result. Flask automatically converts the dict into JSON.

    Args
    - data (list of string) - list of strings to process - POST

    Returns
    - dict as JSON
    """

    data = request.json
    return scriptparser(data)


@app.route('/test/')
def test():
    """
    Simulates the root function by reading from a local file instead of POST
    data. This allows the endpoint to be tested using a web browser easily.
    Flask automatically converts the dict into JSON.

    Args
    - None

    Returns
    - dict as JSON
    """
    with open("farsi-english-script.json") as file:
        data = json.loads(file.read())
        return scriptparser(data)


def scriptparser(data):
    """
    Parses a given list of strings into a dict that collects text with its
    metadata and translated text. This relies on the strings being in the order:
    metadata, text. Each of these can be repeated as many times as needed
    andempty strings are removed.

    First lines are analysed to see what language they are or if they are
    metadata. These are added to a temporary dict until the next metadata line
    is reached. At this point the temporary dict is copied to a return dict and
    the pattern is repeated.

    Args
    - data (list of string) - list of strings to process

    Returns
    - dict
    """

    # init retrun dict
    ret = {}
    ret['script'] = []
    lang_set = set()

    # this will store blocks before they are added to the return dict
    block = {}
    block['meta'] = []

    # flag to see if we are past the first lines of meta data
    looking_for_end = False

    # loop through the strings
    for d in data:

        # remove any whitespace, some strings only contain a single space which
        # confuses the language detection
        d = d.strip()

        # skip empty strings
        if d != "":

            # try to detect the language, the quiet flag surpresses an exception
            # when the language can't be detected
            lang = Detector(d, quiet=True).languages[0].name.lower()

            # check if this string is metadata
            if is_meta(d):

                # mark the string as metadata
                type = "meta"

                # flag is set when we have passed the first set of metadata
                # strings, if we see metadata after this point we must have
                # reached the next block
                if looking_for_end:

                    # add the block to the return dict and reset it
                    ret['script'].append(block)
                    block = {}
                    block['meta'] = []
                    looking_for_end = False
            else:
                type = lang

                # add the language to the set of languages
                lang_set.add(lang)

                # we have passed the metadata lines at the start of this block,
                # so set the flag.
                looking_for_end = True

            # add the string to the right part of the dict, metadata goes into a
            # list, text strings get merged and stored using thier language as a
            # key
            if type == "meta":
                block['meta'].append(d)
            else:

                # if this is the first time we've encountered a language we have
                # to add it to the dict, otherwise we merge the string with the
                # existing data
                if type in block:
                    block[type] += (" " + d)
                else:
                    block[type] = d

    # add the last set of data to the return dict
    ret['script'].append(block)

    # add the lang set to the ret dict, needs to be cast to a list so JSON can
    # read it
    ret['languages'] = list(lang_set)
    return ret


def is_meta(text):
    """
    Detects if the passed text is metadata.

    First it checks if all the characters in the string are uppercase, if not it
    also checks if the first three characters are uppercase and there are no
    quotation marks in the string.

    Args
    - text (string) - the text to check

    Returns
    - bool
    """
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
