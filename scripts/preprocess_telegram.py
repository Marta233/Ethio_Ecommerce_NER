import json
import pandas as pd
import re

class TelegramPreprocessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.data = pd.DataFrame()

    def load_data(self):
        """Load data from a JSON file and return a DataFrame."""
        data = []
        with open(self.input_file, 'r', encoding='utf-8') as file:
            for line in file:
                data.append(json.loads(line))
        
        self.data = pd.DataFrame(data)
        print(f"Loaded data shape: {self.data.shape}")
        print(f"Sample data:\n{self.data.head()}")

    def clean_text(self, text):
        """Remove emojis, English words, asterisks, and unwanted characters."""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )

        # Remove emojis and unwanted characters
        text = emoji_pattern.sub('', text)
        text = re.sub(r'[a-zA-Z]+', '', text)  # Remove English words
        text = re.sub(r'\*+', '', text)  # Remove asterisks
        text = re.sub(r'[^\wአ-ዜ\s]', '', text)  # Remove other unwanted characters
        
        cleaned_text = text.strip()
        print(f"Cleaned text: {cleaned_text}")
        return cleaned_text
    def remove_duplicates(self):
        """Remove duplicate text entries."""
        initial_shape = self.data.shape
        self.data.drop_duplicates(subset='text', inplace=True)
        final_shape = self.data.shape
        print(f"Removed {initial_shape[0] - final_shape[0]} duplicate rows. Dataset shape after deduplication: {final_shape}")

    def label_message_utf8_with_birr(self, message):
        """Label messages for product, price, and location."""
        if '\n' in message:
            first_line, remaining_message = message.split('\n', 1)
        else:
            first_line, remaining_message = message, ""

        labeled_tokens = []

        # Tokenize the first line
        first_line_tokens = re.findall(r'\S+', first_line)

        # Filter to keep only Amharic characters and numbers in the first line
        first_line_tokens = [token for token in first_line_tokens if re.match(r'^[\u1200-\u137F0-9]+$', token)]

        print(f"First line tokens: {first_line_tokens}")

        if first_line_tokens:
            labeled_tokens.append(f"{first_line_tokens[0]} B-PRODUCT")  # First token as B-PRODUCT
            for token in first_line_tokens[1:]:
                labeled_tokens.append(f"{token} I-PRODUCT")  # Remaining tokens as I-PRODUCT

        # Process the remaining message
        if remaining_message:
            lines = remaining_message.split('\n')
            for line in lines:
                tokens = re.findall(r'\S+', line)
                tokens = [token for token in tokens if re.match(r'^[\u1200-\u137F0-9]+$', token)]

                print(f"Tokens in remaining line: {tokens}")

                for token in tokens:
                    if re.match(r'^\d{10,}$', token):
                        labeled_tokens.append(f"{token} O")
                    elif re.match(r'^\d+(\.\d{1,2})?$|ETB|ዋጋ|\$|ብር', token):
                        labeled_tokens.append(f"{token} I-PRICE")
                    elif any(loc in token for loc in ['Addis Ababa', 'ለቡ', 'ለቡ መዳህኒዓለም', 'መገናኛ', 'ቦሌ', 'ሜክሲኮ']):
                        labeled_tokens.append(f"{token} I-LOC")
                    else:
                        labeled_tokens.append(f"{token} O")

        labeled_message = "\n".join(labeled_tokens)
        print(f"Labeled message:\n{labeled_message}")
        return labeled_message

    def process_data(self):
        """Load, clean, and label data."""
        self.load_data()

        print("Checking for NaN values in the 'text' column:")
        nan_count = self.data['text'].isnull().sum()
        print(f"Number of NaN values in 'text' column: {nan_count}")

        self.data = self.data.dropna(subset=['text'])
        print(f"Dataset shape after dropping NaN values in 'text' column: {self.data.shape}")

        # Clean the text
        self.data['text'] = self.data['text'].apply(self.clean_text)

        # Label the messages
        self.data['Labeled_Message'] = self.data['text'].apply(self.label_message_utf8_with_birr)

        # Display labeled messages
        print("Labeled messages:")
        print(self.data[['text', 'Labeled_Message']].head())
    def save_labeled_data(self):
        """Save the labeled data to the output file in CoNLL format."""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for index, row in self.data.iterrows():
                # Split the labeled message into tokens and labels
                tokens = row['Labeled_Message'].split('\n')
                for token_label in tokens:
                    if token_label.strip():  # Check for non-empty lines
                        f.write(f"{token_label}\n")  # Write each token and its label
                f.write("\n")  # Separate sentences by a blank line
        print(f"Labeled data saved to {self.output_file}")

