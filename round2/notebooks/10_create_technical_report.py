import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REPORT_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

PDF_PATH = os.path.join(
    REPORT_DIR,
    "Round2_Technical_Report.pdf"
)


# ============================================================
# DOCUMENT
# ============================================================

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    rightMargin=42,
    leftMargin=42,
    topMargin=42,
    bottomMargin=42,
)


# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=20,
    leading=24,
    spaceAfter=10,
)

subtitle_style = ParagraphStyle(
    "SubtitleCustom",
    parent=styles["Normal"],
    alignment=TA_CENTER,
    fontSize=10,
    leading=14,
    spaceAfter=18,
)

heading_style = ParagraphStyle(
    "HeadingCustom",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=8,
)

subheading_style = ParagraphStyle(
    "SubHeadingCustom",
    parent=styles["Heading3"],
    fontSize=11,
    leading=14,
    spaceBefore=8,
    spaceAfter=5,
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
    spaceAfter=7,
)

bullet_style = ParagraphStyle(
    "BulletCustom",
    parent=body_style,
    leftIndent=14,
    firstLineIndent=-8,
    spaceAfter=4,
)

small_style = ParagraphStyle(
    "SmallCustom",
    parent=body_style,
    fontSize=8,
    leading=11,
)


# ============================================================
# TABLE HELPER
# ============================================================

def make_table(data, widths=None, font_size=8.5):

    table = Table(
        data,
        colWidths=widths,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), font_size),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return table


# ============================================================
# STORY
# ============================================================

story = []


# ============================================================
# TITLE
# ============================================================

story.append(
    Paragraph(
        "DATA VORTEX A'26 — ROUND 2",
        title_style,
    )
)

story.append(
    Paragraph(
        "Technical Report — Rebuilding the Social Engine",
        subtitle_style,
    )
)

story.append(
    Paragraph(
        "<b>Task:</b> NLP-based semantic classification of labelled social-media text",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Dataset:</b> Labeled_Social_NLP_Training_Data.csv",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Team:</b> soumadipd43",
        body_style,
    )
)

story.append(Spacer(1, 8))


# ============================================================
# 1. PROBLEM DEFINITION
# ============================================================

story.append(
    Paragraph(
        "1. Problem Definition",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The Round 2 task focuses on rebuilding a semantic comprehension layer "
        "for social-media text. The supplied dataset contains labelled textual "
        "posts with two prediction targets: sentiment_label and topic_category.",
        body_style,
    )
)

story.append(
    Paragraph(
        "The objective is to develop NLP classification models capable of "
        "extracting semantic information from short, noisy social-media text "
        "and assigning the appropriate sentiment and topic labels.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Sentiment classes:</b> Negative, Neutral, Positive.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Topic classes:</b> Account_Security, Community_Discussion, "
        "Feature_Feedback, Technical_Issues.",
        body_style,
    )
)


# ============================================================
# 2. DATASET UNDERSTANDING
# ============================================================

story.append(
    Paragraph(
        "2. Dataset Understanding",
        heading_style,
    )
)

dataset_data = [
    ["Property", "Observed Value"],
    ["Total rows", "9,000"],
    ["Columns", "4"],
    ["Missing values", "None"],
    ["Duplicate rows", "None"],
    ["Unique text IDs", "9,000"],
    ["Rows belonging to duplicated texts", "2,087"],
    ["Conflicting duplicate sentiment labels", "0"],
    ["Conflicting duplicate topic labels", "0"],
]

story.append(
    make_table(
        dataset_data,
        [3.0 * inch, 2.5 * inch],
    )
)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "<b>Sentiment distribution:</b> The three sentiment classes are "
        "perfectly balanced, with 3,000 samples each.",
        body_style,
    )
)

topic_distribution = [
    ["Topic", "Count", "Percentage"],
    ["Community_Discussion", "7,752", "86.13%"],
    ["Technical_Issues", "815", "9.06%"],
    ["Feature_Feedback", "297", "3.30%"],
    ["Account_Security", "136", "1.51%"],
]

story.append(
    Paragraph(
        "<b>Topic distribution:</b>",
        body_style,
    )
)

