import re
import tkinter as tk
from tkinter import ttk, scrolledtext
from email_validator import validate_email, EmailNotValidError

def format_email_addresses(names, domain, style):
    """
    Formate les adresses email selon le style spécifié.
    """
    emails = []
    for name in names:
        parts = name.strip().lower().split()
        if len(parts) < 2:
            # Si un seul mot, on le considère comme prénom
            firstname = parts[0]
            lastname = ""
        else:
            firstname = parts[0]
            lastname = parts[-1]  # Prend le dernier mot comme nom de famille
        
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
        
        # Nettoyer l'email (enlever les caractères spéciaux)
        email = re.sub(r'[^a-z0-9.@]', '', email)
        emails.append(email)
    
    return emails

def format_email_all_styles(names, domain):
    """
    Génère toutes les variantes d'adresses email pour chaque nom.
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
    Simule un test d'envoi d'email.
    """
    try:
        validation = validate_email(email, check_deliverability=True)
        return validation.email
    except EmailNotValidError:
        return None

def identify_valid_email(names, domain):
    """
    Identifie la meilleure adresse email valide parmi les formats générés.
    """
    all_formats = format_email_all_styles(names, domain)
    valid_emails = {}
    
    for i, name in enumerate(names):
        for style, emails in all_formats.items():
            email = emails[i]
            if test_email_delivery(email):
                valid_emails[name] = email
                break  # Prend la première adresse valide trouvée
    
    return valid_emails

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
        input_frame = ttk.LabelFrame(self.root, text="Entrée des données")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Names input
        ttk.Label(input_frame, text="Entrez les noms (un par ligne):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.names_text = scrolledtext.ScrolledText(input_frame, width=40, height=8)
        self.names_text.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        
        # Domain input
        ttk.Label(input_frame, text="Entrez le domaine email (ex. company.com):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.domain_entry = ttk.Entry(input_frame, width=30)
        self.domain_entry.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Configure grid
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)
        
    def create_options_frame(self):
        options_frame = ttk.LabelFrame(self.root, text="Options de formatage")
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
            ("9. Tester toutes les options et identifier la bonne adresse", "9"),
            ("10. Afficher toutes les options sans test de validité", "10")
        ]
        
        for i, (text, value) in enumerate(formats):
            ttk.Radiobutton(options_frame, text=text, value=value, variable=self.format_var).grid(
                row=i // 2, column=i % 2, sticky=tk.W, padx=5, pady=2
            )
        
        # Process button
        ttk.Button(options_frame, text="Générer les adresses email", command=self.process_emails).grid(
            row=5, column=0, columnspan=2, pady=10
        )
        
        # Configure grid
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        
    def create_output_frame(self):
        output_frame = ttk.LabelFrame(self.root, text="Résultats")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(output_frame, width=80, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def process_emails(self):
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Get input values
        names_input = self.names_text.get(1.0, tk.END).strip()
        domain = self.domain_entry.get().strip()
        format_choice = self.format_var.get()
        
        if not names_input or not domain:
            self.result_text.insert(tk.END, "Erreur: Veuillez entrer des noms et un domaine.")
            self.status_var.set("Erreur: Données manquantes")
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
        
        self.status_var.set("Traitement en cours...")
        self.root.update_idletasks()
        
        try:
            if format_choice == '9':
                self.result_text.insert(tk.END, "Recherche des adresses email valides...\n\n")
                valid_emails = identify_valid_email(names, domain)
                self.result_text.insert(tk.END, "Adresses email valides identifiées :\n")
                for name, email in valid_emails.items():
                    self.result_text.insert(tk.END, f"{name}: {email}\n")
                    
                if not valid_emails:
                    self.result_text.insert(tk.END, "Aucune adresse email valide trouvée.\n")
                    
            elif format_choice == '10':
                all_formats = format_email_all_styles(names, domain)
                self.result_text.insert(tk.END, "Toutes les adresses email possibles (sans test de validité) :\n")
                for i, name in enumerate(names):
                    self.result_text.insert(tk.END, f"\nPour {name}:\n")
                    for style, emails in all_formats.items():
                        self.result_text.insert(tk.END, f"{style}: {emails[i]}\n")
            else:
                email_format = format_options.get(format_choice, 'firstname.lastname')
                formatted_emails = format_email_addresses(names, domain, email_format)
                self.result_text.insert(tk.END, "Adresses email formatées :\n")
                for i, email in enumerate(formatted_emails):
                    self.result_text.insert(tk.END, f"{names[i]}: {email}\n")
                    
            self.status_var.set("Traitement terminé avec succès")
        except Exception as e:
            self.result_text.insert(tk.END, f"Erreur lors du traitement: {str(e)}")
            self.status_var.set("Erreur lors du traitement")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmailFormatterApp(root)
    root.mainloop()