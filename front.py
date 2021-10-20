import threading
import time

from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.codeinput import CodeInput
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDToolbar
from kivy.clock import Clock


class TopBar(MDToolbar):
    def back(self):
        self.parent.parent.parent.current = "main_scr"

class BottomBar(MDToolbar):

    def record(self):
        if self.icon == "arrow-right":
            self.icon = "microphone"
        else:
            self.icon = "arrow-right"
               
    
        
class Card(MDCard):
    title = StringProperty()
    description = StringProperty("Not found")

    def __init__(self, title, description, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.title = title
        self.description = description

    def on_release(self):
        self.parent.parent.parent.parent.current = "work_scr"


class MainGrid(ScrollView):
    grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.grid.add_widget(Card(title="Untitled", description="This is a test project"))
        self.grid.add_widget(Card(title="New Project", description="Hmmm"))
        self.grid.add_widget(
            Card(
                title="Test project",
                description="Nice grid?",
            )
        )


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.add_widget(TopBar())
        self.add_widget(MainGrid())
       

class WorkFlowScreen(Screen):
    pass


class frontApp(MDApp):
    def build(self):
        screen_mgr = ScreenManager()

        screen_mgr.add_widget(MainScreen())
        screen_mgr.add_widget(WorkFlowScreen())

        #screen_mgr.current = "main_screen"
        return screen_mgr
        #return MainGrid()

    def theme_switch(self):
        if self.theme_cls.theme_style != "Dark":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


frontApp().run()
