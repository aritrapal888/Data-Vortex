import os
import pandas as pd
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

INPUT_FILE = "round3/data/processed/platform_monetisation_reaction_final.csv"

MODEL_DIR = "round2/models/transformer_sentiment"

OUTPUT_FILE = "round3/data/processed/platform_monetisation_reaction_sentiment.csv"

print("=" * 70)
print("DATA VORTEX ROUND 3 - SENTIMENT ANALYSIS")
print("=" * 70)

# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("\nComments to analyze:", len(df))

# ---------------------------------------------------------
# Load Round 2 DistilBERT model
# ---------------------------------------------------------

print("\nLoading Round 2 DistilBERT model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_DIR
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_DIR
)

model.eval()

# ---------------------------------------------------------
# Label mapping
# ---------------------------------------------------------

id2label = model.config.id2label

print("\nModel labels:")
print(id2label)

# ---------------------------------------------------------
# Run inference
# ---------------------------------------------------------

texts = df["comment_text"].astype(str).tolist()

predicted_labels = []
confidence_scores = []

print("\nRunning sentiment inference...")

with torch.no_grad():

    for i, text in enumerate(texts):

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=128
        )

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

        confidence, prediction = torch.max(
            probabilities,
            dim=1
        )

        label_id = prediction.item()

        label = id2label[label_id]

        predicted_labels.append(label)
        confidence_scores.append(
            confidence.item()
        )

        print(
            f"[{i + 1:02d}/{len(texts)}] "
            f"{label:<10} "
            f"{confidence.item():.4f} | "
            f"{text[:70]}"
        )

# ---------------------------------------------------------
# Add predictions
# ---------------------------------------------------------

df["sentiment_label"] = predicted_labels
df["sentiment_confidence"] = confidence_scores

# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)
print("SENTIMENT DISTRIBUTION")
print("=" * 70)

print(
    df["sentiment_label"].value_counts()
)

print("\nAverage confidence:")
print(
    df["sentiment_confidence"].mean()
)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("SENTIMENT ANALYSIS COMPLETE")
print("=" * 70)