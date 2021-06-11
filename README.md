# News Labs Coding Challenge

This repo contains a solution for the challenge set out in the PDF file "News
Labs Coding Exercise 2021.pdf", see that file for a full description of the
challenge.

## Setup

To install the dependancies, run: `pip install -r requirements.txt`

This has been confirmed working using Python 3.7.3 on Debian Buster running on
ChromeOS.

## Running

To launch the web app navigate to the repo root and run: `python app.py`

## API details

The web app provides a single endpoint ("/") that takes a list of strings as
POST data. This data should be a list of strings containing metadata, and script
text in various languages. and example of this is shown below:

```
["OOV:", "Some text", "何か", "OOV:", "more text", "まだまだ"]
```

This data will be processed and returned with each group of script text
collected by language and with accompanying metadata in a list. All languages
detected are returned in a list alongside the script. The above example gives
the following output:

```
{
  "languages": [
    "english",
    "japanese"
  ],
  "script": [
    {
      "english": "Some text",
      "japanese": "\u4f55\u304b",
      "meta":["OOV:"]
    },
    {
      "english": "more text",
      "japanese": "\u307e\u3060\u307e\u3060",
      "meta":["OOV:"]
    }
  ]
}
```

To test the API launch the web app and then run: `curl POST
http://localhost:8080/ -d @test-data.json --header "Content-Type:
application/json"`

The API can also be tested by visiting `http://localhost:8080/test/` in a web
browser. This will load the file `farsi-english-script.json` as if it was passed
as JSON data and render the output in the web browser.
