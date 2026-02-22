# screens/expense_screen.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock

from screens.base_screen import BaseScreen
from widgets.custom_widgets import (
    Card, PrimaryButton, SecondaryButton, 
    CustomTextInput, CustomSpinner, AmountLabel
)
from models import Expense, TransactionType
from utils import (
    get_current_date, validate_amount, 
    get_category_suggestions, format_currency, get_status_color
)

class ExpenseScreen(BaseScreen):
    def build_ui(self):
        super().build_ui()
        
        # Header
        self.header.add_widget(Label(
            text='💳 Expenses',
            font_size='20sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        ))
        
        # Input Form
        form_card = Card(bg_color=(0.98, 0.98, 0.98, 1))
        form_card.height = dp(350)
        
        # Type Selection
        type_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        type_layout.add_widget(Label(text='Type:', size_hint_x=None, width=dp(80)))
        self.type_spinner = CustomSpinner(
            text='expense',
            values=['expense', 'income'],
            size_hint_x=0.7
        )
        type_layout.add_widget(self.type_spinner)
        form_card.add_widget(type_layout)
        
        # Amount
        amount_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        amount_layout.add_widget(Label(text='Amount:', size_hint_x=None, width=dp(80)))
        self.amount_input = CustomTextInput(
            hint_text='Enter amount',
            input_filter='float',
            size_hint_x=0.7
        )
        amount_layout.add_widget(self.amount_input)
        form_card.add_widget(amount_layout)
        
        # Category
        cat_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        cat_layout.add_widget(Label(text='Category:', size_hint_x=None, width=dp(80)))
        self.category_spinner = CustomSpinner(
            text='Select category',
            values=get_category_suggestions(),
            size_hint_x=0.7
        )
        cat_layout.add_widget(self.category_spinner)
        form_card.add_widget(cat_layout)
        
        # Date
        date_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        date_layout.add_widget(Label(text='Date:', size_hint_x=None, width=dp(80)))
        self.date_input = CustomTextInput(
            text=get_current_date(),
            size_hint_x=0.7
        )
        date_layout.add_widget(self.date_input)
        form_card.add_widget(date_layout)
        
        # Description
        desc_layout = BoxLayout(size_hint_y=None, height=dp(80), spacing=dp(10))
        desc_layout.add_widget(Label(text='Note:', size_hint_x=None, width=dp(80), valign='top'))
        self.desc_input = CustomTextInput(
            hint_text='Description (optional)',
            multiline=True,
            size_hint_x=0.7
        )
        desc_layout.add_widget(self.desc_input)
        form_card.add_widget(desc_layout)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        add_btn = PrimaryButton(text='Add Transaction')
        add_btn.bind(on_press=self.add_transaction)
        clear_btn = SecondaryButton(text='Clear')
        clear_btn.bind(on_press=self.clear_form)
        
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(clear_btn)
        form_card.add_widget(btn_layout)
        
        self.content.add_widget(form_card)
        
        # Summary Card
        self.summary_card = Card(bg_color=(0.9, 0.95, 1, 1))
        self.summary_card.height = dp(80)
        self.summary_label = Label(
            text='Income: ₹0.00 | Expense: ₹0.00',
            font_size='14sp',
            bold=True
        )
        self.summary_card.add_widget(self.summary_label)
        self.content.add_widget(self.summary_card)
        
        # Transactions List
        list_card = Card(bg_color=(1, 1, 1, 1))
        list_card.height = dp(400)
        list_card.add_widget(Label(
            text='Recent Transactions',
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))
        
        self.transactions_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.transactions_layout.bind(minimum_height=self.transactions_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.transactions_layout)
        list_card.add_widget(scroll)
        
        self.content.add_widget(list_card)
        
        # Load data
        Clock.schedule_once(lambda dt: self.load_data(), 0)
    
    def add_transaction(self, instance):
        valid, amount = validate_amount(self.amount_input.text)
        if not valid:
            self.show_message('Error', 'Please enter a valid amount')
            return
        
        category = self.category_spinner.text
        if category == 'Select category':
            self.show_message('Error', 'Please select a category')
            return
        
        expense = Expense(
            id=None,
            amount=amount,
            category=category,
            description=self.desc_input.text,
            date=self.date_input.text,
            transaction_type=TransactionType(self.type_spinner.text)
        )
        
        self.db.add_expense(expense)
        self.show_message('Success', 'Transaction added!')
        self.clear_form()
        self.load_data()
    
    def clear_form(self, instance=None):
        self.amount_input.text = ''
        self.category_spinner.text = 'Select category'
        self.desc_input.text = ''
        self.date_input.text = get_current_date()
    
    def load_data(self):
        # Clear existing
        self.transactions_layout.clear_widgets()
        
        expenses = self.db.get_expenses()
        total_income = 0
        total_expense = 0
        
        for exp in expenses[:50]:  # Show last 50
            exp_id, amount, cat, desc, date, trans_type, created = exp
            
            if trans_type == 'income':
                total_income += amount
                color = (0.2, 0.7, 0.2, 1)
                sign = '+'
            else:
                total_expense += amount
                color = (0.9, 0.2, 0.2, 1)
                sign = '-'
            
            # Transaction item
            item = Card(
                bg_color=(0.98, 0.98, 0.98, 1),
                radius=[dp(5)]
            )
            item.height = dp(70)
            
            # Top row: Date and Amount
            top_row = BoxLayout(size_hint_y=None, height=dp(30))
            top_row.add_widget(Label(
                text=date,
                font_size='12sp',
                color=(0.5, 0.5, 0.5, 1),
                halign='left'
            ))
            top_row.add_widget(Label(
                text=f'{sign}{format_currency(amount)}',
                font_size='14sp',
                bold=True,
                color=color,
                halign='right'
            ))
            item.add_widget(top_row)
            
            # Bottom row: Category and Description
            bottom_row = BoxLayout(size_hint_y=None, height=dp(30))
            bottom_row.add_widget(Label(
                text=f'{cat} • {desc[:20]}',
                font_size='12sp',
                color=(0.3, 0.3, 0.3, 1),
                halign='left'
            ))
            item.add_widget(bottom_row)
            
            # Make clickable for delete
            item.bind(on_touch_down=lambda touch, exp_id=exp_id: self.on_item_touch(touch, exp_id))
            
            self.transactions_layout.add_widget(item)
        
        # Update summary
        net = total_income - total_expense
        self.summary_label.text = (
            f'Income: {format_currency(total_income)} | '
            f'Expense: {format_currency(total_expense)}\n'
            f'Net: {format_currency(net)}'
        )
        self.summary_label.color = (0.2, 0.7, 0.2, 1) if net >= 0 else (0.9, 0.2, 0.2, 1)
    
    def on_item_touch(self, touch, exp_id):
        if touch.button == 'right' or touch.is_double_tap:
            self.confirm_action(
                'Delete',
                'Delete this transaction?',
                lambda: self.delete_expense(exp_id)
            )
    
    def delete_expense(self, exp_id):
        self.db.delete_expense(exp_id)
        self.load_data()