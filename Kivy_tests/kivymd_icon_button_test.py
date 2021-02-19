#
#  A simple test on how MDIconButton works
#  It has some preset on the icon, button size, and padding
#  which was causing some weird behaviour
#

from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder


Builder.load_string('''
#:import random random

<MySpinnerOption>:
    height: 90
    #font_size: dp(13)

<RootBox>
    MDIconButton:
        icon: 'plus-circle'
        pos_hint: {"center_x": 0.1, "center_y": 0.1}
        theme_text_color: "Custom"
        text_color: [0, 0, 0, 1]

    MDIconButton:
        icon: 'plus-circle'
        pos_hint: {"center_x": 0.25, "center_y": 0.1}
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        md_bg_color: [0.125, 0.224, 0.631, 0.5]

    MDIconButton:
        icon: 'plus-circle'
        pos_hint: {"center_x": 0.4, "center_y": 0.1}
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        user_font_size: dp(40)
        md_bg_color: [0.125, 0.224, 0.631, 0.6]

    MDIconButton:
        icon: 'plus-circle'
        pos_hint: {"center_x": 0.55, "center_y": 0.1}
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        user_font_size: dp(40)
        size: dp(60), dp(60)
        md_bg_color: [0.125, 0.224, 0.631, 0.7]

    MDIconButton:
        icon: 'plus-circle'
        pos_hint: {"center_x": 0.7, "center_y": 0.1}
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        user_font_size: dp(40)
        size: dp(50), dp(50)
        md_bg_color: [0.125, 0.224, 0.631, 0.8]          # There is a x-cutoff?

    MDIconButton:
        icon: 'plus-circle'
        pos_hint: {"center_x": 0.85, "center_y": 0.1}
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        user_font_size: dp(40)
        size: dp(35), dp(35)
        md_bg_color: [0.125, 0.224, 0.631, 0.9]
        padding:0                                        # It is the padding ...

    Label:
        pos_hint: {"center_x": 0.5, "center_y": 0.95}
        text: 'Weird MDIcons Behaviour'
        color: [0,0,0,1]
        font_size: dp(30)
''')


class RootBox(RelativeLayout):
    pass

class TestApp(MDApp):

    def build(self):
        return RootBox()

if __name__ == "__main__":

    TestApp().run()