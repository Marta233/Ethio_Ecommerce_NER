Fine-Tune the Model for NER: Entity Labeling and CoNLL Format Generation
This repository is developed collaboratively by Getahun Tiruneh and Marta Assefa to create tools for dynamic entity labeling of Amharic messages and generate CoNLL formatted outputs. It is designed for processing data fetched from the Qenash.com - ቅናሽ e-commerce channel, specifically targeting price, location, and product entities. The repository allows for dynamic batching of messages for labeling and exporting labeled data in the CoNLL format.

Table of Contents
Features
Installation
Usage
Entity Labeling
Generate CoNLL Output
Dynamic Batching
Fine-Tune the Model for NER
File Structure
Contributing
License
Features
Entity Labeling: Automatically labels entities such as prices, locations, and products in Amharic messages.
CoNLL Format Generation: Produces output in the standard CoNLL format for NLP tasks.
Dynamic Batching: Allows flexible generation of labeled data from custom message ranges (e.g., 0-50, 51-100, etc.).
Amharic Language Support: Handles Amharic text preprocessing, including the removal of emojis, special characters, and punctuation.
Installation
To get started, clone this repository to your local machine:

bash
Copy code
git clone https://github.com/getahunTiruneh/Ethio-Mart-Collaboration.git
cd Ethio-Mart-Collaboration 
Usage
Entity Labeling
The entity labeling feature tags tokens in Amharic messages as belonging to one of the following categories:

B-PRICE / I-PRICE: Price-related entities.
B-LOC / I-LOC: Location-related entities.
B-PRODUCT / I-PRODUCT: Product-related entities.
O: Outside any entity.
Here’s how you can label entities in a sample message:

python
Copy code
from entity_labeler import EntityLabeler

# Initialize the entity labeler
labeler = EntityLabeler()

# Sample message
message = "ብር 500 ዋጋ በመገናኛ ምርት"

# Label entities
labeled_entities = labeler.label_entities(message)
print(labeled_entities)
Fine-Tune the Model for NER
To fine-tune the NER model using the labeled data, follow these steps:

Prepare the Dataset: Ensure the labeled data is in CoNLL format.
Load the Model: Use a pre-trained transformer model suitable for NER tasks.
Set Up Training Parameters: Specify the learning rate, batch size, and the number of epochs.
Train the Model: Implement training using the Hugging Face Trainer API.
Here's a sample code snippet for fine-tuning:

python
Copy code
from transformers import Trainer, TrainingArguments, XLMRobertaForTokenClassification

# Load the pre-trained model
model = XLMRobertaForTokenClassification.from_pretrained('xlm-roberta-base', num_labels=num_labels)

# Set up training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_steps=10_000,
    save_total_limit=2,
)

# Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Fine-tune the model
trainer.train()
Data Source
The data processed in this repository is fetched from the Qenash.com - ቅናሽ e-commerce channel. This platform provides a variety of e-commerce data, and we focus on labeling entities related to prices, locations, and products from these messages.

Contributing
This project is collaboratively developed by Getahun Tiruneh and Marta Assefa. If you'd like to contribute, feel free to submit issues or pull requests for any improvements or feature requests.

