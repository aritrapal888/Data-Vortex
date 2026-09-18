import os
import joblib
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
from scipy.sparse import hstack
import matplotlib.pyplot as plt


print("=" * 70)
print("DATA VORTEX A'26 — FINAL TOPIC MODEL")
print("=" * 70)


# ================================================================
# PATHS
# ================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRAIN_PATH = os.path.join(
    BASE_DIR,
    "data",
    "train.csv"
)

TEST_PATH = os.path.join(
    BASE_DIR,
    "data",
    "test.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "final_topic"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


# ================================================================
# LOAD DATA
# ================================================================

print("\nLoading train and test data...")

train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)

X_train_text = train["post_text"].fillna("")
X_test_text = test["post_text"].fillna("")

y_train = train["topic_category"]
y_test = test["topic_category"]

print(f"Training rows: {len(train)}")
print(f"Testing rows : {len(test)}")


# ================================================================
# WORD TF-IDF
# ================================================================

print("\nCreating word TF-IDF...")

word_vectorizer = TfidfVectorizer(
    analyzer="word",
    ngram_range=(1, 2),
    max_features=75000,
    sublinear_tf=True
)

X_train_word = word_vectorizer.fit_transform(
    X_train_text
)

X_test_word = word_vectorizer.transform(
    X_test_text
)

print("Word features:")
print("Train:", X_train_word.shape)
print("Test :", X_test_word.shape)


# ================================================================
# CHARACTER TF-IDF
# ================================================================

print("\nCreating character TF-IDF...")

char_vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    max_features=75000,
    sublinear_tf=True
)

X_train_char = char_vectorizer.fit_transform(
    X_train_text
)

X_test_char = char_vectorizer.transform(
    X_test_text
)

print("Character features:")
print("Train:", X_train_char.shape)
print("Test :", X_test_char.shape)


# ================================================================
# COMBINE FEATURES
# ================================================================

X_train = hstack([
    X_train_word,
    X_train_char
])

X_test = hstack([
    X_test_word,
    X_test_char
])

print("\nCombined feature matrix:")
print("Train:", X_train.shape)
print("Test :", X_test.shape)


# ================================================================
# FINAL TOPIC MODEL
# ================================================================

print("\nTraining final Topic Enhanced Logistic Regression...")

model = LogisticRegression(
    C=1.0,
    class_weight="balanced",
    max_iter=3000,
    solver="lbfgs",
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# ================================================================
# SAVE COMPLETE TRAINED MODEL PACKAGE
# ================================================================

print("\nSaving complete trained model package...")

model_package = {
    "model": model,
    "word_vectorizer": word_vectorizer,
    "char_vectorizer": char_vectorizer,
    "labels": list(model.classes_),
    "model_name": "Enhanced Logistic Regression",
    "task": "Topic Classification",
    "word_ngram_range": (1, 2),
    "word_max_features": 75000,
    "char_ngram_range": (3, 5),
    "char_max_features": 75000,
    "class_weight": "balanced",
    "C": 1.0,
    "solver": "lbfgs",
    "max_iter": 3000
}

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "final_topic_logistic_regression.pkl"
)

joblib.dump(
    model_package,
    MODEL_PATH,
    compress=3
)

print("\nSaved trained model:")
print(MODEL_PATH)


# ================================================================
# PREDICTION
# ================================================================

print("\nGenerating test predictions...")

y_pred = model.predict(
    X_test
)


# ================================================================
# EVALUATION METRICS
# ================================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

macro_precision = precision_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

macro_recall = recall_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

macro_f1 = f1_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)

weighted_f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


# ================================================================
# RESULTS
# ================================================================

print("\n" + "=" * 70)
print("FINAL TOPIC MODEL RESULTS")
print("=" * 70)

print(f"Accuracy        : {accuracy:.4f}")
print(f"Macro Precision : {macro_precision:.4f}")
print(f"Macro Recall    : {macro_recall:.4f}")
print(f"Macro F1        : {macro_f1:.4f}")
print(f"Weighted F1     : {weighted_f1:.4f}")


