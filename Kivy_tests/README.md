Kivy tests and snippets 
=========================================

This directory contains various tests that I did to explore some of the Kivy behaviour/issues. Useful snippets are also kept here.

kivy_display_text_test.py:
- I encountered an issue that once I drag the app across multiple displays, the app font size will change according to the resolution of the new screen. For example, when I move the app window from the internal retina display of my macbook to an external display (1920 x 1080), the text on the app will double in size. See Kivy_retina_display.png and Kivy_external_display.png for a screenshot illustrating the issue.
- This snippet is an example of using on_resize to detect which monitor the screen is in and rescale the text accordingly.  - I mentioned this issue in one of the tickets: https://github.com/kivy/kivy/issues/6785. This seems to be patched in #7293. But the fix does not work well with other libraries e.g. the KivyMD components. It would be nice to know if there is another fix.

kivymd_icon_button_test.py:
- I encountered an issue that the icon in MDIconButton was not displayed correctly. The icon was cropped left and right when the button itself is small. This is a simple test on how different setup changes the appearance of the MDIconButton class.
- The issue was that there are some presets on the icon size, button size, and padding on the button class, resulting in the behavior.

kivy_var_access_test.py:
- This is an example test on how to access variables across different classes and widgets at different levels. 
- I encountered some issues because self.ids do not include widgets that are added dynamically with python. Only those defined in the kv files are included.
- This test includes an example of how to use self.children, self.walk, and also how to use weakref to modify the self.ids.

kivy_click_drag_test.py:
- This is a snippet showing how to distinguish between a click, drag (or swipe) on a label, and mouse scrolling.

kivy_dropdown_properties_update.py:
- This is the solution of a question I posted on stackoverflow about how to update the dropdown list properties. The key is to trigger rebuild of dropdown by changing option_cls.


