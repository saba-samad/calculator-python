import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)
        
        # Variables
        self.current = ""
        self.expression = ""
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#2C3E50", pady=20)
        display_frame.pack(fill="x")
        
        # Main display
        display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Helvetica", 40, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1",
            anchor="e",
            padx=20
        )
        display.pack(fill="x")
        
        # Expression display
        self.expr_label = tk.Label(
            display_frame,
            text="",
            font=("Helvetica", 14),
            bg="#2C3E50",
            fg="#95A5A6",
            anchor="e",
            padx=20
        )
        self.expr_label.pack(fill="x")
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2C3E50")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Button layout
        buttons = [
            ('C', '#E74C3C'), ('⌫', '#E67E22'), ('%', '#E67E22'), ('÷', '#E67E22'),
            ('7', '#34495E'), ('8', '#34495E'), ('9', '#34495E'), ('×', '#E67E22'),
            ('4', '#34495E'), ('5', '#34495E'), ('6', '#34495E'), ('-', '#E67E22'),
            ('1', '#34495E'), ('2', '#34495E'), ('3', '#34495E'), ('+', '#E67E22'),
            ('±', '#34495E'), ('0', '#34495E'), ('.', '#34495E'), ('=', '#2ECC71')
        ]
        
        # Create and place buttons
        for i, (text, color) in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            # Button frame for padding
            btn_frame = tk.Frame(
                buttons_frame,
                bg="#2C3E50",
                padx=5,
                pady=5
            )
            btn_frame.grid(row=row, column=col, sticky="nsew")
            
            # Button
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Helvetica", 20),
                bg=color,
                fg="#FFFFFF",
                activebackground=self.adjust_color(color, 20),
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                command=lambda x=text: self.button_click(x)
            )
            btn.pack(expand=True, fill="both")
        
        # Configure grid weights
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def adjust_color(self, color, amount):
        """Darken the color by the given amount"""
        r = max(0, int(color[1:3], 16) - amount)
        g = max(0, int(color[3:5], 16) - amount)
        b = max(0, int(color[5:7], 16) - amount)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def button_click(self, value):
        if value == 'C':
            self.clear()
        elif value == '⌫':
            self.backspace()
        elif value == '=':
            self.calculate()
        elif value == '±':
            self.negate()
        else:
            self.append_value(value)
    
    def clear(self):
        self.current = ""
        self.expression = ""
        self.display_var.set("0")
        self.expr_label.config(text="")
    
    def backspace(self):
        self.current = self.current[:-1]
        if not self.current:
            self.current = "0"
        self.display_var.set(self.current)
    
    def negate(self):
        if self.current and self.current != "0":
            if self.current[0] == "-":
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.display_var.set(self.current)
    
    def append_value(self, value):
        if value in "0123456789.":
            if self.current == "0" and value != ".":
                self.current = value
            else:
                self.current += value
            self.display_var.set(self.current)
        else:
            if value == "×":
                self.expression += self.current + "*"
            elif value == "÷":
                self.expression += self.current + "/"
            elif value == "%":
                try:
                    result = float(self.current) / 100
                    self.current = str(result)
                    self.display_var.set(self.current)
                    return
                except ValueError:
                    self.display_var.set("Error")
                    return
            else:
                self.expression += self.current + value
            self.expr_label.config(text=self.expression)
            self.current = ""
    
    def calculate(self):
        try:
            self.expression += self.current
            result = eval(self.expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)
            
            self.current = str(result)
            self.display_var.set(self.current)
            self.expr_label.config(text=self.expression + "=")
            self.expression = ""
            
        except Exception as e:
            self.display_var.set("Error")
            self.current = ""
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