story.append(
    make_table(
        topic_distribution,
        [2.8 * inch, 1.2 * inch, 1.3 * inch],
    )
)

story.append(
    Paragraph(
        "The topic target is highly imbalanced. This imbalance was explicitly "
        "considered during model development and evaluation.",
        body_style,
    )
)


# ============================================================
# 3. PREPROCESSING PIPELINE
# ============================================================

story.append(
    Paragraph(
        "3. Preprocessing Pipeline",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The preprocessing strategy was deliberately conservative so that "
        "semantic information and social-media signals were not unnecessarily "
        "removed.",
        body_style,
    )
)

preprocessing_steps = [
    ["Step", "Processing"],
    ["1", "Load the original labelled CSV dataset."],
    ["2", "Validate missing values, duplicates and label consistency."],
    ["3", "Normalize leading/trailing whitespace in post_text."],
    ["4", "Remove empty text records; none were removed."],
    ["5", "Create a group-based train/test split using post_text."],
    ["6", "Verify zero exact post_text overlap between train and test."],
    ["7", "Apply TF-IDF feature extraction for the classical topic model."],
    ["8", "Tokenize text using DistilBERT tokenizer for sentiment modelling."],
]

story.append(
    make_table(
        preprocessing_steps,
        [0.6 * inch, 5.0 * inch],
    )
)

story.append(
    Paragraph(
        "A GroupShuffleSplit strategy was used with post_text as the grouping "
        "variable. The final split contains 7,178 training rows and 1,822 "
        "testing rows. There is zero exact text overlap between the two sets, "
        "reducing the risk of duplicate-text leakage.",
        body_style,
    )
)


# ============================================================
# 4. MODEL SELECTION
# ============================================================

story.append(
    Paragraph(
        "4. Model Selection",
        heading_style,
    )
)

story.append(
    Paragraph(
        "Several classical machine-learning baselines were evaluated using "
        "TF-IDF representations. Logistic Regression, Linear SVM and Naive "
        "Bayes were tested for both sentiment and topic classification.",
        body_style,
    )
)

baseline_data = [
    ["Task", "Model", "Accuracy", "Macro F1"],
    ["Sentiment", "Logistic Regression", "58.23%", "0.5833"],
    ["Sentiment", "Linear SVM", "55.65%", "0.5574"],
    ["Sentiment", "Naive Bayes", "57.03%", "0.5689"],
    ["Topic", "Logistic Regression", "88.20%", "0.3413"],
    ["Topic", "Linear SVM", "91.66%", "0.5465"],
    ["Topic", "Naive Bayes", "85.51%", "0.2305"],
]

story.append(
    make_table(
        baseline_data,
        [1.0 * inch, 2.0 * inch, 1.2 * inch, 1.2 * inch],
    )
)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "An enhanced TF-IDF representation combining word n-grams and "
        "character n-grams improved topic performance substantially. "
        "Class weighting was used for the imbalanced topic target.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Final sentiment model:</b> DistilBERT "
        "(distilbert-base-uncased), fine-tuned for three sentiment classes.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Final topic model:</b> Linear SVM with C=2.0, balanced class "
        "weights, combined word and character TF-IDF features.",
        body_style,
    )
)


# ============================================================
# 5. TRAINING METHODOLOGY
# ============================================================

story.append(
    Paragraph(
        "5. Training Methodology",
        heading_style,
    )
)

story.append(
    Paragraph(
        "For sentiment classification, DistilBERT was fine-tuned using the "
        "7,178 training samples. Text was tokenized with a maximum sequence "
        "length of 128 tokens. Training used two epochs, a learning rate of "
        "2 × 10⁻⁵, batch size of 8 and weight decay of 0.01.",
        body_style,
    )
)

story.append(
    Paragraph(
        "The model was evaluated after training using the held-out test set. "
        "The best model was selected using Macro F1 as the evaluation criterion.",
        body_style,
    )
)

story.append(
    Paragraph(
        "For topic classification, word-level TF-IDF features used 1–3 grams "
        "with a maximum of 100,000 features. Character-level TF-IDF features "
        "used 3–6 character grams with a maximum of 100,000 features. The two "
        "sparse matrices were combined and supplied to a Linear SVM with "
        "C=2.0 and class_weight='balanced'.",
        body_style,
    )
)

