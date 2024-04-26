from abstract_utilities import *
import os,json
from os.path import join,isfile,isdir,exists
import clipboard
def await_copy(print_str):
        print(print_str)
        clipboard.copy("null")
        spam = clipboard.paste()
        while True:
                if clipboard.paste() != spam:
                       return  clipboard.paste()
        return clipboard.paste()
def get_abs_path():
        return os.path.abspath(__file__)
def get_abs_dir():
        return dirname(get_abs_path())
def make_email(first, last, domain):
    """Generate an email address from a first name, last name, and domain."""
    return f"{first[0].lower()}{last.lower()}@{domain}"

def derive_email(first, last, email):
    """Derive the email convention based on a first name, last name, and a sample email."""
    domain = email.split('@')[1]  # Split the email to extract the domain part
    local_part = email.split('@')[0]  # Split the email to extract the local part
    pattern = ""

    # Determine pattern based on the local part of the email
    if local_part == f"{first[0].lower()}{last.lower()}":
        pattern = "{f}{l}"
    elif local_part == f"{first.lower()}{last.lower()}":
        pattern = "{ff}{l}"
    elif local_part == f"{first.lower()}":
        pattern = "{ff}"
    elif local_part == f"{first.lower()}.{last.lower()}":
        pattern = "{ff}.{l}"
    elif local_part == f"{first.lower()}{last[0].lower()}":
        pattern = "{ff}{ll}"
    elif local_part == f"{first[0].lower()}.{last.lower()}":
        pattern = "{f}.{l}"
    else:
        # Add more conditions as needed to identify other patterns
        pattern = "unknown"

    # Return the derived pattern and domain
    return pattern, domain
def get_email(first_name,last_name,pattern, domain):
        return f"{pattern.replace('{f}', first_name[0].lower()).replace('{l}', last_name.lower()).replace('{ff}', first_name.lower()).replace('{ll}', last_name[0].lower())}@{domain}"
def get_contacts():
    import os
    from os.path import join, abspath

    def get_abs_dir():
        """Return the absolute directory path of the current script."""
        return os.path.dirname(abspath(__file__))

    while True:
        # Simulate or replace `await_copy` with the actual function or logic to obtain data
        crunchbase_url = await_copy('Copy Crunchbase URL: ')
        company_name = crunchbase_url.split('/')[-1]
        company_path = join(get_abs_dir(), company_name)
        os.makedirs(company_path, exist_ok=True)

        email = await_copy('Copy email: ')
        name = await_copy('Copy name: ')

        first_name = name.split(' ')[0]
        last_name = name.split(' ')[-1]
        pattern, domain = derive_email(first_name, last_name, email)


        # Example to stop the loop, replace with appropriate condition
        contacts_html = await_copy("copy contacts")
        contacts_file = os.path.join(company_path, "contacts.txt")
        write_to_file(contents=contacts_html,file_path=contacts_file)
        contact_details = parse_contacts(contacts_html,pattern, domain)
        output_file_path = os.path.join(company_path, 'contacts.json')
        safe_dump_to_file(data=contact_details, file_path=output_file_path) 
def read_from_file(file_path):
    """Utility function to read from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def safe_dump_to_file(data, file_path):
    """Utility function to safely dump data into a file in JSON format."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def make_email(first, last, domain):
    """Generate an email address using the first letter of the first name and the full last name."""
    return f"{first[0].lower()}{last.lower()}@{domain}"

def clean_text(text):
    """Clean special characters from the text."""
    return text.replace('\u200b', '').replace("&amp;", "&").replace("&nbsp;", " ")

def parse_contacts(content,pattern, domain):
    """Parse contact information from the given content."""
    contacts = []
    for contact_info in content.split('<contacts-card-row')[1:]:
        visible = 1
        current_text = ''

        for char in contact_info:
            if visible % 2 == 0 and char not in ['<', '>']:
                current_text += char
            if char in ['<', '>']:
                visible += 1
                if current_text.strip() and current_text.strip() != ' ':
                    contacts.append(clean_text(current_text.strip()))
                    current_text = ''

    contact_details = []
    contact_js = {}
    for text in contacts:
        text = text.strip()
        if text and 'found' not in text and 'View' not in text:
            if '@' in text:
                contact_js['email'] = text
            elif '+1' in text:
                if 'phones' not in contact_js:
                    contact_js['phones'] = []
                contact_js['phones'].append(text)
            elif any(c.isdigit() for c in text):
                continue  # Skip if the text is numeric (likely phone or noise)
            else:
                if 'name' not in contact_js:
                    contact_js['name'] = text
                else:
                    if 'title' not in contact_js:
                        contact_js['title'] = []
                    contact_js['title'].append(text)

        if 'name' in contact_js and 'email' not in contact_js and ' ' in contact_js['name']:
            names = contact_js['name'].split(' ')
            contact_js['email'] = get_email(names[0], names[-1],pattern, domain)

        if contact_js:
            contact_details.append(contact_js)
            contact_js = {}

    return contact_details

def process_directory(base_path):
    """Process each company directory in the given base path."""
    for company in os.listdir(base_path):
        company_path = os.path.join(base_path, company)
        if os.path.isdir(company_path):
            contacts_file = os.path.join(company_path, "contacts.txt")
            contact_data = read_from_file(contacts_file)

            contacts_list = parse_contacts(contact_data)
            output_file_path = os.path.join(company_path, 'contacts.json')
            safe_dump_to_file(data=contacts_list, file_path=output_file_path)                                
                                
                                        
                
get_contacts()
