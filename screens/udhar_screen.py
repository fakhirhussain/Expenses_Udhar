# screens/udhar_screen.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock

from screens.base_screen import BaseScreen
from widgets.custom_widgets import (
    Card, PrimaryButton, SecondaryButton, 
    CustomTextInput, StatusBadge
)
from models import Udhar, UdharStatus
from utils import get_current_date, validate_amount, format_currency

class UdharScreen(BaseScreen):
    def build_ui(self):
        super().build_ui()
        
        # Header
        self.header.add_widget(Label(
            text='🤝 Udhar (Credit)',
            font_size='20sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        ))
        
        # Input Form
        form_card = Card(bg_color=(0.98, 0.98, 0.98, 1))
        form_card.height = dp(300)
        
        # Person Name
        name_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        name_layout.add_widget(Label(text='Name:', size_hint_x=None, width=dp(80)))
        self.name_input = CustomTextInput(hint_text='Person name', size_hint_x=0.7)
        name_layout.add_widget(self.name_input)
        form_card.add_widget(name_layout)
        
        # Amount
        amt_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        amt_layout.add_widget(Label(text='Amount:', size_hint_x=None, width=dp(80)))
        self.amount_input = CustomTextInput(
            hint_text='Amount lent',
            input_filter='float',
            size_hint_x=0.7
        )
        amt_layout.add_widget(self.amount_input)
        form_card.add_widget(amt_layout)
        
        # Dates
        dates_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        dates_layout.add_widget(Label(text='Given:', size_hint_x=None, width=dp(80)))
        self.date_input = CustomTextInput(
            text=get_current_date(),
            size_hint_x=0.3
        )
        dates_layout.add_widget(self.date_input)
        dates_layout.add_widget(Label(text='Due:', size_hint_x=None, width=dp(50)))
        self.due_input = CustomTextInput(
            hint_text='YYYY-MM-DD',
            size_hint_x=0.3
        )
        dates_layout.add_widget(self.due_input)
        form_card.add_widget(dates_layout)
        
        # Description
        desc_layout = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        desc_layout.add_widget(Label(text='Note:', size_hint_x=None, width=dp(80)))
        self.desc_input = CustomTextInput(
            hint_text='Description',
            size_hint_x=0.7
        )
        desc_layout.add_widget(self.desc_input)
        form_card.add_widget(desc_layout)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        add_btn = PrimaryButton(text='Add Udhar')
        add_btn.bind(on_press=self.add_udhar)
        clear_btn = SecondaryButton(text='Clear')
        clear_btn.bind(on_press=self.clear_form)
        
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(clear_btn)
        form_card.add_widget(btn_layout)
        
        self.content.add_widget(form_card)
        
        # Summary Card
        self.summary_card = Card(bg_color=(1, 0.95, 0.9, 1))
        self.summary_card.height = dp(60)
        self.summary_label = Label(
            text='Total Pending: ₹0.00',
            font_size='16sp',
            bold=True,
            color=(0.9, 0.3, 0.1, 1)
        )
        self.summary_card.add_widget(self.summary_label)
        self.content.add_widget(self.summary_card)
        
        # Udhar List
        list_card = Card(bg_color=(1, 1, 1, 1))
        list_card.height = dp(400)
        list_card.add_widget(Label(
            text='Active Udhar Records',
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))
        
        self.udhar_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.udhar_layout.bind(minimum_height=self.udhar_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.udhar_layout)
        list_card.add_widget(scroll)
        
        self.content.add_widget(list_card)
        
        Clock.schedule_once(lambda dt: self.load_data(), 0)
    
    def add_udhar(self, instance):
        name = self.name_input.text.strip()
        if not name:
            self.show_message('Error', 'Please enter person name')
            return
        
        valid, amount = validate_amount(self.amount_input.text)
        if not valid:
            self.show_message('Error', 'Please enter valid amount')
            return
        
        udhar = Udhar(
            id=None,
            person_name=name,
            amount=amount,
            description=self.desc_input.text,
            date_given=self.date_input.text,
            due_date=self.due_input.text or None,
            status=UdharStatus.PENDING
        )
        
        self.db.add_udhar(udhar)
        self.show_message('Success', f'Udhar added for {name}')
        self.clear_form()
        self.load_data()
    
    def clear_form(self, instance=None):
        self.name_input.text = ''
        self.amount_input.text = ''
        self.desc_input.text = ''
        self.due_input.text = ''
        self.date_input.text = get_current_date()
    
    def load_data(self):
        self.udhar_layout.clear_widgets()
        
        udhar_list = self.db.get_udhar_list()
        total_pending = 0
        
        for udhar in udhar_list:
            udhar_id, person, amount, desc, date_given, due_date, status, paid, created = udhar
            remaining = amount - paid
            
            if status in ['pending', 'partial']:
                total_pending += remaining
            
            # Udhar Card
            card = Card(bg_color=(0.98, 0.98, 0.98, 1), radius=[dp(8)])
            card.height = dp(120)
            
            # Header with name and status
            header = BoxLayout(size_hint_y=None, height=dp(35))
            header.add_widget(Label(
                text=person,
                font_size='16sp',
                bold=True,
                halign='left',
                color=(0.2, 0.2, 0.2, 1)
            ))
            
            status_colors = {
                'pending': (0.9, 0.2, 0.2, 1),
                'partial': (0.9, 0.6, 0.1, 1),
                'cleared': (0.2, 0.7, 0.2, 1)
            }
            status_label = Label(
                text=status.upper(),
                font_size='12sp',
                bold=True,
                color=status_colors.get(status, (0.5, 0.5, 0.5, 1)),
                size_hint_x=None,
                width=dp(80)
            )
            header.add_widget(status_label)
            card.add_widget(header)
            
            # Amount details
            amounts = BoxLayout(size_hint_y=None, height=dp(30))
            amounts.add_widget(Label(
                text=f'Total: {format_currency(amount)}',
                font_size='13sp',
                color=(0.4, 0.4, 0.4, 1)
            ))
            amounts.add_widget(Label(
                text=f'Paid: {format_currency(paid)}',
                font_size='13sp',
                color=(0.2, 0.6, 0.2, 1)
            ))
            amounts.add_widget(Label(
                text=f'Due: {format_currency(remaining)}',
                font_size='13sp',
                bold=True,
                color=(0.9, 0.2, 0.2, 1)
            ))
            card.add_widget(amounts)
            
            # Date info
            info = BoxLayout(size_hint_y=None, height=dp(25))
            date_text = f'Given: {date_given}'
            if due_date:
                date_text += f' | Due: {due_date}'
            info.add_widget(Label(
                text=date_text,
                font_size='11sp',
                color=(0.5, 0.5, 0.5, 1),
                halign='left'
            ))
            card.add_widget(info)
            
            # Action buttons
            if status != 'cleared':
                actions = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
                
                pay_btn = SecondaryButton(
                    text='Record Payment',
                    size_hint_x=0.5
                )
                pay_btn.bind(on_press=lambda x, id=udhar_id, rem=remaining: 
                           self.show_payment_popup(id, rem))
                
                full_btn = PrimaryButton(
                    text='Mark Cleared',
                    size_hint_x=0.5
                )
                full_btn.bind(on_press=lambda x, id=udhar_id, rem=remaining: 
                            self.mark_cleared(id, rem))
                
                actions.add_widget(pay_btn)
                actions.add_widget(full_btn)
                card.add_widget(actions)
            
            # Long press to delete
            card.bind(on_touch_down=lambda touch, id=udhar_id: 
                     self.on_card_touch(touch, id))
            
            self.udhar_layout.add_widget(card)
        
        self.summary_label.text = f'Total Pending: {format_currency(total_pending)}'
    
    def show_payment_popup(self, udhar_id, remaining):
        from widgets.popup_widgets import InputPopup
        popup = InputPopup(
            title='Record Payment',
            hint_text=f'Amount (max {format_currency(remaining)})',
            input_type='number',
            on_submit=lambda val: self.record_payment(udhar_id, float(val), remaining)
        )
        popup.open()
    
    def record_payment(self, udhar_id, amount, max_amount):
        if amount <= 0 or amount > max_amount:
            self.show_message('Error', 'Invalid amount')
            return
        self.db.update_udhar_payment(udhar_id, amount)
        self.load_data()
    
    def mark_cleared(self, udhar_id, remaining):
        self.confirm_action(
            'Confirm',
            f'Mark as fully paid? Remaining: {format_currency(remaining)}',
            lambda: self.clear_udhar(udhar_id, remaining)
        )
    
    def clear_udhar(self, udhar_id, remaining):
        self.db.update_udhar_payment(udhar_id, remaining)
        self.load_data()
    
    def on_card_touch(self, touch, udhar_id):
        if touch.is_double_tap:
            self.confirm_action(
                'Delete',
                'Delete this udhar record?',
                lambda: self.delete_udhar(udhar_id)
            )
    
    def delete_udhar(self, udhar_id):
        self.db.delete_udhar(udhar_id)
        self.load_data()