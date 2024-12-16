import tkinter as tk
from tkinter import messagebox, ttk
import imaplib
import email
from email.header import decode_header
import json
import os
from pathlib import Path
import base64


class EmailManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Manager")
        self.root.geometry("800x600")

        # Config file path
        self.config_file = Path.home() / '.email_manager_config.json'

        # Email connection settings
        self.email_address = None
        self.password = None
        self.imap_server = None
        self.mail = None
        self.current_emails = []
        self.current_index = 0
        self.labels = []

        # Login Frame
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Email:").grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self.login_frame, width=40)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="App Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, width=40, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="IMAP Server:").grid(row=2, column=0, padx=5, pady=5)
        self.server_entry = tk.Entry(self.login_frame, width=40)
        self.server_entry.grid(row=2, column=1, padx=5, pady=5)
        self.server_entry.insert(0, "imap.gmail.com")

        self.save_credentials_var = tk.BooleanVar(value=True)
        self.save_credentials_check = tk.Checkbutton(
            self.login_frame,
            text="Save credentials",
            variable=self.save_credentials_var
        )
        self.save_credentials_check.grid(row=3, column=0, columnspan=2, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Load saved credentials
        self.load_saved_credentials()

        # Email Display Frame
        self.email_frame = tk.Frame(root)

        self.subject_label = tk.Label(self.email_frame, text="", wraplength=700, font=('Arial', 12, 'bold'))
        self.subject_label.pack(pady=10)

        self.from_label = tk.Label(self.email_frame, text="", wraplength=700)
        self.from_label.pack(pady=5)

        self.content_text = tk.Text(self.email_frame, wrap=tk.WORD, height=20, width=80)
        self.content_text.pack(pady=10)

        # Action Frame
        self.action_frame = tk.Frame(self.email_frame)
        self.action_frame.pack(pady=10)

        # Label selection
        self.label_frame = tk.Frame(self.action_frame)
        self.label_frame.pack(side=tk.TOP, pady=5)

        tk.Label(self.label_frame, text="Apply Label:").pack(side=tk.LEFT, padx=5)
        self.label_var = tk.StringVar()
        self.label_combo = ttk.Combobox(self.label_frame, textvariable=self.label_var)
        self.label_combo.pack(side=tk.LEFT, padx=5)

        # Buttons Frame
        self.button_frame = tk.Frame(self.action_frame)
        self.button_frame.pack(side=tk.TOP, pady=5)

        self.keep_button = tk.Button(self.button_frame, text="Keep", command=self.keep_email)
        self.keep_button.pack(side=tk.LEFT, padx=5)

        self.archive_button = tk.Button(self.button_frame, text="Archive", command=self.archive_email)
        self.archive_button.pack(side=tk.LEFT, padx=5)

        self.apply_label_button = tk.Button(self.button_frame, text="Apply Label", command=self.apply_label)
        self.apply_label_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_email)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def load_saved_credentials(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.email_entry.insert(0, config.get('email', ''))
                    decoded_password = base64.b64decode(config.get('password', '')).decode()
                    self.password_entry.insert(0, decoded_password)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load saved credentials: {str(e)}")

    def save_credentials(self):
        if self.save_credentials_var.get():
            try:
                config = {
                    'email': self.email_address,
                    'password': base64.b64encode(self.password.encode()).decode()
                }
                with open(self.config_file, 'w') as f:
                    json.dump(config, f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save credentials: {str(e)}")

    def get_labels(self):
        try:
            _, label_data = self.mail.list()
            self.labels = []
            for label in label_data:
                try:
                    _, label_name = label.decode().split('" "')
                    label_name = label_name.strip('"')
                    if not label_name.startswith('[Gmail]'):  # Skip Gmail system labels
                        self.labels.append(label_name)
                except:
                    continue
            self.label_combo['values'] = self.labels
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch labels: {str(e)}")

    def login(self):
        self.email_address = self.email_entry.get()
        self.password = self.password_entry.get()
        self.imap_server = self.server_entry.get()

        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)

            # Save credentials if requested
            self.save_credentials()

            # Switch to email management interface
            self.login_frame.pack_forget()
            self.email_frame.pack(pady=20, padx=20)

            # Get labels
            self.get_labels()

            # Load emails
            self.load_emails()

        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    def load_emails(self):
        self.mail.select('INBOX')
        _, messages = self.mail.search(None, 'ALL')
        self.current_emails = messages[0].split()

        if self.current_emails:
            self.show_email(0)
        else:
            messagebox.showinfo("Info", "No emails found")

    def show_email(self, index):
        if 0 <= index < len(self.current_emails):
            self.current_index = index
            email_id = self.current_emails[index]

            _, msg_data = self.mail.fetch(email_id, '(RFC822)')
            email_body = msg_data[0][1]
            message = email.message_from_bytes(email_body)

            # Display subject
            subject = decode_header(message["subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            self.subject_label.config(text=f"Subject: {subject}")

            # Display from
            sender = decode_header(message["from"])[0][0]
            if isinstance(sender, bytes):
                sender = sender.decode()
            self.from_label.config(text=f"From: {sender}")

            # Display content
            self.content_text.delete(1.0, tk.END)
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode()
                            self.content_text.insert(tk.END, body)
                        except:
                            continue
            else:
                try:
                    body = message.get_payload(decode=True).decode()
                    self.content_text.insert(tk.END, body)
                except:
                    self.content_text.insert(tk.END, "Unable to display content")

    def keep_email(self):
        if self.current_index < len(self.current_emails) - 1:
            self.show_email(self.current_index + 1)
        else:
            messagebox.showinfo("Info", "No more emails to process")

    def archive_email(self):
        if self.current_emails:
            try:
                email_id = self.current_emails[self.current_index]
                # Move to [Gmail]/All Mail (archive)
                self.mail.copy(email_id, '[Gmail]/All Mail')
                # Remove from inbox
                self.mail.store(email_id, '+FLAGS', '\\Deleted')
                self.mail.expunge()

                self.current_emails.pop(self.current_index)

                if self.current_emails:
                    if self.current_index >= len(self.current_emails):
                        self.current_index = len(self.current_emails) - 1
                    self.show_email(self.current_index)
                else:
                    messagebox.showinfo("Info", "No more emails to process")
                    self.clear_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to archive email: {str(e)}")

    def apply_label(self):
        if not self.label_var.get():
            messagebox.showwarning("Warning", "Please select a label first")
            return

        if self.current_emails:
            try:
                email_id = self.current_emails[self.current_index]
                self.mail.store(email_id, '+X-GM-LABELS', f'({self.label_var.get()})')
                messagebox.showinfo("Success", f"Applied label: {self.label_var.get()}")
                self.keep_email()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply label: {str(e)}")

    def delete_email(self):
        if self.current_emails:
            try:
                email_id = self.current_emails[self.current_index]
                self.mail.store(email_id, '+FLAGS', '\\Deleted')
                self.mail.expunge()

                self.current_emails.pop(self.current_index)

                if self.current_emails:
                    if self.current_index >= len(self.current_emails):
                        self.current_index = len(self.current_emails) - 1
                    self.show_email(self.current_index)
                else:
                    messagebox.showinfo("Info", "No more emails to process")
                    self.clear_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete email: {str(e)}")

    def clear_display(self):
        self.content_text.delete(1.0, tk.END)
        self.subject_label.config(text="")
        self.from_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmailManager(root)
    root.mainloop()