story.append(
    Paragraph(
        "The use of character n-grams helps represent variations and partial "
        "patterns in short social-media text, while word n-grams capture "
        "lexical context.",
        body_style,
    )
)


# ============================================================
# 6. EVALUATION METRICS
# ============================================================

story.append(
    Paragraph(
        "6. Evaluation Metrics",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The evaluation uses accuracy, precision, recall, F1-score and "
        "confusion matrices. Macro-averaged metrics are particularly important "
        "for topic classification because the topic labels are highly "
        "imbalanced.",
        body_style,
    )
)

metrics_data = [
    ["Task", "Model", "Accuracy", "Macro F1", "Weighted F1"],
    ["Sentiment", "DistilBERT", "68.33%", "0.6781", "0.6777"],
    ["Topic", "TF-IDF + Linear SVM", "93.08%", "0.6160", "0.9157"],
]

story.append(
    make_table(
        metrics_data,
        [1.0 * inch, 2.0 * inch, 1.1 * inch, 1.0 * inch, 1.1 * inch],
    )
)

story.append(
    Paragraph(
        "The sentiment model achieved 68.33% accuracy and a Macro F1 of "
        "0.6781. The topic model achieved 93.08% accuracy and a Macro F1 "
        "of 0.6160. The difference between topic accuracy and Macro F1 "
        "reflects the strong topic-class imbalance.",
        body_style,
    )
)


# ============================================================
# 7. CONFUSION MATRIX — SENTIMENT
# ============================================================

story.append(
    Paragraph(
        "7. Confusion Matrix — Sentiment",
        heading_style,
    )
)

sentiment_cm = [
    ["Actual \\ Predicted", "Negative", "Neutral", "Positive"],
    ["Negative", "459", "70", "67"],
    ["Neutral", "128", "312", "171"],
    ["Positive", "52", "89", "474"],
]

story.append(
    make_table(
        sentiment_cm,
        [1.7 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch],
    )
)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "The model correctly classified 459 Negative, 312 Neutral and "
        "474 Positive test samples. Neutral has the weakest recall at "
        "51.06%. The largest individual confusion is Neutral predicted "
        "as Positive, occurring in 171 cases.",
        body_style,
    )
)


# ============================================================
# 8. CONFUSION MATRIX — TOPIC
# ============================================================

story.append(
    Paragraph(
        "8. Confusion Matrix — Topic",
        heading_style,
    )
)

topic_cm = [
    [
        "Actual \\ Predicted",
        "Account_Security",
        "Community_Discussion",
        "Feature_Feedback",
        "Technical_Issues",
    ],
    ["Account_Security", "8", "15", "2", "0"],
    ["Community_Discussion", "0", "1558", "0", "0"],
    ["Feature_Feedback", "0", "53", "7", "0"],
    ["Technical_Issues", "0", "56", "0", "123"],
]

story.append(
    make_table(
        topic_cm,
        [1.25 * inch, 1.1 * inch, 1.35 * inch, 1.15 * inch, 1.1 * inch],
        font_size=7,
    )
)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "Community_Discussion is classified very strongly, with all 1,558 "
        "test samples correctly identified. The minority classes are harder "
        "to detect. Feature_Feedback has recall of 11.67%, while "
        "Account_Security has recall of 32.00%. Many minority-class samples "
        "are classified as Community_Discussion.",
        body_style,
    )
)


# ============================================================
# 9. ERROR ANALYSIS
# ============================================================

story.append(PageBreak())

story.append(
    Paragraph(
        "9. Error Analysis",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The error patterns reveal different challenges for the two NLP tasks.",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Sentiment classification:</b>",
        subheading_style,
    )
)

for item in [
    "Neutral language is the most difficult sentiment class, with recall of 0.5106.",
    "Neutral → Positive is the largest confusion pair with 171 samples.",
    "Neutral → Negative accounts for another 128 misclassifications.",
    "The relatively balanced class distribution means these errors are not primarily caused by class-frequency imbalance.",
]:
    story.append(
        Paragraph(
            "• " + item,
            bullet_style,
        )
    )


story.append(
    Paragraph(
        "<b>Topic classification:</b>",
        subheading_style,
    )
)

