from tkinter import Tk, Label, Button, filedialog, StringVar, IntVar, ttk
import threading
import PyPDF2
import time
import sys

class PDFToTextApp:
    def __init__(self, root):
        self.root = root
        root.title("PDF to Text Converter")
        
        self.pdf_path = StringVar()
        self.pdf_path.set("No PDF selected")
        
        self.txt_path = StringVar()
        self.txt_path.set("No destination selected")
        
        self.progress = IntVar()
        
        self.label_pdf = Label(root, textvariable=self.pdf_path)
        self.label_pdf.pack()
        
        self.select_pdf_button = Button(root, text="Select PDF", command=self.select_pdf)
        self.select_pdf_button.pack()
        
        self.label_txt = Label(root, textvariable=self.txt_path)
        self.label_txt.pack()
        
        self.select_txt_button = Button(root, text="Select Destination", command=self.select_destination)
        self.select_txt_button.pack()
        
        self.progress_bar = ttk.Progressbar(root, variable=self.progress, maximum=100)
        self.progress_bar.pack()
        
        self.convert_button = Button(root, text="Convert", command=self.start_conversion)
        self.convert_button.pack()
        
    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_path.set(file_path)
            
    def select_destination(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.txt_path.set(file_path)
            
    def start_conversion(self):
        if self.pdf_path.get() == "No PDF selected" or self.txt_path.get() == "No destination selected":
            return
        
        thread = threading.Thread(target=self.convert_pdf_to_txt)
        thread.daemon = True
        thread.start()
        
    def convert_pdf_to_txt(self):
        pdf_path = self.pdf_path.get()
        txt_path = self.txt_path.get()
        
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)
            
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    txt_file.write(text)
                    
                    self.progress.set((page_num + 1) * 100 // total_pages)
                    self.root.update_idletasks()
                    
        self.progress.set(0)

# Initialize the application
root = Tk()
root.geometry("400x200")
app = PDFToTextApp(root)
root.mainloop()