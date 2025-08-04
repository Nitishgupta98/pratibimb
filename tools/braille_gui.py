#!/usr/bin/env python3
"""
Braille Converter GUI - User-friendly interface for text-to-braille conversion
A simple graphical interface for the Grade 1 Braille converter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from braille_converter import text_to_braille_unicode, load_config

class BrailleConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Braille Converter - Text to Grade 1 Unicode Braille")
        self.root.geometry("800x600")
        
        # Load configuration
        self.config = load_config()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Braille Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Input file selection
        ttk.Label(main_frame, text="Input File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.input_file_var = tk.StringVar(value=self.config.get('input_file', 'input_text.txt'))
        input_file_entry = ttk.Entry(main_frame, textvariable=self.input_file_var, width=50)
        input_file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", 
                  command=self.browse_input_file).grid(row=1, column=2, pady=5)
        
        # Input text area
        ttk.Label(main_frame, text="Input Text:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=5)
        self.input_text = scrolledtext.ScrolledText(main_frame, height=10, width=60)
        self.input_text.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                           padx=5, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Load File", 
                  command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Convert to Braille", 
                  command=self.convert_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save Braille", 
                  command=self.save_braille).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Output text area
        ttk.Label(main_frame, text="Braille Output:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=5)
        self.output_text = scrolledtext.ScrolledText(main_frame, height=10, width=60)
        self.output_text.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                            padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Load initial file if exists
        if os.path.exists(self.input_file_var.get()):
            self.load_file()
    
    def browse_input_file(self):
        """Browse for input file"""
        filename = filedialog.askopenfilename(
            title="Select Input Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.input_file_var.set(filename)
    
    def load_file(self):
        """Load text from selected file"""
        try:
            filename = self.input_file_var.get()
            if not os.path.exists(filename):
                messagebox.showerror("Error", f"File '{filename}' not found!")
                return
            
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(1.0, content)
            self.status_var.set(f"Loaded {len(content)} characters from {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def convert_text(self):
        """Convert input text to Braille"""
        try:
            input_content = self.input_text.get(1.0, tk.END).rstrip('\n')
            if not input_content:
                messagebox.showwarning("Warning", "No input text to convert!")
                return
            
            # Convert to Braille
            braille_output = text_to_braille_unicode(input_content, self.config)
            
            # Display in output area
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, braille_output)
            
            # Update status
            self.status_var.set(f"Converted {len(input_content)} characters to Braille")
            
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")
    
    def save_braille(self):
        """Save Braille output to file"""
        try:
            braille_content = self.output_text.get(1.0, tk.END).rstrip('\n')
            if not braille_content:
                messagebox.showwarning("Warning", "No Braille output to save!")
                return
            
            filename = filedialog.asksaveasfilename(
                title="Save Braille Output",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(braille_content)
                
                self.status_var.set(f"Braille output saved to {filename}")
                messagebox.showinfo("Success", f"Braille output saved to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def clear_all(self):
        """Clear all text areas"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("Text areas cleared")

def main():
    root = tk.Tk()
    app = BrailleConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
