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
    "Round2_Evaluation_Metrics_Report.pdf"
)


# ============================================================
# DOCUMENT
# ============================================================

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
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
    spaceAfter=12,
)

subtitle_style = ParagraphStyle(
    "SubtitleCustom",
    parent=styles["Normal"],
    alignment=TA_CENTER,
    fontSize=11,
    leading=15,
    spaceAfter=20,
)

heading_style = ParagraphStyle(
    "HeadingCustom",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=10,
    leading=15,
    spaceAfter=8,
)

small_style = ParagraphStyle(
    "SmallCustom",
    parent=styles["BodyText"],
    fontSize=8.5,
    leading=12,
)


# ============================================================
# HELPERS
# ============================================================

def make_table(data, widths=None):

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
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return table


# ============================================================
# CONTENT
# ============================================================

story = []


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

story.append(
    Paragraph(
        "DATA VORTEX A'26 — ROUND 2",
        title_style,
    )
)

story.append(
    Paragraph(
        "Evaluation Metrics Report",
        subtitle_style,
    )
)

story.append(
    Paragraph(
        "<b>Theme:</b> Rebuilding the Social Engine",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Dataset:</b> Labeled Social NLP Training Data",
        body_style,
    )
)

story.append(
    Paragraph(
        "<b>Test Set:</b> 1,822 samples",
        body_style,
    )
)

story.append(Spacer(1, 10))


# ============================================================
# 1. MODEL OVERVIEW
# ============================================================

story.append(
    Paragraph(
        "1. Model Overview",
        heading_style,
    )
)

story.append(
    Paragraph(
        "Two NLP classification tasks were evaluated: sentiment classification "
        "and topic classification. A transformer-based model was used for "
        "sentiment classification, while a TF-IDF based linear classifier was "
        "used for topic classification.",
        body_style,
    )
)

model_data = [
    ["Task", "Final Model", "Features / Configuration"],
    [
        "Sentiment",
        "DistilBERT",
        "distilbert-base-uncased, 3 classes, 2 epochs"
    ],
    [
        "Topic",
        "Linear SVM",
        "Word + Character TF-IDF, C=2.0, class_weight=balanced"
    ],
]

story.append(
    make_table(
        model_data,
        [1.0 * inch, 1.4 * inch, 4.0 * inch],
    )
)


# ============================================================
# 2. SENTIMENT RESULTS
# ============================================================

story.append(
    Paragraph(
        "2. Sentiment Classification Evaluation",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The final sentiment model was DistilBERT "
        "(distilbert-base-uncased), fine-tuned for three sentiment classes: "
        "Negative, Neutral and Positive.",
        body_style,
    )
)

sentiment_metrics = [
    ["Metric", "Value"],
    ["Accuracy", "0.6833 (68.33%)"],
    ["Macro Precision", "0.6822"],
    ["Macro Recall", "0.6838"],
    ["Macro F1", "0.6781"],
    ["Weighted F1", "0.6777"],
]

story.append(
    make_table(
        sentiment_metrics,
        [3.5 * inch, 2.0 * inch],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Sentiment Classification Report</b>",
        body_style,
    )
)

sentiment_report = [
    ["Class", "Precision", "Recall", "F1-score", "Support"],
    ["Negative", "0.7183", "0.7701", "0.7433", "596"],
    ["Neutral", "0.6624", "0.5106", "0.5767", "611"],
    ["Positive", "0.6657", "0.7707", "0.7144", "615"],
]

