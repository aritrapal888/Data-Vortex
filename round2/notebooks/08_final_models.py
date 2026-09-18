import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRAIN_PATH = os.path.join(BASE_DIR, "data", "train.csv")
TEST_PATH = os.path.join(BASE_DIR, "data", "test.csv")

REPORT_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "final_topic")

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

X_train_text = train_df["post_text"].astype(str)
X_test_text = test_df["post_text"].astype(str)

y_train = train_df["topic_category"]
y_test = test_df["topic_category"]


# ============================================================
# TF-IDF FEATURES
# ============================================================

print("=" * 70)
print("DATA VORTEX A'26 — FINAL TOPIC MODEL")
print("=" * 70)

print("\nCreating word TF-IDF...")

word_vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    max_features=100000,
    sublinear_tf=True,
)

X_train_word = word_vectorizer.fit_transform(X_train_text)
X_test_word = word_vectorizer.transform(X_test_text)


print("Creating character TF-IDF...")

char_vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 6),
    max_features=100000,
    sublinear_tf=True,
)

X_train_char = char_vectorizer.fit_transform(X_train_text)
X_test_char = char_vectorizer.transform(X_test_text)


X_train = hstack(
    [X_train_word, X_train_char]
).tocsr()

X_test = hstack(
    [X_test_word, X_test_char]
).tocsr()

print("\nCombined feature matrix:")
print("Train:", X_train.shape)
print("Test :", X_test.shape)


# ============================================================
# FINAL TOPIC MODEL
# ============================================================

print("\nTraining final Topic Linear SVM...")

topic_model = LinearSVC(
    C=2.0,
    class_weight="balanced",
    max_iter=10000,
)

topic_model.fit(X_train, y_train)

topic_predictions = topic_model.predict(X_test)


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    topic_predictions,
)

macro_precision = precision_score(
    y_test,
    topic_predictions,
    average="macro",
    zero_division=0,
)

macro_recall = recall_score(
    y_test,
    topic_predictions,
    average="macro",
    zero_division=0,
)

macro_f1 = f1_score(
    y_test,
    topic_predictions,
    average="macro",
    zero_division=0,
)

weighted_f1 = f1_score(
    y_test,
    topic_predictions,
    average="weighted",
    zero_division=0,
)


print("\n" + "=" * 70)
print("FINAL TOPIC MODEL RESULTS")
print("=" * 70)

print(f"Accuracy        : {accuracy:.4f}")
print(f"Macro Precision : {macro_precision:.4f}")
print(f"Macro Recall    : {macro_recall:.4f}")
print(f"Macro F1        : {macro_f1:.4f}")
print(f"Weighted F1     : {weighted_f1:.4f}")


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    y_test,
    topic_predictions,
    digits=4,
    zero_division=0,
)

print("\nCLASSIFICATION REPORT")
print("-" * 70)
print(report)


# ============================================================
# CONFUSION MATRIX
# ============================================================

labels = sorted(y_test.unique())

cm = confusion_matrix(
    y_test,
    topic_predictions,
    labels=labels,
)

print("\nCONFUSION MATRIX")
print("-" * 70)
print(cm)


# ============================================================
# SAVE CONFUSION MATRIX IMAGE
# ============================================================

fig, ax = plt.subplots(figsize=(8, 7))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels,
)

disp.plot(
    ax=ax,
    xticks_rotation=45,
    values_format="d",
)

ax.set_title("Final Topic Classification — Confusion Matrix")

plt.tight_layout()

cm_path = os.path.join(
    OUTPUT_DIR,
    "topic_confusion_matrix.png",
)

plt.savefig(
    cm_path,
    dpi=300,
    bbox_inches="tight",
)

plt.close()


# ============================================================
# SAVE CONFUSION MATRIX CSV
# ============================================================

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels,
)

cm_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "topic_confusion_matrix.csv",
    )
)


# ============================================================
# SAVE METRICS REPORT
# ============================================================

report_path = os.path.join(
    REPORT_DIR,
    "final_topic_evaluation.txt",
)

with open(
    report_path,
    "w",
    encoding="utf-8",
) as f:

    f.write("DATA VORTEX A'26 — FINAL TOPIC MODEL\n")
    f.write("=" * 70 + "\n\n")

    f.write("Model: Linear SVM\n")
    f.write("C: 2.0\n")
    f.write("Class Weight: balanced\n")
    f.write("Word TF-IDF: 1-3 grams, max 100000 features\n")
    f.write("Character TF-IDF: 3-6 grams, max 100000 features\n")
    f.write(f"Training samples: {len(train_df)}\n")
    f.write(f"Testing samples: {len(test_df)}\n\n")

    f.write("EVALUATION METRICS\n")
    f.write("-" * 70 + "\n")

    f.write(f"Accuracy: {accuracy:.4f}\n")
    f.write(f"Macro Precision: {macro_precision:.4f}\n")
    f.write(f"Macro Recall: {macro_recall:.4f}\n")
    f.write(f"Macro F1: {macro_f1:.4f}\n")
    f.write(f"Weighted F1: {weighted_f1:.4f}\n\n")

    f.write("CLASSIFICATION REPORT\n")
    f.write("-" * 70 + "\n")
    f.write(report)

    f.write("\nCONFUSION MATRIX\n")
    f.write("-" * 70 + "\n")
    f.write(str(cm))


print("\nSaved confusion matrix:")
print(cm_path)

print("\nSaved evaluation report:")
print(report_path)

print("\n" + "=" * 70)
print("FINAL TOPIC MODEL COMPLETE")
print("=" * 70)