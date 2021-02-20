#
#  An example test on how to access variables across different classes and widgets
#  at different levels. self.ids does not include widgets that are added dynamically
#  with python, only those defined in the kv files, causing some issues
#  This script includes an example on how to use self.children, self.walk, and also 
#  how to use weakref to modify self.ids
#

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import TwoLineIconListItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.clock import Clock

import weakref


KV = '''
<SwipeToDeleteItem>
    swipe_distance: self.width * 0.4
    size_hint_y: None
    height: content.height
    anchor: 'right'

    MDCardSwipeLayerBox:
        padding: [self.width* 0.85,0,self.width*0.15,0]
        canvas.before:
            Color: 
                rgba:  [1,0.2196,0.1372,0.8]   #Warning red like iOS
            Rectangle:
                pos: self.pos
                size: self.size

        MDIconButton:
            icon: "trash-can"
            size_hint_x: None
            size_hint_y: None
            height: content.height
            pos_hint: {"center_x": 0.9, "center_y": 0.5}

    MDCardSwipeFrontBox:
        elevation: 10

        MyRowListItem:
            text_color: [1,0,0,1]
            secondary_text_color: [1,0,0,1]
            background_normal: ''
            id: content
            text: root.text
            secondary_text: root.secondary_text

            IconLeftWidget:
                pos_hint: {"center_y": 0.5}
                disabled: True
                icon: 'plus'


<OneScreen>
    name: 'mainscreen'
    id: 'mainscreen'

    BoxLayout:
        id: boxlayout
        orientation: "vertical"
        test_text: "This is a class variable at the BoxLayout level"

        MDToolbar:
            id: toolbar
            title: "Level Access Test"
            font_size: dp(50)
            md_bg_color: [0.161, 0.439, 0.796, 1]

            MDIconButton:
                id: iconbutton
                size_hint_x: None
                pos_hint: {"center_x": 1.0, "center_y": 0.5}
                icon: 'plus'
                md_bg_color: [0.125, 0.224, 0.631, 0.5]
                test_text: "This is a class variable at the MDIconButton level"
                padding: 0
                on_press: 
                    root.change_text()

        MDToolbar:
            id: searchbar
            test_text: "This is a class variable at the MDToolbar level"
            elevation: 0
            notch_radius: 0
            title: "Example toolbar"
            md_bg_color: [1, 0, 0, 0.2]

        ScrollView:
            name: 'scrollview'
            id: scrollview
            test_text: "This is a class variable at the scrollview level"

            MDList:
                id: md_list
                test_text: "This is a class variable at the MDList level"
                
                Label:
                    name: 'Swipedefault'
                    id: swipedefault
                    text: 'Default text'
                    test_text: "This is a class variable at the Label level"

<TwoScreen>
    name: 'twoscreen'
    id: twoscreen_id
    test_text: 'This is a class variable at the screen level: TwoScreen'
    BoxLayout:
        Label:
            id: twoscreen_label
            text: 'Blank Screen!'
            test_text: "This is a class variable at the label in another screen"

'''


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty(10)
    secondary_text = StringProperty(10)
    id = StringProperty(10)
    name = StringProperty(10)
    test_text = 'This is a class variable at SwipeToDeleteItem level'

    def __init__(self, **kwargs):
        super(SwipeToDeleteItem, self).__init__(**kwargs)
        print(f'From SwipeToDeleteItem: {self.test_text}')


class MyRowListItem(TwoLineIconListItem):
    pass





class MyScreenManager(ScreenManager):
    menu_screen = ObjectProperty(None)
    test_text = 'This is a class variable at the screen manager level'

class TwoScreen(Screen):
    pass

