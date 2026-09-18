import csv
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "sql" / "outputs"


def read_csv(filename):
    with open(OUTPUT_DIR / filename, encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def make_image(csv_file, image_file, title):
    data = read_csv(csv_file)

    headers = data[0]
    rows = data[1:]

    # Make the image tall enough for all rows.
    height = max(5, 1.5 + len(rows) * 0.38)

    fig, ax = plt.subplots(figsize=(15, height))
    ax.axis("off")

    ax.set_title(
        title,
        fontsize=18,
        fontweight="bold",
        pad=20
    )

    table = ax.table(
        cellText=rows,
        colLabels=headers,
        loc="center",
        cellLoc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)

    # Make header text bold.
    for cell in table.get_celld().values():
        if cell.get_text().get_text() in headers:
            cell.get_text().set_weight("bold")

    output_path = OUTPUT_DIR / image_file

    plt.savefig(
        output_path,
        format="jpeg",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Created: {output_path}")


make_image(
    "E3_output.csv",
    "E3_output.jpeg",
    "DATA VORTEX — E3: Average Engagement by Platform"
)

make_image(
    "M1_output.csv",
    "M1_output.jpeg",
    "DATA VORTEX — M1: Location Engagement"
)

make_image(
    "H6_output.csv",
    "H6_output.jpeg",
    "DATA VORTEX — H6: Suspicious High Impact Users"
)

print("\nAll three JPEG output screenshots created successfully.")