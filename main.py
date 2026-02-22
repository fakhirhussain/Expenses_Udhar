# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.metrics import dp

from database import Database
from screens.expense_screen import ExpenseScreen
from screens.udhar_screen import UdharScreen
from screens.report_screen import ReportScreen

# Mobile-friendly configuration
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

Window.clearcolor = (0.95, 0.95, 0.95, 1)

class UdharExpenseApp(App):
    def build(self):
        self.db = Database()
        
        # Create screen manager
        sm = ScreenManager(transition=SlideTransition())
        
        # Add screens
        sm.add_widget(ExpenseScreen(db=self.db, name='expenses'))
        sm.add_widget(UdharScreen(db=self.db, name='udhar'))
        sm.add_widget(ReportScreen(db=self.db, name='reports'))
        
        # Bottom navigation
        root = BoxLayout(orientation='vertical')
        root.add_widget(sm)
        
        # Navigation bar
        nav = BoxLayout(
            size_hint_y=None, 
            height=dp(60),
            padding=dp(5),
            spacing=dp(5)
        )
        
        nav.add_widget(self.create_nav_btn('💳', 'Expenses', sm, 'expenses'))
        nav.add_widget(self.create_nav_btn('🤝', 'Udhar', sm, 'udhar'))
        nav.add_widget(self.create_nav_btn('📊', 'Reports', sm, 'reports'))
        
        root.add_widget(nav)
        
        return root
    
    def create_nav_btn(self, icon, text, sm, screen_name):
        from kivy.uix.button import Button
        btn = Button(
            text=f'{icon}\n{text}',
            font_size='12sp',
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            on_press=lambda x: setattr(sm, 'current', screen_name)
        )
        return btn

if __name__ == '__main__':
    UdharExpenseApp().run()