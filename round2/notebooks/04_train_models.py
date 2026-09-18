import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ============================================================
# DATA VORTEX A'26 — ROUND 2
# NLP MODEL TRAINING & COMPARISON
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "data" / "train.csv"
TEST_PATH = BASE_DIR / "data" / "test.csv"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

FIGURE_DIR = OUTPUT_DIR / "confusion_matrices"
FIGURE_DIR.mkdir(exist_ok=True)

RESULTS_DIR = BASE_DIR / "reports"
RESULTS_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("DATA VORTEX A'26 — ROUND 2 NLP MODEL TRAINING")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load data
# ------------------------------------------------------------

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

X_train_text = train_df["post_text"].astype(str)
X_test_text = test_df["post_text"].astype(str)

print("\nDataset:")
print(f"Training samples : {len(train_df)}")
print(f"Testing samples  : {len(test_df)}")

# ------------------------------------------------------------
# 2. TF-IDF feature extraction
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TF-IDF FEATURE EXTRACTION")
print("=" * 70)

vectorizer = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True,
    max_features=50000
)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

print(f"TF-IDF training matrix: {X_train.shape}")
print(f"TF-IDF testing matrix : {X_test.shape}")

# ------------------------------------------------------------
# 3. Define models
# ------------------------------------------------------------

models = {
    "Logistic_Regression": LogisticRegression(
        max_iter=2000,
        random_state=42
    ),

    "Linear_SVM": LinearSVC(
        C=1.0,
        random_state=42
    ),

    "Naive_Bayes": MultinomialNB(
        alpha=1.0
    )
}

# ------------------------------------------------------------
# 4. Evaluation function
# ------------------------------------------------------------

def evaluate_models(target_name, y_train, y_test):

    print("\n")
    print("=" * 70)
    print(f"{target_name.upper()} CLASSIFICATION")
    print("=" * 70)

    results = []

    for model_name, model in models.items():

        print("\n" + "-" * 70)
        print(f"Training: {model_name}")
        print("-" * 70)

        # Train
        model.fit(X_train, y_train)

        # Predict
        predictions = model.predict(X_test)

        # Metrics
        accuracy = accuracy_score(y_test, predictions)

        precision_macro, recall_macro, f1_macro, _ = (
            precision_recall_fscore_support(
                y_test,
                predictions,
                average="macro",
                zero_division=0
            )
        )

        precision_weighted, recall_weighted, f1_weighted, _ = (
            precision_recall_fscore_support(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )
        )

        print(f"Accuracy          : {accuracy:.4f}")
        print(f"Macro Precision   : {precision_macro:.4f}")
        print(f"Macro Recall      : {recall_macro:.4f}")
        print(f"Macro F1          : {f1_macro:.4f}")
        print(f"Weighted F1       : {f1_weighted:.4f}")

        print("\nClassification Report:")
        print(
            classification_report(
                y_test,
                predictions,
                digits=4,
                zero_division=0
            )
        )

        # ----------------------------------------------------
        # Confusion matrix
        # ----------------------------------------------------

        labels = sorted(pd.Series(y_test).unique())

        cm = confusion_matrix(
            y_test,
            predictions,
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
            f"{target_name} — {model_name}\nConfusion Matrix"
        )

        plt.tight_layout()

        figure_path = (
            FIGURE_DIR /
            f"{target_name}_{model_name}_confusion_matrix.png"
        )

        plt.savefig(
            figure_path,
            dpi=200,
            bbox_inches="tight"
        )

        plt.close()

        print(f"Confusion matrix saved: {figure_path}")

        # ----------------------------------------------------
        # Store result
        # ----------------------------------------------------

        results.append({
            "target": target_name,
            "model": model_name,
            "accuracy": accuracy,
            "macro_precision": precision_macro,
            "macro_recall": recall_macro,
            "macro_f1": f1_macro,
            "weighted_precision": precision_weighted,
            "weighted_recall": recall_weighted,
            "weighted_f1": f1_weighted
        })

        # ----------------------------------------------------
        # Save classification report
        # ----------------------------------------------------

        report_path = (
            RESULTS_DIR /
            f"{target_name}_{model_name}_classification_report.txt"
        )

        with open(report_path, "w", encoding="utf-8") as f:

            f.write(
                classification_report(
                    y_test,
                    predictions,
                    digits=4,
                    zero_division=0
                )
            )

    return results


# ------------------------------------------------------------
# 5. Sentiment models
# ------------------------------------------------------------

sentiment_results = evaluate_models(
    "Sentiment",
    train_df["sentiment_label"],
    test_df["sentiment_label"]
)

# ------------------------------------------------------------
# 6. Topic models
# ------------------------------------------------------------

topic_results = evaluate_models(
    "Topic",
    train_df["topic_category"],
    test_df["topic_category"]
)

# ------------------------------------------------------------
# 7. Combine results
# ------------------------------------------------------------

all_results = sentiment_results + topic_results

results_df = pd.DataFrame(all_results)

results_path = RESULTS_DIR / "model_comparison.csv"

results_df.to_csv(
    results_path,
    index=False
)

# ------------------------------------------------------------
# 8. Display comparison
# ------------------------------------------------------------

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(
    results_df[
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

# ------------------------------------------------------------
# 9. Identify best model for each target
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("BEST MODELS")
print("=" * 70)

for target in ["Sentiment", "Topic"]:

    subset = results_df[
        results_df["target"] == target
    ]

    best = subset.loc[
        subset["macro_f1"].idxmax()
    ]

    print(
        f"\n{target}:"
        f"\n  Model     : {best['model']}"
        f"\n  Accuracy  : {best['accuracy']:.4f}"
        f"\n  Macro F1  : {best['macro_f1']:.4f}"
    )

print("\n" + "=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)

print(f"\nResults saved to:")
print(results_path)

print(f"\nConfusion matrices saved to:")
print(FIGURE_DIR)