class OneScreen(Screen):
    test_text = 'This is a class variable at the screen level: OneScreen'

    # Make a quick list
    def on_enter(self):
        pri_text_list = ['Test1', 'Test2', 'Test3']
        second_text_list = ['test', 'test', 'test']
        swipe_id_list = ['swipe1', 'swipe2', 'swipe3']
        name_list = ['Swipe1', 'Swipe2', 'Swipe3']
        for i in range(len(pri_text_list)):
            new_widget =  SwipeToDeleteItem(text=pri_text_list[i], secondary_text=second_text_list[i], id=swipe_id_list[i], name=name_list[i]) #, id=swipe_id_list[i])
            self.ids.md_list.add_widget(new_widget)

            #One can also add it into self.ids (*****)
            #From stackoverflow: https://stackoverflow.com/questions/52151553/how-to-set-kivy-widget-id-from-python-code-file
            self.ids[swipe_id_list[i]] = weakref.ref(new_widget)

        self.test_text_instance = 'This is an instance variable at the screen level: OneScreen'
        Clock.schedule_once(self.accesstesttext)


    def accesstesttext(self, dt):
        app = MDApp.get_running_app()


        #Report start
        print('------ Report ------')

        #Access app level class variable
        print(app.test_text)           

        #Access root level class variable (which in this case is the screen manager)
        print(app.root.test_text)      # Start from the top app level
        print(self.parent.test_text)   # Or start from OneScreen level

        #Access mainscreen level class variable
        print(self.test_text)          # (which is just itself)
        print(app.root.get_screen('mainscreen').test_text)  # Or start from the app level

        #Access mainscreen level instance variable
        print(self.test_text_instance)
        print(app.root.get_screen('mainscreen').test_text_instance)

        #Access children of the mainscreen
        print(self.ids.boxlayout.test_text)    #One level down
        print(app.root.get_screen('mainscreen').ids.boxlayout.test_text)  # Or start from the app level
        print(self.ids.searchbar.test_text)    #Two level down
        print(self.ids.searchbar.ids.label_title.font_name)               # Sub level within the MDToolbar
        print(self.ids.iconbutton.test_text)   #Three level down
        print(self.ids.md_list.test_text)      #Two Level down - MDList

        #Access twoscreen level class variable
        print(self.parent.get_screen('twoscreen').test_text)  # Start from current level
        print(app.root.get_screen('twoscreen').test_text)     # Or start from the app level
        print(self.parent.get_screen('twoscreen').ids.twoscreen_label.test_text)  # One level down in twoscreen

        #Access down the tree using multiple .ids?
        #print(self.ids.md_list.ids.swipedefault.test_text)   # This won't work, since swipe1 will not be in md_list
        print(self.ids.swipedefault.test_text)                # Instead this will work
        #print(self.ids.swipe1.test_text)                     # This won't work, since swipe1 is dynamically added, so it won't be in self.ids
        
        #Access the ids in different levels
        print('IDs:')
        print(self.ids)                     # Note that it has id of all levels under Onescreen, including the swipe_default under md_list
        print(self.ids.toolbar.ids)         # Note that it does not have the iconbutton under toolbar
        print(self.ids.scrollview.ids)      # Note that it has nothing!

        #Access objects down the widget tree using self.children
        #A lot of information here!
        print('Widget Tree:')
        for child in self.children:
            print("First Level:", child)              # One level down - BoxLayout
            print("     Second Level:", child.children)    # Two level down
            for sub_child in child.children:
                # Grab the children of md_list
                if hasattr(sub_child, 'name'):        # Check if it has name attribute
                    if sub_child.name == 'scrollview':
                        #print(sub_child.ids)
                        sub2_child = sub_child.children[0]       #Get the particular children, in this case MD List
                        print(f'     Picked: {sub2_child}')
                        print("          Third Level:", sub2_child.children)
                        for sub3_child in sub2_child.children:
                            if hasattr(sub3_child, 'id'):
                                print(f'          {sub3_child.id}')   # Note that only the dynamically added ones has .id attribute, not the kivy one
                            print(f'          {sub3_child.name}')     # But all of them has name attribute
                            print(f'          {sub3_child.test_text}')               # And the class variable can be accessed
                            print(f'          {sub3_child.text}')

        #Doing similar things using walk()
        print('Walk:')
        for widget in self.walk():
            if hasattr(widget, 'id'):
                print("{} -> {}".format(widget, widget.name))

        #After doing the weakref thing, we can access the swipe items directly
        print(self.ids.swipe1.test_text)
        print(self.ids.swipe2.test_text)
        print(self.ids.swipe3.test_text)



    def change_text(self, *args):
        print('Text Changed!')
        self.ids.swipe1.text = 'Super Change Text1'
        self.ids.swipe1.secondary_text = 'Modified Change Text1'


class TestApp(MDApp):
    test_text = 'This is a class variable at the App level'

    def build(self):
        kvfile = Builder.load_string(KV)
        # Create the screen manager
        # global sm
        sm = MyScreenManager()
        sm.add_widget(OneScreen())
        sm.add_widget(TwoScreen())
        return sm


# Start the App
if __name__ == "__main__":
    TestApp().run()


