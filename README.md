# zoom-chat-follow
Hacky script to generate clicker-style chart responses from Zoom chat during meetings.

This script was designed to allow in-class participation through the Zoom chat to be reflected on my shared video feed.
My setup is pretty ugly, and involves using OBS Project screen capture of a browser window locally displaying the associated zoomchart.html.

* This Python script tails an auto-saving Zoom chat log, does some basic regex to strip responses to either "A", "B", "C", "D", or "E", and also counts the number of "?".
* The script writes out the number of each vote to a JSON file, as well as a list of the number of "?"s in the previous 10 minutes.
* The associated auto-refreshing **local** webpage reloads this data every couple of seconds, and displays them using chart.js

