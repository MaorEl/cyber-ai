import re
import json
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure nltk resources are downloaded
nltk.download('stopwords')
nltk.download('wordnet')

def remove_attachment_text(text):
    # Split the text at the specific phrase
    parts = text.split("Content-Disposition: attachment;")
    # Return the part before the phrase if it exists
    if parts:
        return parts[0]

    else:
        return text

def parse_contacts(data):
    # count the number of '~' in the data to check if its notes
    count = data.count('~')
    if count < 30:
        return data

    # Normalize the data by removing line continuation characters
    data = data.replace("=\n", " ")  # Assumes `=` at the end of the line followed by a newline

    # Split the data into individual records on '#'
    records = data.split('#')

    # Initialize a list to store parsed contacts
    contacts = []

    # Iterate through each record
    for record in records:
        # Split the record into fields using '~'
        fields = record.split('~')

        # TODO: need to check relevant fields
        if len(fields) > 21:  # Check to ensure it's a valid record
            contact = {
                'first_name': fields[1].strip(),
                'last_name': fields[3].strip(),
                'phone_numbers': fields[11:14],
                'position': fields[15].strip(),
                'company': fields[18].strip(),
                'email': fields[21].strip() if len(fields) > 21 else None  # Safeguard for missing email
            }
            contacts.append(contact)
            # print('contact:', contact)

    if not contacts:
        return ' '
    return json.dumps(contacts)


def remove_substring(text, start, end):
    # Regex pattern to match a substring that starts with 'X-d' and ends with 'subject'
    pattern = rf'{start}.*?{end}'
    # Replace the matching substring with an empty string
    cleaned_text = re.sub(pattern, ' ', text, flags=re.DOTALL)
    return cleaned_text

# remove foward text
def remove_foward_text(text: str):
    text = text.replace('FW:', ' ')
    text = text.replace('RE:', ' ')
    text = remove_substring(text, '----------- Forwarded', 'Subject')
    text = text.replace('-', ' ')
    text = text.replace('\\n', ' ')
    text = text.replace(':', ' ')
    return text
    
def remove_email_headers(text):
    # Remove email headers and any non-alphabetic characters
    text = re.sub(r'\b(email|subject|sent|from|to|message|original|pm)\b', '', text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    return text

def tokenize_and_lemmatize(text):
    
    remove_words = ['please', 'com', 'would', 'said', 'new', 'smith', 'thanks', 'use', 'also', 'know', 'original', 'email', 'california']
    
    # if text is None, return an empty list
    if text is None:
        return ''
    
    # if text epmty, return an empty list
    if text == '':
        return ''

    # Tokenize the text by splitting on whitespace
    tokens = text.split()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and word not in remove_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return ' '.join(tokens)

def remove_small_words(text, min_length=3):
    # Tokenize the text by splitting on whitespace
    tokens = text.split()
    # Remove words that are less than `min_length` characters
    tokens = [word for word in tokens if len(word) >= min_length]
    return ' '.join(tokens)


def data_cleaning(enron_df: pd.DataFrame, lemmatize: bool = True):
    enron_df['email_text'] = enron_df['email_text'].apply(remove_attachment_text)
    print('removed attachments')

    enron_df['email_text'] = enron_df['email_text'].apply(parse_contacts)
    print('parsed contacts')

    enron_df['email_text'] = enron_df['email_text'].apply(remove_foward_text)
    print('removed foward text')

    enron_df['email_text'].fillna(' ', inplace=True)
    print('filled nan values')

    enron_df['email_text'] = enron_df['email_text'].apply(remove_email_headers)
    print('removed email headers')

    enron_df['email_text'] = enron_df['email_text'].apply(remove_small_words)
    print('removed small words')

    if lemmatize:
        enron_df['email_text'] = enron_df['email_text'].apply(tokenize_and_lemmatize)
        print('lemmatized')


def preprocess_text(text, should_remove_small_words=False, lemmatize=False):
    text = remove_attachment_text(text)
    text = parse_contacts(text)
    text = remove_foward_text(text)
    text = remove_email_headers(text)
    if should_remove_small_words:
        text = remove_small_words(text)
    if lemmatize:
        text = tokenize_and_lemmatize(text)
    
    return text



