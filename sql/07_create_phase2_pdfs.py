import csv
import html
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"
OUTPUT_DIR = SQL_DIR / "outputs"

PDF_DIR = BASE_DIR / "outputs"
PDF_DIR.mkdir(exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def read_csv(filename):
    path = OUTPUT_DIR / filename

    with open(path, "r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def read_sql(filename):
    path = SQL_DIR / filename

    return path.read_text(encoding="utf-8")


def create_document(path):
    return SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )


# ============================================================
# DATA
# ============================================================

e3 = read_csv("E3_output.csv")
m1 = read_csv("M1_output.csv")
h6 = read_csv("H6_output.csv")

e3_sql = read_sql("03_E3_platform_engagement.sql")
m1_sql = read_sql("04_M1_location_engagement.sql")
h6_sql = read_sql("05_H6_suspicious_high_impact_users.sql")


# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()

styles.add(
    ParagraphStyle(
        name="DVTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=19,
        leading=23,
        spaceAfter=10,
    )
)

styles.add(
    ParagraphStyle(
        name="DVSubtitle",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=14,
        spaceAfter=15,
    )
)

styles.add(
    ParagraphStyle(
        name="CodeBlock",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=6.8,
        leading=8.5,
        spaceAfter=12,
    )
)


def code_paragraph(sql_text):
    escaped = html.escape(sql_text)
    escaped = escaped.replace("\n", "<br/>")

    return Paragraph(
        f"<font name='Courier'>{escaped}</font>",
        styles["CodeBlock"],
    )


# ============================================================
# PDF 1 — SQL QUERIES
# ============================================================

sql_pdf = PDF_DIR / "Data_Vortex_Phase2_SQL_Queries.pdf"

story = [
    Paragraph(
        "DATA VORTEX — ROUND 1 PHASE 2",
        styles["DVTitle"],
    ),
    Paragraph(
        "Final SQL Queries",
        styles["Heading1"],
    ),
    Paragraph(
        "Selected questions: E3 (Easy), M1 (Medium), H6 (Hard)",
        styles["DVSubtitle"],
    ),
]


sections = [
    (
        "E3 — Average Engagement by Platform",
        e3_sql,
    ),
    (
        "M1 — Which Locations Generate the Most Engagement?",
        m1_sql,
    ),
    (
        "H6 — Find the Most Suspicious High Impact Users",
        h6_sql,
    ),
]


for title, query in sections:

    story.append(
        Paragraph(title, styles["Heading2"])
    )

    story.append(
        code_paragraph(query)
    )

    story.append(Spacer(1, 8))


story.append(
    Paragraph(
        "All analytical outputs are generated dynamically from the SQLite "
        "database. No result values are hardcoded into the analytical queries.",
        styles["BodyText"],
    )
)

create_document(sql_pdf).build(story)


# ============================================================
# PDF 2 — LOGIC EXPLANATION
# ============================================================

logic_pdf = PDF_DIR / "Data_Vortex_Phase2_Logic_Explanation.pdf"

story = [
    Paragraph(
        "DATA VORTEX — ROUND 1 PHASE 2",
        styles["DVTitle"],
    ),
    Paragraph(
        "Logic Explanation",
        styles["Heading1"],
    ),
    Paragraph(
        "Analytical approach for the selected Easy, Medium and Hard questions.",
        styles["DVSubtitle"],
    ),
]


story.append(
    Paragraph(
        "E3 — Average Engagement by Platform",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        "The query groups posts by platform and calculates the average "
        "likes, shares, comments and total engagement for each platform. "
        "Posts with missing likes and engagement are excluded from these "
        "engagement averages. The results are ordered from the highest "
        "average total engagement to the lowest.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 12))

story.append(
    Paragraph(
        "SQL concepts used: GROUP BY, AVG(), WHERE, ORDER BY and calculated "
        "aggregation.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 18))


story.append(
    Paragraph(
        "M1 — Which Locations Generate the Most Engagement?",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        "The users and posts tables are joined using user_id. Posts with "
        "missing engagement are excluded. The query then groups records "
        "by user location, counts the posts and calculates total engagement "
        "using SUM(). Finally, locations are ordered from highest to lowest "
        "total engagement.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 12))

story.append(
    Paragraph(
        "SQL concepts used: INNER JOIN, GROUP BY, COUNT(), SUM(), WHERE "
        "and ORDER BY.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 18))


story.append(
    Paragraph(
        "H6 — Find the Most Suspicious High Impact Users",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        "The analysis first calculates the overall average engagement. "
        "A second aggregation calculates post count, average engagement "
        "and total engagement for every user. The final filtering stage "
        "keeps users who have fewer than 10,000 followers, whose average "
        "engagement is above the overall average, and who have at least "
        "one post where shares are greater than likes.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 12))

story.append(
    Paragraph(
        "The EXISTS condition checks whether the user has at least one "
        "qualifying post without duplicating users in the final result. "
        "The final output is ranked by total engagement.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 12))

story.append(
    Paragraph(
        "SQL concepts used: CTEs, aggregation, INNER JOIN, CROSS JOIN, "
        "EXISTS, correlated subquery, filtering and ORDER BY.",
        styles["BodyText"],
    )
)

story.append(PageBreak())

story.append(
    Paragraph(
        "Data Handling Principle",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        "The SQL analysis respects the Phase 1 cleaning methodology. "
        "Missing engagement values are not converted to zero because doing "
        "so would fabricate engagement. Only records with known engagement "
        "are included in engagement-based calculations.",
        styles["BodyText"],
    )
)

create_document(logic_pdf).build(story)


# ============================================================
# PDF 3 — INSIGHT REPORT
# ============================================================

insight_pdf = PDF_DIR / "Data_Vortex_Phase2_Insight_Report.pdf"

top_e3 = e3[0]
top_m1 = m1[0]

story = [
    Paragraph(
        "DATA VORTEX — ROUND 1 PHASE 2",
        styles["DVTitle"],
    ),
    Paragraph(
        "Phase 2 Insight Report",
        styles["Heading1"],
    ),
    Paragraph(
        "Selected questions: E3 (Easy), M1 (Medium), H6 (Hard)",
        styles["DVSubtitle"],
    ),
]


# E3
story.append(
    Paragraph(
        "1. Platform Engagement — E3",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        f"The platform with the highest average total engagement is "
        f"<b>{html.escape(top_e3['platform'])}</b>, with an average total "
        f"engagement of <b>{top_e3['avg_total_engagement']}</b>.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "The SQL output shows that platform-level average engagement values "
        "are relatively close to one another. Therefore, platform choice "
        "does not appear to create a large difference in average engagement "
        "within this recovered dataset.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 18))


# M1
story.append(
    Paragraph(
        "2. Location Engagement — M1",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        f"The highest-total-engagement location in the SQL output is "
        f"<b>{html.escape(top_m1['location'])}</b>, with "
        f"<b>{top_m1['total_engagement']}</b> total engagement across "
        f"<b>{top_m1['post_count']}</b> posts with known engagement.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "This analysis demonstrates that engagement can vary substantially "
        "across user locations. The result is based on total engagement, "
        "so both posting volume and engagement per post can influence the "
        "ranking.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 18))


# H6
story.append(
    Paragraph(
        "3. Suspicious High-Impact Users — H6",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        f"The H6 query identified <b>{len(h6)}</b> users who satisfy all "
        "three specified conditions: fewer than 10,000 followers, average "
        "post engagement above the overall average, and at least one post "
        "where shares exceed likes.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "These users are noteworthy because their engagement performance "
        "is high relative to the overall dataset despite having comparatively "
        "small follower counts. The shares-greater-than-likes condition "
        "adds a behavioral signal to the identification criteria.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 18))


# Data integrity
story.append(
    Paragraph(
        "4. Data Integrity",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        "The SQL database contains 1,500 users and 12,000 cleaned posts. "
        "Database loading validation found zero invalid user references "
        "and zero duplicate post IDs. Missing engagement is excluded from "
        "engagement calculations rather than being interpreted as zero.",
        styles["BodyText"],
    )
)

story.append(Spacer(1, 18))


# Limitations
story.append(
    Paragraph(
        "5. Limitations",
        styles["Heading2"],
    )
)

story.append(
    Paragraph(
        "The findings describe the recovered Dataset 01 only. They should "
        "not be generalized beyond this dataset. The analyses identify "
        "patterns and associations rather than proving causation. Records "
        "with incomplete engagement are intentionally excluded from "
        "engagement-based calculations.",
        styles["BodyText"],
    )
)

create_document(insight_pdf).build(story)


# ============================================================
# FINAL MESSAGE
# ============================================================

print()
print("=" * 60)
print("PHASE 2 PDF GENERATION COMPLETE")
print("=" * 60)

print(f"Created: {sql_pdf}")
print(f"Created: {logic_pdf}")
print(f"Created: {insight_pdf}")

print()
print("All three required PDF deliverables are ready.")