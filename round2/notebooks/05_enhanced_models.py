import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ============================================================
# DATA VORTEX A'26 — ROUND 2
# ENHANCED NLP EXPERIMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "data" / "train.csv"
TEST_PATH = BASE_DIR / "data" / "test.csv"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

FIGURE_DIR = OUTPUT_DIR / "enhanced_confusion_matrices"
FIGURE_DIR.mkdir(exist_ok=True)

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("DATA VORTEX A'26 — ENHANCED NLP EXPERIMENT")
print("=" * 70)

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

X_train_text = train_df["post_text"].astype(str)
X_test_text = test_df["post_text"].astype(str)

# ------------------------------------------------------------
# Word TF-IDF
# ------------------------------------------------------------

print("\n[1] WORD TF-IDF")
print("-" * 50)

word_vectorizer = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    max_features=75000
)

X_train_word = word_vectorizer.fit_transform(X_train_text)
X_test_word = word_vectorizer.transform(X_test_text)

print("Training shape:", X_train_word.shape)
print("Testing shape :", X_test_word.shape)

# ------------------------------------------------------------
# Character TF-IDF
# ------------------------------------------------------------

print("\n[2] CHARACTER TF-IDF")
print("-" * 50)

char_vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    min_df=2,
    max_features=75000,
    sublinear_tf=True
)

X_train_char = char_vectorizer.fit_transform(X_train_text)
X_test_char = char_vectorizer.transform(X_test_text)

print("Training shape:", X_train_char.shape)
print("Testing shape :", X_test_char.shape)

# ------------------------------------------------------------
# Combine word + character features
# ------------------------------------------------------------

from scipy.sparse import hstack

X_train_combined = hstack([
    X_train_word,
    X_train_char
])

X_test_combined = hstack([
    X_test_word,
    X_test_char
])

print("\n[3] COMBINED FEATURES")
print("-" * 50)

print("Training shape:", X_train_combined.shape)
print("Testing shape :", X_test_combined.shape)

# ------------------------------------------------------------
# Evaluation
# ------------------------------------------------------------

def evaluate(
    target_name,
    y_train,
    y_test,
    Xtr,
    Xte,
    class_weight
):

    print("\n")
    print("=" * 70)
    print(f"{target_name.upper()} — ENHANCED MODELS")
    print("=" * 70)

    models = {

        "Enhanced_Logistic_Regression": LogisticRegression(
            C=2.0,
            max_iter=3000,
            class_weight=class_weight,
            random_state=42
        ),

        "Enhanced_Linear_SVM": LinearSVC(
            C=1.0,
            class_weight=class_weight,
            random_state=42
        )
    }

    results = []

    for name, model in models.items():

        print("\n" + "-" * 70)
        print(name)
        print("-" * 70)

        model.fit(Xtr, y_train)

        pred = model.predict(Xte)

        accuracy = accuracy_score(
            y_test,
            pred
        )

        precision, recall, f1, _ = (
            precision_recall_fscore_support(
                y_test,
                pred,
                average="macro",
                zero_division=0
            )
        )

        weighted_f1 = (
            precision_recall_fscore_support(
                y_test,
                pred,
                average="weighted",
                zero_division=0
            )[2]
        )

        print(f"Accuracy        : {accuracy:.4f}")
        print(f"Macro Precision : {precision:.4f}")
        print(f"Macro Recall    : {recall:.4f}")
        print(f"Macro F1        : {f1:.4f}")
        print(f"Weighted F1     : {weighted_f1:.4f}")

        print("\nClassification Report:")
        print(
            classification_report(
                y_test,
                pred,
                digits=4,
                zero_division=0
            )
        )

        # Confusion matrix

        labels = sorted(pd.Series(y_test).unique())

        cm = confusion_matrix(
            y_test,
            pred,
            labels=labels
        )

        fig, ax = plt.subplots(figsize=(7, 6))

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=labels
        )

        disp.plot(
            ax=ax,
            values_format="d",
            xticks_rotation=30
        )

        plt.title(
            f"{target_name} — {name}"
        )

        plt.tight_layout()

        fig_path = (
            FIGURE_DIR /
            f"{target_name}_{name}.png"
        )

        plt.savefig(
            fig_path,
            dpi=200,
            bbox_inches="tight"
        )

        plt.close()

        results.append({
            "target": target_name,
            "model": name,
            "class_weight": str(class_weight),
            "accuracy": accuracy,
            "macro_precision": precision,
            "macro_recall": recall,
            "macro_f1": f1,
            "weighted_f1": weighted_f1
        })

    return results


# ------------------------------------------------------------
# Sentiment
# ------------------------------------------------------------

sentiment_results = evaluate(
    "Sentiment",
    train_df["sentiment_label"],
    test_df["sentiment_label"],
    X_train_combined,
    X_test_combined,
    None
)

# ------------------------------------------------------------
# Topic — class weighted
# ------------------------------------------------------------

topic_results = evaluate(
    "Topic",
    train_df["topic_category"],
    test_df["topic_category"],
    X_train_combined,
    X_test_combined,
    "balanced"
)

# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

results = pd.DataFrame(
    sentiment_results + topic_results
)

path = REPORT_DIR / "enhanced_model_comparison.csv"

results.to_csv(
    path,
    index=False
)

print("\n")
print("=" * 70)
print("ENHANCED MODEL COMPARISON")
print("=" * 70)

print(
    results[
        [
            "target",
            "model",
            "accuracy",
            "macro_precision",
            "macro_recall",
            "macro_f1",
            "weighted_f1"
        ]
    ].to_string(index=False)
)

print("\nResults saved to:")
print(path)

print("\n" + "=" * 70)
print("EXPERIMENT COMPLETE")
print("=" * 70)