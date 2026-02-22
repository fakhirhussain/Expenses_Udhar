# database.py (Enhanced for mobile with proper paths)
import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple
from models import Expense, Udhar, TransactionType, UdharStatus
import os
from kivy.app import App

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Use app's user data directory for mobile storage
            app = App.get_running_app()
            if app:
                data_dir = app.user_data_dir
            else:
                data_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(data_dir, "udhar_expense.db")
        
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Udhar table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS udhar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_name TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date_given TEXT NOT NULL,
                due_date TEXT,
                status TEXT DEFAULT 'pending',
                amount_paid REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Udhar payments history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS udhar_payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                udhar_id INTEGER,
                amount REAL NOT NULL,
                payment_date TEXT NOT NULL,
                FOREIGN KEY (udhar_id) REFERENCES udhar(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Expense Operations
    def add_expense(self, expense: Expense) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (amount, category, description, date, transaction_type)
            VALUES (?, ?, ?, ?, ?)
        ''', expense.to_tuple())
        conn.commit()
        expense_id = cursor.lastrowid
        conn.close()
        return expense_id
    
    def get_expenses(self, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None,
                     category: Optional[str] = None) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM expenses WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if category:
            query += " AND category = ?"
            params.append(category)
            
        query += " ORDER BY date DESC, id DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def delete_expense(self, expense_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        conn.close()
    
    def get_categories(self) -> List[str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    # Udhar Operations
    def add_udhar(self, udhar: Udhar) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO udhar (person_name, amount, description, date_given, 
                             due_date, status, amount_paid)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', udhar.to_tuple())
        conn.commit()
        udhar_id = cursor.lastrowid
        conn.close()
        return udhar_id
    
    def get_udhar_list(self, status: Optional[str] = None) -> List[Tuple]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM udhar"
        params = []
        
        if status:
            query += " WHERE status = ?"
            params.append(status)
            
        query += " ORDER BY date_given DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def update_udhar_payment(self, udhar_id: int, payment_amount: float):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT amount, amount_paid FROM udhar WHERE id = ?", (udhar_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
            
        total_amount, current_paid = result
        new_paid = current_paid + payment_amount
        
        if new_paid >= total_amount:
            new_status = 'cleared'
        elif new_paid > 0:
            new_status = 'partial'
        else:
            new_status = 'pending'
        
        cursor.execute('''
            UPDATE udhar 
            SET amount_paid = ?, status = ?
            WHERE id = ?
        ''', (new_paid, new_status, udhar_id))
        
        cursor.execute('''
            INSERT INTO udhar_payments (udhar_id, amount, payment_date)
            VALUES (?, ?, ?)
        ''', (udhar_id, payment_amount, datetime.now().strftime("%Y-%m-%d")))
        
        conn.commit()
        conn.close()
        return True
    
    def delete_udhar(self, udhar_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM udhar_payments WHERE udhar_id = ?", (udhar_id,))
        cursor.execute("DELETE FROM udhar WHERE id = ?", (udhar_id,))
        conn.commit()
        conn.close()
    
    # Analytics
    def get_monthly_summary(self, year: int, month: int) -> dict:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        cursor.execute('''
            SELECT COALESCE(SUM(amount), 0) FROM expenses 
            WHERE transaction_type = 'expense' 
            AND date >= ? AND date < ?
        ''', (start_date, end_date))
        total_expense = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COALESCE(SUM(amount), 0) FROM expenses 
            WHERE transaction_type = 'income' 
            AND date >= ? AND date < ?
        ''', (start_date, end_date))
        total_income = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT category, COALESCE(SUM(amount), 0) 
            FROM expenses 
            WHERE transaction_type = 'expense' 
            AND date >= ? AND date < ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        ''', (start_date, end_date))
        category_breakdown = cursor.fetchall()
        
        cursor.execute('''
            SELECT COALESCE(SUM(amount - amount_paid), 0) 
            FROM udhar 
            WHERE status IN ('pending', 'partial')
        ''')
        pending_udhar = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_expense': total_expense,
            'total_income': total_income,
            'net_savings': total_income - total_expense,
            'category_breakdown': category_breakdown,
            'pending_udhar': pending_udhar
        }