story.append(
    make_table(
        sentiment_report,
        [1.5 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Sentiment Confusion Matrix</b>",
        body_style,
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
        [1.6 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Sentiment Error Analysis:</b> The Neutral class has the lowest "
        "recall (0.5106). The largest confusion occurs between Neutral and "
        "Positive, with 171 Neutral samples predicted as Positive. "
        "There are also 128 Neutral samples predicted as Negative. "
        "This indicates that neutral social-media language is harder to "
        "separate from explicitly positive or negative language.",
        body_style,
    )
)


# ============================================================
# 3. TOPIC RESULTS
# ============================================================

story.append(PageBreak())

story.append(
    Paragraph(
        "3. Topic Classification Evaluation",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The final topic classifier uses combined word-level and character-level "
        "TF-IDF features with a Linear SVM. Class weighting was enabled to "
        "reduce the effect of the strong topic-class imbalance.",
        body_style,
    )
)

topic_metrics = [
    ["Metric", "Value"],
    ["Accuracy", "0.9308 (93.08%)"],
    ["Macro Precision", "0.9260"],
    ["Macro Recall", "0.5310"],
    ["Macro F1", "0.6160"],
    ["Weighted F1", "0.9157"],
]

story.append(
    make_table(
        topic_metrics,
        [3.5 * inch, 2.0 * inch],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Topic Classification Report</b>",
        body_style,
    )
)

topic_report = [
    ["Class", "Precision", "Recall", "F1-score", "Support"],
    ["Account_Security", "1.0000", "0.3200", "0.4848", "25"],
    ["Community_Discussion", "0.9263", "1.0000", "0.9617", "1558"],
    ["Feature_Feedback", "0.7778", "0.1167", "0.2029", "60"],
    ["Technical_Issues", "1.0000", "0.6872", "0.8146", "179"],
]

story.append(
    make_table(
        topic_report,
        [1.7 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 0.9 * inch],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Topic Confusion Matrix</b>",
        body_style,
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
        [1.3 * inch, 1.1 * inch, 1.4 * inch, 1.2 * inch, 1.1 * inch],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "<b>Topic Error Analysis:</b> The dataset has substantial topic "
        "imbalance, with Community_Discussion representing the large majority "
        "of samples. Although the classifier achieves high overall accuracy, "
        "minority-class recall is substantially lower. Feature_Feedback has "
        "the lowest recall (0.1167), while Account_Security has recall 0.3200. "
        "Many minority-class samples are predicted as Community_Discussion. "
        "Therefore, macro F1 is more informative than accuracy alone for "
        "evaluating topic performance.",
        body_style,
    )
)


# ============================================================
# 4. COMPARISON
# ============================================================

story.append(
    Paragraph(
        "4. Final Evaluation Summary",
        heading_style,
    )
)

summary_data = [
    ["Task", "Model", "Accuracy", "Macro F1", "Weighted F1"],
    ["Sentiment", "DistilBERT", "68.33%", "0.6781", "0.6777"],
    ["Topic", "TF-IDF + Linear SVM", "93.08%", "0.6160", "0.9157"],
]

story.append(
    make_table(
        summary_data,
        [1.1 * inch, 2.0 * inch, 1.1 * inch, 1.0 * inch, 1.1 * inch],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "The evaluation demonstrates two different performance characteristics. "
        "Sentiment classification remains a more challenging semantic task, "
        "while topic classification achieves high overall accuracy but shows "
        "weaker minority-class recall because of the dataset's topic imbalance. "
        "Macro F1 is therefore reported alongside accuracy to provide a more "
        "balanced view of classification performance.",
        body_style,
    )
)


# ============================================================
# 5. METHODOLOGICAL NOTE
# ============================================================

story.append(
    Paragraph(
        "5. Evaluation Methodology",
        heading_style,
    )
)

story.append(
    Paragraph(
        "The dataset was split using a group-based strategy based on post_text. "
        "This prevented exact duplicate texts from appearing in both the "
        "training and testing sets. The resulting split contained 7,178 "
        "training rows and 1,822 testing rows, with zero exact text overlap "
        "between the two sets.",
        body_style,
    )
)

story.append(
    Paragraph(
        "For topic classification, class_weight='balanced' was used to account "
        "for the severe class imbalance. Evaluation includes accuracy, "
        "macro precision, macro recall, macro F1, weighted F1, classification "
        "reports and confusion matrices.",
        body_style,
    )
)


# ============================================================
# BUILD PDF
# ============================================================

doc.build(story)

print("=" * 70)
print("EVALUATION REPORT CREATED")
print("=" * 70)
print("\nSaved to:")
print(PDF_PATH)