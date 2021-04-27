#
# An example of how to control the properties of the dropdown list options
# This is the solution of a question I posted on stackoverflow:
# https://stackoverflow.com/questions/66249054/is-there-a-way-to-dynamically-modify-the-properties-e-g-fontsize-color-of-th
#

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.spinner import SpinnerOption
from kivy.properties import ListProperty


Builder.load_string('''
#:import random random

<MySpinnerOption>:
    height: 90
    #font_size: dp(13)

<RootBox>:
    Spinner:
        id: my_spinner
        size_hint: (0.5, 0.25)
        font_size: dp(15)
        color: [1,1,1,1]
        background_color: [1,1,1,1]
        pos_hint: {'center_x': 0.5, 'center_y':0.5}
        values: ['Hi', 'I', 'am', 'your', 'spinner']
        text: 'Please select'
        option_cls: 'MySpinnerOption'

    Button:
        id: color_button
        text: 'Change Color'
        pos_hint: {'center_x':0.5, 'center_y': 0.25}
        size_hint: (0.5, 0.075)
        color: [1,1,1,1]
        on_press: root.color_array = [random.random() for _ in range(3)] + [1]
    Label:
        id: color_label
        text: 'Color: {:.2f},{:.2f},{:.2f}'.format(*root.color_array[:3])
''')


class MySpinnerOption(SpinnerOption):
    my_font_color = [1,1,1,1]  # this is a class attribute, not an instance attribute
    my_font_scale = 2
    def __init__(self, **kwargs):
        #self.height = 90
        #self.font_size = dp(13)
        self.color = self.my_font_color  # use the class attribute for the font color
        self.font_size = dp(self.my_font_scale * 13)
        super(MySpinnerOption, self).__init__(**kwargs)


class RootBox(BoxLayout):
    color_array = ListProperty([0,0,0,0.5])

    def on_color_array(self, *args):
        print(self.color_array)
        #These two work without problem
        self.ids.color_label.color = self.color_array
        self.ids.my_spinner.color = self.color_array

        #This works
        MySpinnerOption.my_font_color = self.color_array  # change the class attribute
        #MySpinnerOption.my_font_scale = self.color_array[0]*10  # change the class attribute

        # trigger rebuild of dropdown by changing option_cls
        self.ids.my_spinner.option_cls = 'SpinnerOption'
        self.ids.my_spinner.option_cls = 'MySpinnerOption'


class TestApp(App):

    def build(self):
        return RootBox()

if __name__ == "__main__":

    TestApp().run()