# ================================================================
# CLASSIFICATION REPORT
# ================================================================

print("\nCLASSIFICATION REPORT")
print("-" * 70)

report = classification_report(
    y_test,
    y_pred,
    zero_division=0
)

print(report)


# ================================================================
# CONFUSION MATRIX
# ================================================================

print("\nCONFUSION MATRIX")
print("-" * 70)

labels = sorted(
    y_test.unique()
)

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print(cm)


# ================================================================
# SAVE CONFUSION MATRIX CSV
# ================================================================

cm_df = pd.DataFrame(
    cm,
    index=labels,
    columns=labels
)

cm_csv_path = os.path.join(
    OUTPUT_DIR,
    "topic_confusion_matrix.csv"
)

cm_df.to_csv(
    cm_csv_path
)


# ================================================================
# SAVE CONFUSION MATRIX PNG
# ================================================================

plt.figure(figsize=(8, 6))

plt.imshow(
    cm,
    interpolation="nearest"
)

plt.title(
    "Final Topic Model — Confusion Matrix"
)

plt.colorbar()

tick_marks = np.arange(
    len(labels)
)

plt.xticks(
    tick_marks,
    labels,
    rotation=45,
    ha="right"
)

plt.yticks(
    tick_marks,
    labels
)

threshold = cm.max() / 2

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):

        plt.text(
            j,
            i,
            format(cm[i, j], "d"),
            horizontalalignment="center",
            color="white" if cm[i, j] > threshold else "black"
        )

plt.ylabel(
    "True Label"
)

plt.xlabel(
    "Predicted Label"
)

plt.tight_layout()

cm_png_path = os.path.join(
    OUTPUT_DIR,
    "topic_confusion_matrix.png"
)

plt.savefig(
    cm_png_path,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ================================================================
# SAVE EVALUATION REPORT
# ================================================================

evaluation_path = os.path.join(
    REPORT_DIR,
    "final_topic_evaluation.txt"
)

with open(
    evaluation_path,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "DATA VORTEX A'26 — FINAL TOPIC MODEL EVALUATION\n"
    )

    f.write(
        "=" * 70 + "\n\n"
    )

    f.write(
        "Model: Enhanced Logistic Regression\n"
    )

    f.write(
        "Features: Word TF-IDF (1-2 grams) + Character TF-IDF (3-5 grams)\n"
    )

    f.write(
        "Word TF-IDF maximum features: 75,000\n"
    )

    f.write(
        "Character TF-IDF maximum features: 75,000\n"
    )

    f.write(
        "Class weighting: balanced\n"
    )

    f.write(
        "C: 1.0\n"
    )

    f.write(
        "Solver: lbfgs\n"
    )

    f.write(
        "Maximum iterations: 3000\n\n"
    )

    f.write(
        "Evaluation Metrics\n"
    )

    f.write(
        "-" * 70 + "\n"
    )

    f.write(
        f"Accuracy        : {accuracy:.4f}\n"
    )

    f.write(
        f"Macro Precision : {macro_precision:.4f}\n"
    )

    f.write(
        f"Macro Recall    : {macro_recall:.4f}\n"
    )

    f.write(
        f"Macro F1        : {macro_f1:.4f}\n"
    )

    f.write(
        f"Weighted F1     : {weighted_f1:.4f}\n\n"
    )

    f.write(
        "Classification Report\n"
    )

    f.write(
        "-" * 70 + "\n"
    )

    f.write(
        report
    )

    f.write(
        "\n\nConfusion Matrix\n"
    )

    f.write(
        "-" * 70 + "\n"
    )

    f.write(
        str(cm)
    )


# ================================================================
# FINAL OUTPUT
# ================================================================

print("\nSaved confusion matrix CSV:")
print(cm_csv_path)

print("\nSaved confusion matrix image:")
print(cm_png_path)

print("\nSaved evaluation report:")
print(evaluation_path)

print("\n" + "=" * 70)
print("FINAL TOPIC MODEL COMPLETE")
print("=" * 70)