# screens/base_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

class BaseScreen(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.build_ui()
    
    def build_ui(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.add_widget(self.main_layout)
        
        # Header
        self.header = BoxLayout(size_hint_y=None, height=dp(50))
        self.main_layout.add_widget(self.header)
        
        # Scrollable content
        self.scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scroll.add_widget(self.content)
        self.main_layout.add_widget(self.scroll)
    
    def show_message(self, title, message):
        from widgets.popup_widgets import MessagePopup
        popup = MessagePopup(title=title, message=message)
        popup.open()
    
    def confirm_action(self, title, message, callback):
        from widgets.popup_widgets import ConfirmPopup
        popup = ConfirmPopup(title=title, message=message, on_confirm=callback)
        popup.open()