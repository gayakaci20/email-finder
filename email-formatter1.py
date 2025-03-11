import re
import smtplib
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

def format_emails_from_input():
    """
    Fonction interactive pour formater et tester des adresses email.
    """
    print("Email Address Formatter & Validator")
    print("===================================")
    
    names_input = input("Entrez les noms (un par ligne, appuyez deux fois sur Entrée pour terminer) :\n")
    names = []
    while names_input:
        names.append(names_input)
        names_input = input()
    
    domain = input("Entrez le domaine email (ex. company.com) : ")
    
    print("\nChoisissez le format d'email :")
    print("1. firstname.lastname (ex: john.doe)")
    print("2. f.lastname (ex: j.doe)")
    print("3. firstname.l (ex: john.d)")
    print("4. firstnamelastname (ex: johndoe)")
    print("5. flastname (ex: jdoe)")
    print("6. lastname.firstname (ex: doe.john)")
    print("7. l.firstname (ex: d.john)")
    print("8. initials (ex: jd)")
    print("9. Tester toutes les options et identifier la bonne adresse")
    print("10. Afficher toutes les options sans test de validité")
    
    format_choice = input("Entrez votre choix (1-10) : ")
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
    
    if format_choice == '9':
        valid_emails = identify_valid_email(names, domain)
        print("\nAdresses email valides identifiées :")
        for name, email in valid_emails.items():
            print(f"{name}: {email}")
    elif format_choice == '10':
        all_formats = format_email_all_styles(names, domain)
        print("\nToutes les adresses email possibles (sans test de validité) :")
        for i, name in enumerate(names):
            print(f"\nPour {name}:")
            for style, emails in all_formats.items():
                print(f"{style}: {emails[i]}")
    else:
        email_format = format_options.get(format_choice, 'firstname.lastname')
        formatted_emails = format_email_addresses(names, domain, email_format)
        print("\nAdresses email formatées :")
        for email in formatted_emails:
            print(email)

if __name__ == "__main__":
    format_emails_from_input()