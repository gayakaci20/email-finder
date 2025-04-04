import re
import tkinter as tk
from tkinter import ttk, scrolledtext
from email_validator import validate_email, EmailNotValidError
from normalize_chars import normalize_accented_chars

def format_email_addresses(names, domain, style):
    """
    Format email addresses according to the specified style.
    """
    emails = []
    for name in names:
        # Normalize accented characters in the name
        name = normalize_accented_chars(name)
        parts = name.strip().lower().split()
        if len(parts) < 2:
            # If single word, consider it as firstname
            firstname = parts[0]
            lastname = ""
        else:
            # Handle compound first names and last name
            lastname = parts[-1]  # Take the last word as lastname
            firstname_parts = parts[:-1]  # All words except the last one are part of the firstname
            firstname = '-'.join(firstname_parts)  # Join firstname parts with hyphens
        
        email = ""
        if style == 'firstname.lastname':
            email = f"{firstname}.{lastname}@{domain}"
        elif style == 'f.lastname':
            email = f"{firstname[0]}.{lastname}@{domain}"
        elif style == 'firstname.l':
            email = f"{firstname}.{lastname[0]}@{domain}"
        elif style == 'firstnamelastname':
            email = f"{firstname}{lastname}@{domain}"
        elif style == 'flastname':
            email = f"{firstname[0]}{lastname}@{domain}"
        elif style == 'lastname.firstname':
            email = f"{lastname}.{firstname}@{domain}"
        elif style == 'l.firstname':
            email = f"{lastname[0]}.{firstname}@{domain}"
        elif style == 'initials':
            email = f"{firstname[0]}{lastname[0]}@{domain}"
        
        # Clean email (preserve hyphens, remove other special characters)
        email = re.sub(r'[^a-z0-9.@-]', '', email)
        # Remove consecutive hyphens and ensure hyphens aren't at start/end of parts
        parts = email.split('@')
        local_part = re.sub(r'-+', '-', parts[0]).strip('-')
        domain = re.sub(r'-+', '-', parts[1]).strip('-')
        email = f"{local_part}@{domain}"
        emails.append(email)
    
    return emails

def format_email_all_styles(names, domain):
    """
    Generate all email address variants for each name.
    """
    styles = {
        'firstname.lastname': [],
        'f.lastname': [],
        'firstname.l': [],
        'firstnamelastname': [],
        'flastname': [],
        'lastname.firstname': [],
        'l.firstname': [],
        'initials': []
    }
    
    for style in styles.keys():
        styles[style] = format_email_addresses(names, domain, style)
    
    return styles

def test_email_delivery(email):
    """
    Tests email deliverability using Abstract API.
    """
    import requests
    import time

    api_key = 'API KEY HERE --------->>>>>>'                    # Replace with your API key
    api_url = f'https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}'

    try:
        # Add delay to respect API rate limits
        time.sleep(1)
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            # Check if the email is deliverable and has valid format
            if data.get('deliverability') == 'DELIVERABLE' and data.get('is_valid_format').get('value'):
                return email
            elif response.status_code == 429:  # Rate limit exceeded
                time.sleep(60)  # Wait for 60 seconds before retrying
                return test_email_delivery(email)  # Retry the request
        return None
    except Exception as e:
        print(f"Error testing email {email}: {str(e)}")
        return None

def identify_valid_email(names, domain):
    """
    Tests all possible email formats and returns validation results.
    """
    all_formats = format_email_all_styles(names, domain)
    validation_results = {}
    
    for i, name in enumerate(names):
        validation_results[name] = {}
        for style, emails in all_formats.items():
            email = emails[i]
            is_valid = test_email_delivery(email)
            validation_results[name][style] = {
                'email': email,
                'is_valid': bool(is_valid)
            }
    
    return validation_results

class EmailFormatterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Address Formatter & Validator")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Variables
        self.format_var = tk.StringVar(value="1")
        
        # Create main frames
        self.create_input_frame()
        self.create_options_frame()
        self.create_output_frame()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Data Input")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Names input
        ttk.Label(input_frame, text="Enter names (one per line):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.names_text = scrolledtext.ScrolledText(input_frame, width=40, height=8)
        self.names_text.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        # Domain input
        ttk.Label(input_frame, text="Enter email domain (e.g. company.com):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.domain_entry = ttk.Entry(input_frame, width=30)
        self.domain_entry.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Configure grid
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)
        
    def create_options_frame(self):
        options_frame = ttk.LabelFrame(self.root, text="Formatting Options")
        options_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Format options
        formats = [
            ("1. firstname.lastname (ex: john.doe)", "1"),
            ("2. f.lastname (ex: j.doe)", "2"),
            ("3. firstname.l (ex: john.d)", "3"),
            ("4. firstnamelastname (ex: johndoe)", "4"),
            ("5. flastname (ex: jdoe)", "5"),
            ("6. lastname.firstname (ex: doe.john)", "6"),
            ("7. l.firstname (ex: d.john)", "7"),
            ("8. initials (ex: jd)", "8"),
            ("9. Test all options and identify the correct address", "9"),
            ("10. Show all options without validity test", "10"),
            ("11. Validate emails using regex (offline validation)", "11")
        ]
        
        for i, (text, value) in enumerate(formats):
            ttk.Radiobutton(options_frame, text=text, value=value, variable=self.format_var).grid(
                row=i // 2, column=i % 2, sticky=tk.W, padx=5, pady=2
            )
        
        # Process button
        ttk.Button(options_frame, text="Generate email addresses", command=self.process_emails).grid(
            row=5, column=0, columnspan=2, pady=10
        )
        
        # Configure grid
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
    def create_output_frame(self):
        output_frame = ttk.LabelFrame(self.root, text="Results")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create a frame for the result text and copy button
        result_container = ttk.Frame(output_frame)
        result_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_container, width=80, height=10)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add copy button
        copy_button = ttk.Button(result_container, text="Copy Emails", command=self.copy_emails)
        copy_button.pack(side=tk.RIGHT, padx=5)
        
    def copy_emails(self):
        """Extract and copy only the email addresses from the results."""
        content = self.result_text.get(1.0, tk.END)
        # Extract email addresses using regex
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, content)
        
        if emails:
            # Join emails with newlines and copy to clipboard
            email_text = '\n'.join(emails)
            self.root.clipboard_clear()
            self.root.clipboard_append(email_text)
            self.status_var.set("Emails copied to clipboard")
        else:
            self.status_var.set("No emails found to copy")
    
    def process_emails(self):
        # Allow hyphens in domain name but not at start or end
        # Allow hyphens in domain name but not at start or end
        pattern = r'^[a-zA-Z0-9._%+-]+@(?!-)[a-zA-Z0-9-]+(?<!-)(\.[a-zA-Z0-9-]+(?<!-))*\.[a-zA-Z]{2,}$'
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Get input values
        names_input = self.names_text.get(1.0, tk.END).strip()
        domain = self.domain_entry.get().strip()
        format_choice = self.format_var.get()
        
        if not names_input or not domain:
            self.result_text.insert(tk.END, "Error: Please enter names and domain.")
            self.status_var.set("Error: Missing data")
            return
        
        # Process names
        names = [name for name in names_input.split('\n') if name.strip()]
        
        # Format options mapping
        format_options = {
            '1': 'firstname.lastname',
            '2': 'f.lastname',
            '3': 'firstname.l',
            '4': 'firstnamelastname',
            '5': 'flastname',
            '6': 'lastname.firstname',
            '7': 'l.firstname',
            '8': 'initials'
        }
        
        self.status_var.set("Processing...")
        self.root.update_idletasks()
        
        try:
            if format_choice == '9':
                self.result_text.insert(tk.END, "Testing all possible email formats...\n\n")
                emails_list = []
                validation_results = identify_valid_email(names, domain)
                self.result_text.insert(tk.END, "All possible email addresses with validation results:\n")
                for name, formats in validation_results.items():
                    self.result_text.insert(tk.END, f"\nFor {name}:\n")
                    for style, result in formats.items():
                        status = "✓ Valid" if result['is_valid'] else "✗ Invalid"
                        self.result_text.insert(tk.END, f"{style}: {result['email']} [{status}]\n")
                        if result['is_valid']:
                            emails_list.append(result['email'])
                    
            elif format_choice == '10':
                all_formats = format_email_all_styles(names, domain)
                self.result_text.insert(tk.END, "All possible email addresses (without validity test):\n")
                for i, name in enumerate(names):
                    self.result_text.insert(tk.END, f"\nFor {name}:\n")
                    for style, emails in all_formats.items():
                        self.result_text.insert(tk.END, f"{style}: {emails[i]}\n")
            elif format_choice == '11':
                all_formats = format_email_all_styles(names, domain)
                self.result_text.insert(tk.END, "Validating all possible email formats using regex:\n")
                for i, name in enumerate(names):
                    self.result_text.insert(tk.END, f"\nFor {name}:\n")
                    for style, emails in all_formats.items():
                        email = emails[i]
                        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        is_valid = bool(re.match(pattern, email) and
                                      len(email) <= 254 and
                                      len(email.split('@')[0]) <= 64)
                        status = "✓ Valid" if is_valid else "✗ Invalid"
                        self.result_text.insert(tk.END, f"{style}: {email} - {status}\n")
            else:
                email_format = format_options.get(format_choice, 'firstname.lastname')
                formatted_emails = format_email_addresses(names, domain, email_format)
                self.result_text.insert(tk.END, "Formatted email addresses:\n")
                for i, email in enumerate(formatted_emails):
                    self.result_text.insert(tk.END, f"{names[i]}: {email}\n")
                    
            self.status_var.set("Processing completed successfully")
        except Exception as e:
            self.result_text.insert(tk.END, f"Processing error: {str(e)}")
            self.status_var.set("Processing error")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailFormatterApp(root)
    root.mainloop()