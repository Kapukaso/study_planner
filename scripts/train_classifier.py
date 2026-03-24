"""
Script to fine-tune DistilBERT for academic content classification.
Categories: concept, definition, formula, example, pyq, highlight, summary
"""
import os
import torch
import pandas as pd
import numpy as np
from datasets import load_dataset, Dataset, DatasetDict
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    TrainingArguments, 
    Trainer,
    DataCollatorWithPadding
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Configuration
MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "./models/academic_classifier"
CATEGORIES = ['concept', 'definition', 'formula', 'example', 'pyq', 'highlight', 'summary']
ID2LABEL = {i: label for i, label in enumerate(CATEGORIES)}
LABEL2ID = {label: i for i, label in enumerate(CATEGORIES)}

def prepare_data():
    """
    Load the collected dataset from data/train.csv.
    """
    if not os.path.exists("data/train.csv"):
        raise FileNotFoundError("Run scripts/collect_data.py first!")
        
    df = pd.read_csv("data/train.csv")
    
    # Ensure text is string and drop NaNs
    df['text'] = df['text'].astype(str)
    df = df.dropna(subset=['text'])
    
    dataset = Dataset.from_pandas(df)
    
    # Split into train/test
    return dataset.train_test_split(test_size=0.1)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
    acc = accuracy_score(labels, predictions)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def train():
    print("Loading datasets and tokenizer...")
    dataset_dict = prepare_data()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding=True)

    tokenized_datasets = dataset_dict.map(tokenize_function, batched=True)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    print("Initializing model...")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, 
        num_labels=len(CATEGORIES),
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        processing_class=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    print("Starting training...")
    trainer.train()
    
    print(f"Saving model to {OUTPUT_DIR}...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

if __name__ == "__main__":
    train()
