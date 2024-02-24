# IISc open day 2024 - Databased rock paper scissors

This is a simple python program that levarages [mediapipe](https://developers.google.com/mediapipe) in order to detect hands and play rock paper scissors against the computer picking randomly

## Instructions
- This program requires mediapipe, opencv-python and keyboard installed
```
pip install opencv-python mediapipe keyboard
```
- Press `esc` to switch to out of game mode, here up to four hands are detected at once
- Press `enter` to switch into game mode
  - Here, there are 5 rounds. Show your hand when the text "Ready" appears.
  - A score above 8 is counted as a win (you receive 3 for a win and 1 for a draw)
  - Hold your hand upright for best results
