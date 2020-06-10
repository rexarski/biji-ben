# CSC318 Assignment 4
Maxwell Huang-Hobbs
g4rbage / 1000675888

## Usage

To run, open 'index.html' in google chrome or some other chromium based browser. Most of it should work with any modern browser, but I didn't go to the trouble of properly prefixing my CSS `\_(ツ)_/¯`.

## About

The main goal behind this ui mockup was to add visual cues to better communicate the 'state' of the shell, while also being minimally invasive. To this end, I added return code 'gems', a simple navigation bar, and a text entry box to report the return codes of commands, current working directory, and user/host in places that can be easily an consistently checked.

The other goal was to play with the metaphor of the 'shell as chat program'. This idea comes from updating the (now defunct) metaphor of the command line shell as an automated teletype printer. While it doesn't necessarily lend itself to curses based shell programs, I believe there's a good chance it will work well with the back and fourth typical to most REPL environments, including CLI shells.
