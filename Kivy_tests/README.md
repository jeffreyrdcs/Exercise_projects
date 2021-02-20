Kivy tests 
=========================================

This directory contains various tests that I did to explore some of the Kivy behaviour / issues. Useful snippets are also kept here.

kivy_display_text_test.py:
- I encountered an issue that once you drag the app across multiple display, the app font size will increase relative to the screen size when I move the window from my internal retina display to an external one.
I end up trying to use on_resize to let kivy detect which monitor the screen is in and rescale the text according to that. This is a snippet of that. Would be nice to know if there is a better fix. 
