# widgets/popup_widgets.py
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

class ConfirmPopup(Popup):
    def __init__(self, title, message, on_confirm, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        layout.add_widget(Label(text=message, text_size=(None, None), halign='center'))
        
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        cancel_btn = Button(text='Cancel', on_press=self.dismiss)
        confirm_btn = Button(text='Confirm', background_color=(0.9, 0.2, 0.2, 1))
        confirm_btn.bind(on_press=lambda x: self.confirm(on_confirm))
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(confirm_btn)
        layout.add_widget(btn_layout)
        
        self.content = layout
    
    def confirm(self, callback):
        callback()
        self.dismiss()

class InputPopup(Popup):
    def __init__(self, title, hint_text, on_submit, input_type='text', **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        self.input_field = TextInput(
            hint_text=hint_text,
            multiline=False,
            input_type=input_type,
            size_hint_y=None,
            height=dp(45)
        )
        layout.add_widget(self.input_field)
        
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        cancel_btn = Button(text='Cancel', on_press=self.dismiss)
        submit_btn = Button(text='Submit', background_color=(0.2, 0.6, 0.9, 1))
        submit_btn.bind(on_press=lambda x: self.submit(on_submit))
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(submit_btn)
        layout.add_widget(btn_layout)
        
        self.content = layout
    
    def submit(self, callback):
        value = self.input_field.text
        if value:
            callback(value)
            self.dismiss()

class MessagePopup(Popup):
    def __init__(self, title, message, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.8, 0.35)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        layout.add_widget(Label(text=message, text_size=(None, None), halign='center'))
        
        ok_btn = Button(text='OK', size_hint_y=None, height=dp(50), on_press=self.dismiss)
        layout.add_widget(ok_btn)
        
        self.content = layout