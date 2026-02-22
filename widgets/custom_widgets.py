# widgets/custom_widgets.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.metrics import dp

class Card(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])
    radius = ListProperty([dp(10)])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

class StatusBadge(Label):
    status = StringProperty('pending')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(80), dp(30))
        self.bind(status=self.update_color)
        
    def update_color(self, *args):
        colors = {
            'pending': (0.9, 0.2, 0.2, 1),
            'partial': (0.9, 0.6, 0.1, 1),
            'cleared': (0.2, 0.7, 0.2, 1)
        }
        self.color = colors.get(self.status, (0.5, 0.5, 0.5, 1))

class AmountLabel(Label):
    amount = NumericProperty(0)
    is_positive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(amount=self.update_text)
        self.bold = True
        self.font_size = '16sp'
        
    def update_text(self, *args):
        from utils import format_currency
        self.text = format_currency(self.amount)
        self.color = (0.2, 0.7, 0.2, 1) if self.is_positive else (0.9, 0.2, 0.2, 1)

class PrimaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.2, 0.6, 0.9, 1)
        self.background_normal = ''
        self.color = (1, 1, 1, 1)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(50)

class SecondaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.9, 0.9, 0.9, 1)
        self.background_normal = ''
        self.color = (0.2, 0.2, 0.2, 1)
        self.size_hint_y = None
        self.height = dp(45)

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.size_hint_y = None
        self.height = dp(45)
        self.padding = [dp(10), dp(10)]
        self.background_color = (0.95, 0.95, 0.95, 1)

class CustomSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(45)
        self.background_color = (0.95, 0.95, 0.95, 1)