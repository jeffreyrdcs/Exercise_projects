#
#  A simple test showing how to distinugish between click and drag on a label
#

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder


Builder.load_string('''
<RootBox>
    canvas.before:
        # Background color
        Color:
            rgba: [1,1,1,1]
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        pos_hint: {"center_x": 0.5, "center_y": 0.95}
        text: 'Distinguishing between click or drag'
        color: [0,0,0,1]
        font_size: dp(30)

    Label:
        size_hint: (0.6, 0.2)
        pos_hint: {"center_x": 0.5, "center_y": 0.75}
        text: root.display_text
        color: [0,0,0,1]
        font_size: dp(25)

    ClickLabel:
        name: 'Label1'
        size_hint: (0.6, 0.175)    
        pos_hint: {"center_x": 0.5, "center_y": 0.35}
        text: 'Label1: Click me or Drag me!'
        color: [0,0,0,1]
        font_size: dp(21)
        canvas.before:
            Color:
                rgba: self.highlight_color
            Rectangle:
                pos: self.pos
                size: self.size

    ClickLabel:
        name: 'Label2'
        size_hint: (0.6, 0.175)    
        pos_hint: {"center_x": 0.5, "center_y": 0.15}
        text: 'Label2: Click me or Drag me!'
        color: [0,0,0,1]
        font_size: dp(21)
        canvas.before:
            Color:
                rgba: self.highlight_color
            Rectangle:
                pos: self.pos
                size: self.size

''')


class ClickLabel(Label):        # Not using a button since it will be easier to demonstrate
    mouse_dpos = [0,0]
    drag_threshold = 60         # pixel
    is_touch_down = False
    activate_item_down = ''
    activate_item_up = ''
    highlight_color = ListProperty([0.5,0.75,0.5,0.5])

    def on_touch_down(self, touch):
        '''
            Function together with touch_up
            Distinugish between drag and click
        '''
        self.mouse_dpos = [touch.x, touch.y]

        if self.collide_point(*touch.pos):
            self.is_touch_down = True
            self.activate_item_down = self.text

            # Change color on press
            self.highlight_color = [0,0,0,0.06]
            return True

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        '''
            Function together with touch_down
            Distinugish between scrolling, drag and clicks
        '''
        # Change back to default color
        self.highlight_color = [0.5,0.75,0.5,0.6]

        # if self.is_touch_down == False and self.collide_point(*touch.pos):
        #     print(' Scrolling?')
        #     return super().on_touch_up(touch)
        if self.is_touch_down == True and self.collide_point(*touch.pos):
            self.activate_item_up = self.text

            if abs(touch.x - self.mouse_dpos[0]) > self.drag_threshold or abs(touch.y - self.mouse_dpos[1]) > self.drag_threshold:
                # Dragging
                self.is_touch_down = False                
                print(f' Drag: {touch.x} , {self.mouse_dpos[0]}')
                self.parent.display_text = 'Dragged '+self.name
                return super().on_touch_up(touch)

            elif self.activate_item_up == self.activate_item_down:
                # Clicking
                self.is_touch_down = False
                print(f' Click: {touch.x} , {self.mouse_dpos[0]}')
                self.parent.display_text = 'Clicked '+self.name
                return super().on_touch_up(touch)


class RootBox(RelativeLayout):
    display_text = StringProperty("Waiting for Input ...")

class TestApp(App):

    def build(self):
        return RootBox()

if __name__ == "__main__":

    TestApp().run()



