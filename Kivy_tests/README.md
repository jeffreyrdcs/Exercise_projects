Kivy tests and snippets 
=========================================

This directory contains various tests that I did to explore some of the Kivy behaviour / issues. Useful snippets are also kept here.

kivy_display_text_test.py:
- I encountered an issue that once you drag the app across multiple display, the app font size will increase relative to the screen size when I move the window from the internal retina display of my mac to an external display. See Kivy_retina_display.png and Kivy_external_display.png for a screenshot illustrating the issue.
- I ended up trying to use on_resize to detect which monitor the screen is in and rescale the text according to that. This snippet is an example of that. It would be nice to know if there is a better fix.

kivymd_icon_button_test.py:
- I encountered an issue that the icon in MDIconButton was not being displayed correctly. The icon was cropped left and right when the button itself is small. This is a simple test on how different setup changes the apperance of the MDIconButton class.
- The issue was that there are some presets on the icon size, button size, and padding on the button class, resulting in the behaviour.

kivy_var_access_test.py:
- This is an example test on how to access variables across different classes and widgets at different levels. 
- I encountered some issues because self.ids does not include widgets that are added dynamically with python. Only those defined in the kv files are included.
- This test includes an example on how to use self.children, self.walk, and also how to use weakref to modify self.ids.

kivy_click_drag_test.py:
- This is a snippet showing how to distinguish between a click and a drag (or a swipe) on a label

