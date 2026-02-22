# screens/report_screen.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.clock import Clock

from screens.base_screen import BaseScreen
from widgets.custom_widgets import Card, CustomSpinner, PrimaryButton
from utils import get_month_options, format_currency, get_current_month

class ReportScreen(BaseScreen):
    def build_ui(self):
        super().build_ui()
        
        # Header
        self.header.add_widget(Label(
            text='📊 Reports',
            font_size='20sp',
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        ))
        
        # Controls
        control_card = Card(bg_color=(0.98, 0.98, 0.98, 1))
        control_card.height = dp(80)
        
        control_layout = BoxLayout(spacing=dp(10))
        control_layout.add_widget(Label(text='Month:', size_hint_x=None, width=dp(80)))
        
        self.month_spinner = CustomSpinner(
            text=get_current_month(),
            values=get_month_options(),
            size_hint_x=0.5
        )
        control_layout.add_widget(self.month_spinner)
        
        gen_btn = PrimaryButton(text='Generate', size_hint_x=0.3)
        gen_btn.bind(on_press=self.generate_report)
        control_layout.add_widget(gen_btn)
        
        control_card.add_widget(control_layout)
        self.content.add_widget(control_card)
        
        # Summary Cards
        self.summary_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        self.summary_grid.bind(minimum_height=self.summary_grid.setter('height'))
        
        # Income Card
        self.income_card = Card(bg_color=(0.9, 1, 0.9, 1))
        self.income_card.height = dp(100)
        self.income_card.add_widget(Label(text='INCOME', font_size='12sp', color=(0.4, 0.4, 0.4, 1)))
        self.income_label = Label(text='₹0.00', font_size='20sp', bold=True, color=(0.2, 0.6, 0.2, 1))
        self.income_card.add_widget(self.income_label)
        self.summary_grid.add_widget(self.income_card)
        
        # Expense Card
        self.expense_card = Card(bg_color=(1, 0.9, 0.9, 1))
        self.expense_card.height = dp(100)
        self.expense_card.add_widget(Label(text='EXPENSE', font_size='12sp', color=(0.4, 0.4, 0.4, 1)))
        self.expense_label = Label(text='₹0.00', font_size='20sp', bold=True, color=(0.8, 0.2, 0.2, 1))
        self.expense_card.add_widget(self.expense_label)
        self.summary_grid.add_widget(self.expense_card)
        
        # Savings Card
        self.savings_card = Card(bg_color=(0.9, 0.95, 1, 1))
        self.savings_card.height = dp(100)
        self.savings_card.add_widget(Label(text='NET SAVINGS', font_size='12sp', color=(0.4, 0.4, 0.4, 1)))
        self.savings_label = Label(text='₹0.00', font_size='22sp', bold=True)
        self.savings_card.add_widget(self.savings_label)
        self.summary_grid.add_widget(self.savings_card)
        
        # Pending Udhar Card
        self.udhar_card = Card(bg_color=(1, 0.95, 0.9, 1))
        self.udhar_card.height = dp(100)
        self.udhar_card.add_widget(Label(text='PENDING UDHAR', font_size='12sp', color=(0.4, 0.4, 0.4, 1)))
        self.udhar_label = Label(text='₹0.00', font_size='20sp', bold=True, color=(0.9, 0.4, 0.1, 1))
        self.udhar_card.add_widget(self.udhar_label)
        self.summary_grid.add_widget(self.udhar_card)
        
        self.content.add_widget(self.summary_grid)
        
        # Category Breakdown
        self.cat_card = Card(bg_color=(1, 1, 1, 1))
        self.cat_card.height = dp(300)
        self.cat_card.add_widget(Label(
            text='Category Breakdown',
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))
        
        self.cat_layout = GridLayout(cols=1, spacing=dp(2), size_hint_y=None)
        self.cat_layout.bind(minimum_height=self.cat_layout.setter('height'))
        
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.cat_layout)
        self.cat_card.add_widget(scroll)
        
        self.content.add_widget(self.cat_card)
        
        # Generate initial report
        Clock.schedule_once(lambda dt: self.generate_report(), 0)
    
    def generate_report(self, instance=None):
        try:
            year, month = map(int, self.month_spinner.text.split('-'))
        except:
            self.show_message('Error', 'Invalid month format')
            return
        
        summary = self.db.get_monthly_summary(year, month)
        
        # Update cards
        self.income_label.text = format_currency(summary['total_income'])
        self.expense_label.text = format_currency(summary['total_expense'])
        
        savings = summary['net_savings']
        self.savings_label.text = format_currency(savings)
        self.savings_label.color = (0.2, 0.6, 0.2, 1) if savings >= 0 else (0.8, 0.2, 0.2, 1)
        
        self.udhar_label.text = format_currency(summary['pending_udhar'])
        
        # Update category breakdown
        self.cat_layout.clear_widgets()
        
        total = summary['total_expense']
        for category, amount in summary['category_breakdown']:
            percentage = (amount / total * 100) if total > 0 else 0
            
            row = BoxLayout(size_hint_y=None, height=dp(40))
            
            # Category name
            row.add_widget(Label(
                text=category,
                font_size='13sp',
                halign='left',
                size_hint_x=0.4
            ))
            
            # Progress bar background
            bar_container = BoxLayout(size_hint_x=0.4)
            with bar_container.canvas:
                Color(0.9, 0.9, 0.9, 1)
                Rectangle(pos=bar_container.pos, size=bar_container.size)
            
            # Progress fill
            bar_fill = BoxLayout()
            bar_fill.width = 0  # Will be updated
            bar_container.add_widget(bar_fill)
            
            row.add_widget(bar_container)
            
            # Amount
            row.add_widget(Label(
                text=f'{format_currency(amount)} ({percentage:.0f}%)',
                font_size='12sp',
                halign='right',
                size_hint_x=0.3,
                color=(0.4, 0.4, 0.4, 1)
            ))
            
            self.cat_layout.add_widget(row)