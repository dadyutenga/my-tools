import os
import re
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CommentRemover:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Code Comment Remover")
        self.root.geometry("850x600")

        self.supported_extensions = {'.php', '.py', '.html', '.css', '.js'}

        self.setup_ui()

    def setup_ui(self):

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_label = ctk.CTkLabel(main_frame, text="🚀 Code Comment Remover",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 5))

        subtitle_label = ctk.CTkLabel(main_frame,
                                     text="Remove comments from PHP, Python, HTML, CSS & JavaScript files",
                                     font=ctk.CTkFont(size=12))
        subtitle_label.pack(pady=(0, 15))

        selection_frame = ctk.CTkFrame(main_frame)
        selection_frame.pack(fill="x", padx=15, pady=(0, 10))

        selection_title = ctk.CTkLabel(selection_frame, text="📁 File Selection",
                                      font=ctk.CTkFont(size=14, weight="bold"))
        selection_title.pack(pady=(10, 5))

        buttons_frame = ctk.CTkFrame(selection_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.select_files_btn = ctk.CTkButton(buttons_frame, text="📄 Select Files",
                                             command=self.select_files,
                                             font=ctk.CTkFont(size=11, weight="bold"),
                                             height=35, width=120)
        self.select_files_btn.pack(side="left", padx=(0, 8))

        self.select_folder_btn = ctk.CTkButton(buttons_frame, text="📂 Select Folder",
                                              command=self.select_folder,
                                              font=ctk.CTkFont(size=11, weight="bold"),
                                              height=35, width=120)
        self.select_folder_btn.pack(side="left", padx=(0, 8))

        self.clear_btn = ctk.CTkButton(buttons_frame, text="🗑️ Clear All",
                                      command=self.clear_selection,
                                      font=ctk.CTkFont(size=11, weight="bold"),
                                      height=35, width=100,
                                      fg_color="
        self.clear_btn.pack(side="left")

        files_frame = ctk.CTkFrame(main_frame)
        files_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        files_title = ctk.CTkLabel(files_frame, text="📋 Selected Files",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        files_title.pack(pady=(10, 5))

        self.files_textbox = ctk.CTkTextbox(files_frame, height=120,
                                           font=ctk.CTkFont(family="Consolas", size=10))
        self.files_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        options_frame = ctk.CTkFrame(main_frame)
        options_frame.pack(fill="x", padx=15, pady=(0, 10))

        options_title = ctk.CTkLabel(options_frame, text="⚙️ Options",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        options_title.pack(pady=(10, 5))

        self.backup_var = ctk.BooleanVar(value=True)
        self.backup_checkbox = ctk.CTkCheckBox(options_frame,
                                              text="💾 Create backup files (.bak)",
                                              variable=self.backup_var,
                                              font=ctk.CTkFont(size=12))
        self.backup_checkbox.pack(pady=(0, 10))

        process_frame = ctk.CTkFrame(main_frame)
        process_frame.pack(fill="x", padx=15, pady=(0, 10))

        process_title = ctk.CTkLabel(process_frame, text="🎯 Processing",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        process_title.pack(pady=(10, 5))

        action_frame = ctk.CTkFrame(process_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.files_count_label = ctk.CTkLabel(action_frame, text="Files: 0",
                                             font=ctk.CTkFont(size=12, weight="bold"))
        self.files_count_label.pack(side="left")

        self.process_btn = ctk.CTkButton(action_frame, text="🚀 REMOVE COMMENTS",
                                        command=self.start_processing,
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        height=40, width=200,
                                        fg_color="
        self.process_btn.pack(side="right")

        self.progress = ctk.CTkProgressBar(process_frame, width=400, height=20,
                                          progress_color="
        self.progress.pack(padx=15, pady=(0, 5))
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(process_frame, text="Ready to process files 🚀",
                                        font=ctk.CTkFont(size=11))
        self.status_label.pack(pady=(0, 10))

        self.selected_files = []

    def select_files(self):
        filetypes = [
            ('All Supported', '*.php;*.py;*.html;*.css;*.js'),
            ('PHP files', '*.php'),
            ('Python files', '*.py'),
            ('HTML files', '*.html'),
            ('CSS files', '*.css'),
            ('JavaScript files', '*.js'),
            ('All files', '*.*')
        ]

        files = filedialog.askopenfilenames(
            title="Select code files",
            filetypes=filetypes
        )

        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
            self.update_files_display()

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder containing code files")
        if folder:
            self.scan_folder(folder)
            self.update_files_display()

    def scan_folder(self, folder_path):
        count = 0
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file)
                if ext.lower() in self.supported_extensions:
                    if file_path not in self.selected_files:
                        self.selected_files.append(file_path)
                        count += 1

        if count > 0:
            self.status_label.configure(text=f"Added {count} files from folder 📁")

    def clear_selection(self):
        self.selected_files.clear()
        self.update_files_display()
        self.status_label.configure(text="Selection cleared 🗑️")

    def update_files_display(self):
        self.files_textbox.delete("0.0", "end")

        if not self.selected_files:
            self.files_textbox.insert("0.0", "No files selected yet...\n\n" +
                                     "Click 'Select Files' or 'Select Folder' to get started!")
        else:
            file_list = []
            for i, file_path in enumerate(self.selected_files, 1):
                _, ext = os.path.splitext(file_path)
                file_name = os.path.basename(file_path)
                folder_name = os.path.dirname(file_path)

                emoji = {"php": "🐘", "py": "🐍", "html": "🌐",
                        "css": "🎨", "js": "⚡"}.get(ext[1:], "📄")

                file_list.append(f"{i:2d}. {emoji} {file_name}")
                file_list.append(f"     📁 {folder_name}\n")

            self.files_textbox.insert("0.0", "\n".join(file_list))

        self.files_count_label.configure(text=f"Files: {len(self.selected_files)}")

    def remove_php_comments(self, content):
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content

    def remove_python_comments(self, content):
        content = re.sub(r'
        content = re.sub(r'', '', content, flags=re.DOTALL)
        content = re.sub(r"", '', content, flags=re.DOTALL)
        return content

    def remove_html_comments(self, content):
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        return content

    def remove_css_comments(self, content):
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content

    def remove_js_comments(self, content):
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content

    def process_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_content = content
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            if ext == '.php':
                content = self.remove_php_comments(content)
            elif ext == '.py':
                content = self.remove_python_comments(content)
            elif ext == '.html':
                content = self.remove_html_comments(content)
            elif ext == '.css':
                content = self.remove_css_comments(content)
            elif ext == '.js':
                content = self.remove_js_comments(content)

            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

            if self.backup_var.get():
                backup_path = file_path + '.bak'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, None

        except Exception as e:
            return False, str(e)

    def start_processing(self):
        if not self.selected_files:
            messagebox.showwarning("No Files Selected",
                                 "Please select some files or folders first! 📂")
            return

        self.process_btn.configure(state="disabled", text="⏳ PROCESSING...")
        self.select_files_btn.configure(state="disabled")
        self.select_folder_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")

        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()

    def process_files(self):
        total_files = len(self.selected_files)
        processed = 0
        errors = []

        for i, file_path in enumerate(self.selected_files):
            file_name = os.path.basename(file_path)
            self.status_label.configure(text=f"Processing: {file_name} ⚡")

            progress_value = (i + 1) / total_files
            self.progress.set(progress_value)
            self.root.update()

            success, error = self.process_file(file_path)
            if success:
                processed += 1
            else:
                errors.append(f"{file_path}: {error}")

        self.process_btn.configure(state="normal", text="🚀 REMOVE COMMENTS")
        self.select_files_btn.configure(state="normal")
        self.select_folder_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")

        if errors:
            error_msg = f"Processed {processed}/{total_files} files successfully.\n\n"
            error_msg += "Errors encountered:\n" + "\n".join(errors[:3])
            if len(errors) > 3:
                error_msg += f"\n... and {len(errors) - 3} more errors"
            messagebox.showwarning("Processing Complete with Errors", error_msg)
            self.status_label.configure(text=f"⚠️ Completed with {len(errors)} errors")
        else:
            messagebox.showinfo("Success! 🎉",
                              f"Successfully processed {processed} files!\n\n" +
                              "All comments have been removed! 🚀")
            self.status_label.configure(text=f"✅ Successfully processed {processed} files!")

        self.progress.set(0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CommentRemover()
    app.run()