for item in [
    "The topic distribution is highly skewed toward Community_Discussion (86.13%).",
    "Feature_Feedback has only 60 test samples and recall of 0.1167.",
    "Account_Security has only 25 test samples and recall of 0.3200.",
    "Feature_Feedback and Account_Security samples are frequently absorbed into the dominant Community_Discussion class.",
    "Accuracy alone therefore gives an incomplete picture of topic performance; Macro F1 provides a more balanced assessment across classes.",
]:
    story.append(
        Paragraph(
            "• " + item,
            bullet_style,
        )
    )


# ============================================================
# 10. DATA QUALITY AND LEAKAGE CONTROL
# ============================================================

story.append(
    Paragraph(
        "10. Data Quality and Leakage Control",
        heading_style,
    )
)

story.append(
    Paragraph(
        "Dataset validation found no missing values, no duplicate rows and "
        "no duplicate text IDs. Although repeated post_text values exist, "
        "duplicate texts had consistent sentiment and topic labels.",
        body_style,
    )
)

story.append(
    Paragraph(
        "To prevent repeated text from appearing across training and testing, "
        "the train/test split was grouped by post_text. The final split has "
        "zero exact text overlap between training and testing data.",
        body_style,
    )
)


# ============================================================
# 11. MODEL COMPARISON AND JUSTIFICATION
# ============================================================

story.append(
    Paragraph(
        "11. Model Comparison and Justification",
        heading_style,
    )
)

comparison_data = [
    ["Task", "Approach", "Accuracy", "Macro F1"],
    ["Sentiment", "TF-IDF + Logistic Regression", "59.66%", "0.5973"],
    ["Sentiment", "DistilBERT", "68.33%", "0.6781"],
    ["Topic", "Baseline TF-IDF + Linear SVM", "91.66%", "0.5465"],
    ["Topic", "Final TF-IDF + Linear SVM", "93.08%", "0.6160"],
]

story.append(
    make_table(
        comparison_data,
        [1.0 * inch, 2.8 * inch, 1.1 * inch, 1.0 * inch],
    )
)

story.append(
    Paragraph(
        "DistilBERT was selected for sentiment because the fine-tuned "
        "transformer produced stronger held-out sentiment metrics than the "
        "tested classical alternatives. For topic classification, the "
        "combined word/character TF-IDF representation with a balanced "
        "Linear SVM provided a practical and computationally efficient "
        "solution while improving Macro F1 over the baseline.",
        body_style,
    )
)


# ============================================================
# 12. LIMITATIONS AND FUTURE IMPROVEMENTS
# ============================================================

story.append(
    Paragraph(
        "12. Limitations and Future Improvements",
        heading_style,
    )
)

for item in [
    "The topic dataset is strongly imbalanced, particularly for Account_Security and Feature_Feedback.",
    "Minority-topic recall remains an important area for improvement.",
    "Sentiment errors show difficulty distinguishing Neutral language from positive and negative language.",
    "Further improvements could investigate targeted data augmentation, domain-specific pretrained language models, threshold/calibration strategies and additional minority-class examples.",
]:
    story.append(
        Paragraph(
            "• " + item,
            bullet_style,
        )
    )


# ============================================================
# 13. CONCLUSION
# ============================================================

story.append(
    Paragraph(
        "13. Conclusion",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The Round 2 NLP pipeline combines leakage-aware dataset preparation, "
        "classical TF-IDF modelling and transformer-based semantic modelling. "
        "The final sentiment model achieved 68.33% accuracy with a Macro F1 "
        "of 0.6781, while the final topic model achieved 93.08% accuracy "
        "with a Macro F1 of 0.6160.",
        body_style,
    )
)

story.append(
    Paragraph(
        "The evaluation demonstrates the importance of examining per-class "
        "metrics and confusion matrices rather than relying on accuracy alone, "
        "particularly for the highly imbalanced topic classification task.",
        body_style,
    )
)


# ============================================================
# BUILD PDF
# ============================================================

doc.build(story)

print("=" * 70)
print("TECHNICAL REPORT CREATED")
print("=" * 70)

print("\nSaved to:")
print(PDF_PATH)