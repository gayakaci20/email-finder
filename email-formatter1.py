import re
import smtplib
from email_validator import validate_email, EmailNotValidError

def format_email_addresses(names, domain, style):
    """
    Formats email addresses according to the specified style.
    """
    emails = []
    for name in names:
        parts = name.strip().lower().split()
        if len(parts) < 2:
            # If only one word, consider it as first name
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
        
        # Clean the email (preserve hyphens, remove other special characters)
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
    Generates all email address variants for each name.
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

    api_key = 'API KEY HERE --------->>>>>>'                       # Replace with your API key
    api_url = f'https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}'

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            # Check if the email is deliverable and has valid format
            if data.get('deliverability') == 'DELIVERABLE' and data.get('is_valid_format').get('value'):
                return email
        return None
    except Exception:
        return None

def identify_valid_email(names, domain):
    """
    Identifies the best valid email address among the generated formats.
    """
    all_formats = format_email_all_styles(names, domain)
    valid_emails = {}
    
    for i, name in enumerate(names):
        for style, emails in all_formats.items():
            email = emails[i]
            if test_email_delivery(email):
                valid_emails[name] = email
                break  # Takes the first valid address found
    
    return valid_emails

def validate_email_regex(email):
    """
    Validates email address using regex pattern.
    Returns True if email is valid, False otherwise.
    """
    # Allow hyphens in both local part and domain, but not at start/end of parts
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]@(?!-)[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9](\.[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])*\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        # Additional checks
        if len(email) <= 254:  # Maximum length check
            local_part = email.split('@')[0]
            if len(local_part) <= 64:  # Local part length check
                # Ensure no consecutive hyphens
                if '--' not in local_part and '--' not in email.split('@')[1]:
                    return True
    return False

def format_emails_from_input():
    """
    Interactive function to format and test email addresses.
    """
    print("Email Address Formatter & Validator")
    print("===================================")
    
    names_input = input("Enter names (one per line, press Enter twice to finish):\n")
    names = []
    while names_input:
        names.append(names_input)
        names_input = input()
    
    domain = input("Enter email domain (e.g. company.com): ")
    
    print("\nChoose email format:")
    print("1. firstname.lastname (e.g.: john.doe)")
    print("2. f.lastname (e.g.: j.doe)")
    print("3. firstname.l (e.g.: john.d)")
    print("4. firstnamelastname (e.g.: johndoe)")
    print("5. flastname (e.g.: jdoe)")
    print("6. lastname.firstname (e.g.: doe.john)")
    print("7. l.firstname (e.g.: d.john)")
    print("8. initials (e.g.: jd)")
    print("9. Test all options and identify the correct address")
    print("10. Display all options without validity testing")
    print("11. Validate emails using regex (offline validation)")
    
    format_choice = input("Enter your choice (1-11): ")
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
    
    emails_list = []
    
    if format_choice == '9':
        valid_emails = identify_valid_email(names, domain)
        print("\nIdentified valid email addresses:")
        for name, email in valid_emails.items():
            print(f"{name}: {email}")
            emails_list.append(email)
    elif format_choice == '10':
        all_formats = format_email_all_styles(names, domain)
        print("\nAll possible email addresses (without validity testing):")
        for i, name in enumerate(names):
            print(f"\nFor {name}:")
            for style, emails in all_formats.items():
                print(f"{style}: {emails[i]}")
                emails_list.append(emails[i])
    elif format_choice == '11':
        all_formats = format_email_all_styles(names, domain)
        print("\nValidating all possible email formats using regex:")
        for i, name in enumerate(names):
            print(f"\nFor {name}:")
            for style, emails in all_formats.items():
                email = emails[i]
                is_valid = validate_email_regex(email)
                status = "✓ Valid" if is_valid else "✗ Invalid"
                print(f"{style}: {email} - {status}")
                if is_valid:
                    emails_list.append(email)
    else:
        email_format = format_options.get(format_choice, 'firstname.lastname')
        formatted_emails = format_email_addresses(names, domain, email_format)
        print("\nFormatted email addresses:")
        for email in formatted_emails:
            print(email)
            emails_list.append(email)
    
    # Add option to copy emails
    if emails_list:
        copy_choice = input("\nWould you like to copy all emails to clipboard? (y/n): ")
        if copy_choice.lower() == 'y':
            try:
                import pyperclip
                email_text = '\n'.join(emails_list)
                pyperclip.copy(email_text)
                print("Emails copied to clipboard successfully!")
            except ImportError:
                print("pyperclip module not found. Please install it using: pip install pyperclip")
            except Exception as e:
                print(f"Failed to copy to clipboard: {str(e)}")

if __name__ == "__main__":
    format_emails_from_input()