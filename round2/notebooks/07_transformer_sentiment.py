import os
import numpy as np
import pandas as pd
import torch

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRAIN_PATH = os.path.join(BASE_DIR, "data", "train.csv")
TEST_PATH = os.path.join(BASE_DIR, "data", "test.csv")

MODEL_DIR = os.path.join(BASE_DIR, "models", "transformer_sentiment")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "transformer_sentiment")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print("Train rows:", len(train_df))
print("Test rows:", len(test_df))


# ============================================================
# 3. ENCODE SENTIMENT LABELS
# ============================================================

label_names = ["Negative", "Neutral", "Positive"]

label2id = {
    "Negative": 0,
    "Neutral": 1,
    "Positive": 2,
}

id2label = {
    0: "Negative",
    1: "Neutral",
    2: "Positive",
}

train_df["label"] = train_df["sentiment_label"].map(label2id)
test_df["label"] = test_df["sentiment_label"].map(label2id)


# ============================================================
# 4. KEEP ONLY REQUIRED COLUMNS
# ============================================================

train_df = train_df[["post_text", "label"]]
test_df = test_df[["post_text", "label"]]

train_df["post_text"] = train_df["post_text"].astype(str)
test_df["post_text"] = test_df["post_text"].astype(str)


# ============================================================
# 5. CONVERT TO HUGGING FACE DATASETS
# ============================================================

train_dataset = Dataset.from_pandas(train_df, preserve_index=False)
test_dataset = Dataset.from_pandas(test_df, preserve_index=False)


# ============================================================
# 6. TOKENIZER
# ============================================================

MODEL_NAME = "distilbert-base-uncased"

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize_function(examples):
    return tokenizer(
        examples["post_text"],
        truncation=True,
        padding="max_length",
        max_length=128,
    )


print("Tokenizing...")

train_dataset = train_dataset.map(
    tokenize_function,
    batched=True,
)

test_dataset = test_dataset.map(
    tokenize_function,
    batched=True,
)

train_dataset = train_dataset.remove_columns(["post_text"])
test_dataset = test_dataset.remove_columns(["post_text"])

train_dataset.set_format("torch")
test_dataset.set_format("torch")


# ============================================================
# 7. LOAD MODEL
# ============================================================

print("\nLoading DistilBERT model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3,
    id2label=id2label,
    label2id=label2id,
)


# ============================================================
# 8. EVALUATION METRICS
# ============================================================

def compute_metrics(eval_pred):

    predictions, labels = eval_pred

    predictions = np.argmax(predictions, axis=1)

    accuracy = accuracy_score(labels, predictions)

    macro_f1 = f1_score(
        labels,
        predictions,
        average="macro",
    )

    weighted_f1 = f1_score(
        labels,
        predictions,
        average="weighted",
    )

    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
    }


# ============================================================
# 9. TRAINING CONFIGURATION
# ============================================================

training_args = TrainingArguments(
    output_dir=MODEL_DIR,

    num_train_epochs=2,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    learning_rate=2e-5,

    weight_decay=0.01,

    eval_strategy="epoch",
    save_strategy="epoch",

    load_best_model_at_end=True,
    metric_for_best_model="macro_f1",
    greater_is_better=True,

    logging_steps=100,

    report_to="none",

    save_total_limit=1,
)


# ============================================================
# 10. TRAINER
# ============================================================

trainer = Trainer(
    model=model,
    args=training_args,

    train_dataset=train_dataset,
    eval_dataset=test_dataset,

    processing_class=tokenizer,

    compute_metrics=compute_metrics,
)


# ============================================================
# 11. TRAIN
# ============================================================

print("\n" + "=" * 60)
print("STARTING DISTILBERT TRAINING")
print("=" * 60)

trainer.train()


# ============================================================
# 12. EVALUATION
# ============================================================

print("\n" + "=" * 60)
print("EVALUATING MODEL")
print("=" * 60)

results = trainer.evaluate()

print("\nEvaluation Results:")

for key, value in results.items():
    if isinstance(value, float):
        print(f"{key}: {value:.4f}")
    else:
        print(f"{key}: {value}")


# ============================================================
# 13. DETAILED PREDICTIONS
# ============================================================

predictions = trainer.predict(test_dataset)

predicted_labels = np.argmax(
    predictions.predictions,
    axis=1,
)

true_labels = predictions.label_ids


# ============================================================
# 14. CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    true_labels,
    predicted_labels,
    target_names=label_names,
    digits=4,
)

print("\nClassification Report:")
print(report)


# ============================================================
# 15. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    true_labels,
    predicted_labels,
)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# 16. SAVE REPORT
# ============================================================

report_path = os.path.join(
    OUTPUT_DIR,
    "transformer_sentiment_report.txt",
)

with open(report_path, "w", encoding="utf-8") as f:

    f.write("DISTILBERT SENTIMENT MODEL\n")
    f.write("=" * 60 + "\n\n")

    f.write(f"Model: {MODEL_NAME}\n")
    f.write(f"Training rows: {len(train_df)}\n")
    f.write(f"Testing rows: {len(test_df)}\n")
    f.write("Epochs: 2\n")
    f.write("Learning rate: 2e-5\n")
    f.write("Batch size: 8\n\n")

    f.write("EVALUATION METRICS\n")
    f.write("-" * 60 + "\n")

    for key, value in results.items():
        if isinstance(value, float):
            f.write(f"{key}: {value:.4f}\n")

    f.write("\nCLASSIFICATION REPORT\n")
    f.write("-" * 60 + "\n")
    f.write(report)

    f.write("\n\nCONFUSION MATRIX\n")
    f.write("-" * 60 + "\n")
    f.write(str(cm))


# ============================================================
# 17. SAVE CONFUSION MATRIX CSV
# ============================================================

cm_df = pd.DataFrame(
    cm,
    index=label_names,
    columns=label_names,
)

cm_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "confusion_matrix.csv",
    )
)


# ============================================================
# 18. SAVE MODEL
# ============================================================

print("\nSaving trained model...")

trainer.save_model(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)


print("\n" + "=" * 60)
print("TRANSFORMER EXPERIMENT COMPLETE")
print("=" * 60)

print("\nModel saved to:")
print(MODEL_DIR)

print("\nReport saved to:")
print(report_path)