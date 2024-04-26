from os.path import join, dirname, abspath, exists
import os
import clipboard
from abstract_utilities import *
def await_copy(prompt):
    """ Wait for the clipboard content to change and return the new content. """
    print(prompt)
    clipboard.copy("null")
    spam = clipboard.paste()
    while True:
        if clipboard.paste() != spam:
            return clipboard.paste()

def write_to_file(contents, file_path):
    """ Write contents to a file at the specified path. """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(contents)

def safe_dump_to_file(data, file_path):
    """ Safely dump data to a file in JSON format. """
    import json
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def derive_email(first, last, email):
    """ Derive the email convention based on a first name, last name, and a sample email. """
    domain = email.split('@')[1]
    local_part = email.split('@')[0]
    pattern = ""
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
        pattern = "unknown"

    return pattern, domain

def get_email(first_name, last_name, pattern, domain):
    """ Generate an email based on the pattern and domain. """
    return f"{pattern.replace('{f}', first_name[0].lower()).replace('{l}', last_name.lower()).replace('{ff}', first_name.lower()).replace('{ll}', last_name[0].lower())}@{domain}"

def clean_text(text):
    """ Clean special characters from the text. """
    return text.replace('\u200b', '').replace("&amp;", "&").replace("&nbsp;", " ")

def make_email(first, last, domain):
    """Generate an email address using the first letter of the first name and the full last name."""
    return f"{first[0].lower()}{last.lower()}@{domain}"

def clean_text(text):
    """Clean special characters from the text."""
    return text.replace('\u200b', '').replace("&amp;", "&").replace("&nbsp;", " ")
def get_contacts():
    import os
    from os.path import join, abspath

    def get_abs_dir():
        """Return the absolute directory path of the current script."""
        return os.path.dirname(abspath(__file__))

    while True:
        # Simulate or replace `await_copy` with the actual function or logic to obtain data

        patterns={'patterns':[],'domains':[]}
        crunchbase_url = await_copy('Copy Crunchbase URL: ')
        company_name = crunchbase_url.split('/')[-1]
        folder_path = join(get_abs_dir(), company_name)
        os.makedirs(folder_path, exist_ok=True)
        content = await_copy('Copy Crunchbase contacts: ')
        contacts=parse_contacts(content)
        for i,each in enumerate(contacts):
            for j,email in enumerate(each['email']):
                contacts[i]['email'][j]=eatAll(email,['\t',' ','\n'])
                pattern, domain=derive_email(each['name'].split(' ')[0], each['name'].split(' ')[-1], eatAll(email,['\t',' ','\n']))              
                patterns['patterns'].append(pattern)
                patterns['domains'].append(domain)
        for i,each in enumerate(contacts):
            if each['email'] == []:
                for domain in patterns['domains']:
                    for pattern in patterns['patterns']:
                        contacts[i]['email'].append(get_email(each['name'].split(' ')[0], each['name'].split(' ')[-1], pattern, domain))
            contacts[i]['email']=list(set(contacts[i]['email'])) 
        safe_dump_to_file(data=contacts,file_path=os.path.join(folder_path,'contacts.json'))
def if_set(item):
    if isinstance(item,set or list or tuple):
        return item[-1]
    return item
def parse_contacts(content):
    """Parse contact information from the given content."""
    contacts=[]
    contacts_All=[]
    for contact_info in content.split('<contacts-card-row')[1:]:
            visible=1
            contacts.append([''])

            for char in contact_info:
                    
                    if visible%2==float(0) and char not in ['<','>']:
                            contacts[-1][-1]+=char 
                    contacts[-1][-1]=contacts[-1][-1].replace('\u200b','').replace("&amp;","&").replace("&nbsp;",',')
                    if char in ['<','>']:
                            visible +=1
                            if contacts[-1][-1] and contacts[-1][-1] != ' ':
                                    contacts[-1]+=' '
            for spec_char in ['',' ',',',' ,,']:
                    while spec_char in contacts[-1]:
                            contacts[-1].remove(spec_char)
            contact_js={'name':"","email":[]}
            for i,item in enumerate(contacts[-1]):
                  item = eatAll(item,['\t',' ','\n',''])
                  if 'found' not in item and 'View' not in item:
                          if i==0:
                                  contact_js['name']=item
                          elif '+1' in item:
                                  if 'phones' not in contact_js:
                                          contact_js['phones']=[]
                                  contact_js['phones'].append(item)
                          elif '@' in item:
                                  contact_js['email'].append(item)
                                  pattern, domain=derive_email(contact_js['name'].split(' ')[0], contact_js['name'].split(' ')[-1], item)
                          else:
                                  if 'title' not in contact_js:
                                          contact_js['title']=[]
                                  contact_js['title'].append(item)
                    
            contact_js['title']=' '.join(contact_js['title'])
            contacts[-1]=contact_js
    
    return contacts
import json
import csv

def json_to_csv(json_file_name, csv_file_path,file_paths):
    """
    Reads JSON files containing lists of dictionaries from multiple directories and writes the contents to a single CSV file.
    Each dictionary in the list becomes one row in the CSV.

    Parameters:
        json_file_name (str): The name of the JSON file to read in each directory.
        csv_file_path (str): The path to the CSV file to create and write.
    """

    
    # Prepare to write to the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        headers = ['name', 'email', 'title', 'phones']
        csv_writer.writerow(headers)  # Write the header row only once

        # Process each JSON file in the specified directories
        for file_path in file_paths:
            json_path = join(file_path, json_file_name)
            if not os.path.exists(json_path):
                print(f"File not found: {json_path}")
                continue  # Skip this file path if the JSON file does not exist
            
            with open(json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Write data rows for this JSON file
            for item in data:
                name = item.get('name', '')
                email = ', '.join(item.get('email', []))  # Join all emails into a single string separated by commas
                title = item.get('title', '').replace('Non-Management', '').replace('Executive Management', '').replace('Showing 3 of 3', '').strip()
                phones = ', '.join(item.get('phones', []))  # Join all phones into a single string separated by commas
                csv_writer.writerow([name, email, title, phones])

# Example usage
file_paths = []
for folder in os.listdir(os.getcwd()):
    file_paths.append(os.path.join(os.getcwd(),folder))
json_file_name = 'contacts.json'  # Name of the JSON file in each directory
csv_file_path = '/home/gamook/Documents/catalyst/solar/contacts.csv'  # Path to the output CSV file
json_to_csv(json_file_name, csv_file_path,file_paths)

    
def main():
    print("Starting contact information retrieval...")

    while True:
        get_contacts()

if __name__ == "__main__":
    main()
