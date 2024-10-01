import pandas as pd

class PreprocessMergedData:
    def __init__(self, data=None):
        self.data = data
    
    def load_conll_skip_wrong(self, file_path):
        """
        Reads a CoNLL format file and loads it into a DataFrame with 'tokens' and 'labels' columns.
        
        :param file_path: Path to the CoNLL file.
        :return: DataFrame with 'tokens' and 'labels' columns.
        """
        data = []
        sentence = []
        labels = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == "":  # Sentence boundary
                    if sentence:  # Only append if the sentence list is not empty
                        data.append((sentence, labels))
                        sentence = []
                        labels = []
                else:
                    parts = line.split()
                    if len(parts) == 2:  # Ensure token and label are available
                        token, label = parts
                        sentence.append(token)
                        labels.append(label)
                    else:
                        print(f"Skipping line: {line}")  # Print problematic lines (for debugging)

            # Append the last sentence if the file doesn't end with a newline
            if sentence:
                data.append((sentence, labels))

        # Convert data to a DataFrame
        self.data = pd.DataFrame(data, columns=['tokens', 'labels'])
        return self.data
    
    def correct_ner_labels(self):
        """
        Corrects the NER labels in the 'labels' column of the dataframe.

        Returns:
        - A pandas DataFrame with corrected labels.
        """
        # Define a mapping for the label replacements
        label_replacements = {
            'I-PHONE': 'O',
            'OO': 'O',
            'B-PROD': 'B-PRODUCT',
            'I-Product': 'I-PRODUCT',
            'B-Product': 'B-PRODUCT'
        }
    
        # Function to replace labels and convert to uppercase
        def correct_labels(label_list):
            # Replace each label in the list and convert to uppercase
            return [label_replacements.get(label, label).upper() for label in label_list]
        
        # Apply the label correction to the 'labels' column
        self.data['labels'] = self.data['labels'].apply(correct_labels)  # Assumes 'labels' column is a list of labels
        
        return self.data

