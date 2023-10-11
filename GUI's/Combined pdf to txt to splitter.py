# Import required modules from Tkinter, threading, PyPDF2, os, and tempfile
from tkinter import Tk, Label, Button, filedialog, StringVar, IntVar, ttk
import threading
import PyPDF2
import os
import tempfile

# Define the StreamlinedApp class
class StreamlinedApp:
    def __init__(self, root):
        # Initialize the Tkinter root window
        self.root = root
        root.title("PDF to Split Text")
        
        # Initialize variables to hold the PDF path and output directory
        self.pdf_path = StringVar()
        self.pdf_path.set("No PDF selected")
        
        self.output_dir = StringVar()
        self.output_dir.set("No output directory selected")
        
        # Initialize a variable to hold the progress value
        self.progress = IntVar()
        
        # Create and pack labels and buttons into the Tkinter window
        self.label_pdf = Label(root, textvariable=self.pdf_path)
        self.label_pdf.pack()
        
        self.select_pdf_button = Button(root, text="Select PDF", command=self.select_pdf)
        self.select_pdf_button.pack()
        
        self.label_output_dir = Label(root, textvariable=self.output_dir)
        self.label_output_dir.pack()
        
        self.select_output_dir_button = Button(root, text="Select Output Directory", command=self.select_output_dir)
        self.select_output_dir_button.pack()
        
        # Create and pack a progress bar
        self.progress_bar = ttk.Progressbar(root, variable=self.progress, maximum=100)
        self.progress_bar.pack()

        # Create and pack a label to show status messages
        self.status_label = Label(root, text="")
        self.status_label.pack()
        
        # Create and pack a button to start the PDF processing
        self.process_button = Button(root, text="Process", command=self.start_process)
        self.process_button.pack()

    # Method to open a file dialog and select a PDF file
    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_path.set(file_path)
            
    # Method to open a directory dialog and select an output directory
    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)
            
    # Method to start the PDF processing in a separate thread
    def start_process(self):
        if self.pdf_path.get() == "No PDF selected" or self.output_dir.get() == "No output directory selected":
            return
        
        thread = threading.Thread(target=self.process_pdf)
        thread.daemon = True
        thread.start()
        
    # Method to process the PDF file
    def process_pdf(self):
        # Convert PDF to Text
        pdf_path = self.pdf_path.get()
        
        # Create a temporary text file to store the PDF text
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w+', encoding='utf-8') as temp_txt_file:
            temp_txt_path = temp_txt_file.name
            
            # Open the PDF file and read its content
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                total_pages = len(pdf_reader.pages)
                
                # Loop through each page and extract text
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    temp_txt_file.write(text)
                    
                    # Update the progress bar
                    self.progress.set((page_num + 1) * 50 // total_pages)
                    self.root.update_idletasks()
            
            # Close the temporary text file
            temp_txt_file.close()
        
        # Split the Text File
        self.split_txt_file(temp_txt_path)
        
        # Remove the temporary text file
        os.remove(temp_txt_path)

        # Update the status label
        self.status_label.config(text="The file is now split!")
        
        # Reset the progress bar
        self.progress.set(0)
        
    # Method to split the text file into smaller parts
    def split_txt_file(self, input_file):
        output_dir = self.output_dir.get()
        max_chars = 9350  # Maximum characters in each split file
        
        # Read the content of the input text file
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        # Initialize variables to keep track of the start and end indices for each split
        start = 0
        end = max_chars
        file_count = 1
        total_chars = len(content)
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Loop to split the text file and save each part
        while start < total_chars:
            end = min(end, total_chars)
            while end > start and content[end-1] != '\n':
                end -= 1
            
            if end == start:
                end = start + max_chars
            
            output_file = os.path.join(output_dir, f'split_{file_count}.txt')
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(content[start:end])
                
            # Update the progress bar
            self.progress.set(50 + (end * 50) // total_chars)
            self.root.update_idletasks()
            
            start = end
            end = start + max_chars
            file_count += 1

# Initialize the Tkinter application
root = Tk()
root.geometry("400x250")
app = StreamlinedApp(root)
root.mainloop()