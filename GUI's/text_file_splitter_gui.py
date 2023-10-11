from tkinter import Tk, Label, Button, filedialog, StringVar, IntVar, ttk
import threading
import os

class TextSplitApp:
    def __init__(self, root):
        self.root = root
        root.title("Text File Splitter")
        
        self.txt_path = StringVar()
        self.txt_path.set("No text file selected")
        
        self.output_dir = StringVar()
        self.output_dir.set("No output directory selected")
        
        self.progress = IntVar()
        
        self.label_txt = Label(root, textvariable=self.txt_path)
        self.label_txt.pack()
        
        self.select_txt_button = Button(root, text="Select Text File", command=self.select_txt)
        self.select_txt_button.pack()
        
        self.label_output_dir = Label(root, textvariable=self.output_dir)
        self.label_output_dir.pack()
        
        self.select_output_dir_button = Button(root, text="Select Output Directory", command=self.select_output_dir)
        self.select_output_dir_button.pack()
        
        self.progress_bar = ttk.Progressbar(root, variable=self.progress, maximum=100)
        self.progress_bar.pack()
        
        self.split_button = Button(root, text="Split File", command=self.start_split)
        self.split_button.pack()
        
    def select_txt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.txt_path.set(file_path)
            
    def select_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir.set(dir_path)
            
    def start_split(self):
        if self.txt_path.get() == "No text file selected" or self.output_dir.get() == "No output directory selected":
            return
        
        thread = threading.Thread(target=self.split_txt_file)
        thread.daemon = True
        thread.start()
        
    def split_txt_file(self):
        input_file = self.txt_path.get()
        output_dir = self.output_dir.get()
        max_chars = 9300  # You can adjust this number
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        start = 0
        end = max_chars
        file_count = 1
        total_chars = len(content)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        while start < total_chars:
            end = min(end, total_chars)
            while end > start and content[end-1] != '\n':
                end -= 1
            
            if end == start:
                end = start + max_chars
            
            output_file = os.path.join(output_dir, f'split_{file_count}.txt')
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(content[start:end])
                
            self.progress.set((end * 100) // total_chars)
            self.root.update_idletasks()
            
            start = end
            end = start + max_chars
            file_count += 1
            
        self.progress.set(0)

# Initialize the application
root = Tk()
root.geometry("400x200")
app = TextSplitApp(root)
root.mainloop()