import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support
)

from scipy.sparse import hstack


# ============================================================
# DATA VORTEX A'26 — ROUND 2
# HYPERPARAMETER TUNING
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "data" / "train.csv"
TEST_PATH = BASE_DIR / "data" / "test.csv"

REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)


print("=" * 70)
print("DATA VORTEX A'26 — HYPERPARAMETER EXPERIMENT")
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

print("\nCreating word TF-IDF...")

word_vectorizer = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    ngram_range=(1, 3),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    max_features=100000
)

X_train_word = word_vectorizer.fit_transform(X_train_text)
X_test_word = word_vectorizer.transform(X_test_text)


# ------------------------------------------------------------
# Character TF-IDF
# ------------------------------------------------------------

print("Creating character TF-IDF...")

char_vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 6),
    min_df=2,
    max_features=100000,
    sublinear_tf=True
)

X_train_char = char_vectorizer.fit_transform(X_train_text)
X_test_char = char_vectorizer.transform(X_test_text)


# ------------------------------------------------------------
# Combine
# ------------------------------------------------------------

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


# ============================================================
# Evaluation function
# ============================================================

def evaluate(
    model,
    Xtr,
    Xte,
    ytr,
    yte
):

    model.fit(Xtr, ytr)

    pred = model.predict(Xte)

    accuracy = accuracy_score(
        yte,
        pred
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            yte,
            pred,
            average="macro",
            zero_division=0
        )
    )

    weighted_f1 = (
        precision_recall_fscore_support(
            yte,
            pred,
            average="weighted",
            zero_division=0
        )[2]
    )

    return {
        "accuracy": accuracy,
        "macro_precision": precision,
        "macro_recall": recall,
        "macro_f1": f1,
        "weighted_f1": weighted_f1
    }


# ============================================================
# SENTIMENT TUNING
# ============================================================

print("\n")
print("=" * 70)
print("SENTIMENT HYPERPARAMETER SEARCH")
print("=" * 70)

sentiment_results = []

for C in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:

    print(f"\nTesting Logistic Regression C={C}")

    model = LogisticRegression(
        C=C,
        max_iter=4000,
        random_state=42
    )

    metrics = evaluate(
        model,
        X_train,
        X_test,
        train_df["sentiment_label"],
        test_df["sentiment_label"]
    )

    sentiment_results.append({
        "target": "Sentiment",
        "model": "LogisticRegression",
        "C": C,
        **metrics
    })

    print(
        f"Accuracy={metrics['accuracy']:.4f} | "
        f"Macro F1={metrics['macro_f1']:.4f}"
    )


# ------------------------------------------------------------
# Sentiment SVM
# ------------------------------------------------------------

for C in [0.25, 0.5, 1.0, 2.0, 4.0]:

    print(f"\nTesting Linear SVM C={C}")

    model = LinearSVC(
        C=C,
        random_state=42
    )

    metrics = evaluate(
        model,
        X_train,
        X_test,
        train_df["sentiment_label"],
        test_df["sentiment_label"]
    )

    sentiment_results.append({
        "target": "Sentiment",
        "model": "LinearSVM",
        "C": C,
        **metrics
    })

    print(
        f"Accuracy={metrics['accuracy']:.4f} | "
        f"Macro F1={metrics['macro_f1']:.4f}"
    )


# ============================================================
# TOPIC TUNING
# ============================================================

print("\n")
print("=" * 70)
print("TOPIC HYPERPARAMETER SEARCH")
print("=" * 70)

topic_results = []


# ------------------------------------------------------------
# Logistic Regression
# ------------------------------------------------------------

for C in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:

    print(
        f"\nTesting Topic Logistic Regression "
        f"C={C}, class_weight=balanced"
    )

    model = LogisticRegression(
        C=C,
        max_iter=4000,
        class_weight="balanced",
        random_state=42
    )

    metrics = evaluate(
        model,
        X_train,
        X_test,
        train_df["topic_category"],
        test_df["topic_category"]
    )

    topic_results.append({
        "target": "Topic",
        "model": "LogisticRegression",
        "C": C,
        **metrics
    })

    print(
        f"Accuracy={metrics['accuracy']:.4f} | "
        f"Macro F1={metrics['macro_f1']:.4f}"
    )


# ------------------------------------------------------------
# Linear SVM
# ------------------------------------------------------------

for C in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:

    print(
        f"\nTesting Topic Linear SVM "
        f"C={C}, class_weight=balanced"
    )

    model = LinearSVC(
        C=C,
        class_weight="balanced",
        random_state=42
    )

    metrics = evaluate(
        model,
        X_train,
        X_test,
        train_df["topic_category"],
        test_df["topic_category"]
    )

    topic_results.append({
        "target": "Topic",
        "model": "LinearSVM",
        "C": C,
        **metrics
    })

    print(
        f"Accuracy={metrics['accuracy']:.4f} | "
        f"Macro F1={metrics['macro_f1']:.4f}"
    )


# ============================================================
# Save results
# ============================================================

results = pd.DataFrame(
    sentiment_results + topic_results
)

output_path = REPORT_DIR / "hyperparameter_results.csv"

results.to_csv(
    output_path,
    index=False
)


print("\n")
print("=" * 70)
print("HYPERPARAMETER RESULTS")
print("=" * 70)

print(
    results[
        [
            "target",
            "model",
            "C",
            "accuracy",
            "macro_precision",
            "macro_recall",
            "macro_f1",
            "weighted_f1"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Best models
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("BEST CONFIGURATIONS")
print("=" * 70)

for target in ["Sentiment", "Topic"]:

    subset = results[
        results["target"] == target
    ]

    best = subset.loc[
        subset["macro_f1"].idxmax()
    ]

    print(f"\n{target}")
    print(f"Model      : {best['model']}")
    print(f"C          : {best['C']}")
    print(f"Accuracy   : {best['accuracy']:.4f}")
    print(f"Macro F1   : {best['macro_f1']:.4f}")

print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 70)
print("TUNING COMPLETE")
print("=" * 70)