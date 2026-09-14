"""
Data Vortex - Dataset 01 Cleaning Pipeline

Purpose:
    Clean the recovered Social Engine datasets without fabricating data.

Rules:
    1. Raw files are never modified.
    2. Exact duplicate post records are removed.
    3. Negative likes are treated as invalid and converted to missing.
    4. Missing platform values become "Unknown".
    5. Missing/corrupted text is not invented.
    6. HTML entities/tags and control characters are cleaned.
    7. Mixed timestamp formats are standardized.
    8. Cleaning decisions are recorded for reproducibility.
"""

from pathlib import Path
import html
import re
import json

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

USERS_FILE = RAW_DIR / "Social_Engine_Users.csv"
POSTS_FILE = RAW_DIR / "Social_Engine_Posts_Corrupted.csv"

CLEAN_USERS_FILE = PROCESSED_DIR / "cleaned_users.csv"
CLEAN_POSTS_FILE = PROCESSED_DIR / "cleaned_posts.csv"
CLEANING_LOG_FILE = PROCESSED_DIR / "cleaning_log.json"


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):
    """
    Clean corrupted social-media text.

    Operations:
    - Treat NULL-like values as missing.
    - Decode HTML entities.
    - Remove HTML tags.
    - Remove control characters.
    - Normalize whitespace.
    """

    if pd.isna(value):
        return pd.NA

    text = str(value)

    # Decode HTML entities such as &amp; -> &
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]*>", " ", text)

    # Remove control characters
    text = re.sub(r"[\x00-\x1F\x7F]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # NULL-like values after corruption has been cleaned
    if re.fullmatch(r"(?i)null[\s&;]*", text):
        return pd.NA

    if text == "":
        return pd.NA

    return text


# ============================================================
# TIMESTAMP CLEANING
# ============================================================

def parse_timestamp(value):
    """
    Convert the three observed timestamp formats into
    one standardized datetime representation.

    Supported formats:
    - DD-MM-YYYY ...
    - YYYY-MM-DDTHH:MM:SS
    - Unix seconds
    """

    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    # Unix timestamp: exactly 10 digits
    if re.fullmatch(r"\d{10}", value):
        try:
            # Unix timestamps represent UTC.
            timestamp = pd.to_datetime(
                int(value),
                unit="s",
                utc=True,
            )
            return timestamp.tz_localize(None)
        except (ValueError, OverflowError):
            return pd.NaT

    # DD-MM-YYYY format
    if re.match(r"^\d{2}-\d{2}-\d{4}", value):
        try:
            return pd.to_datetime(
                value,
                dayfirst=True,
                errors="coerce",
            )
        except (ValueError, TypeError):
            return pd.NaT

    # ISO-style format
    return pd.to_datetime(
        value,
        errors="coerce",
    )


# ============================================================
# USER CLEANING
# ============================================================

def clean_users(users):
    """Clean and standardize the users dataset."""

    users = users.copy()

    # Standardize IDs as strings
    users["user_id"] = users["user_id"].astype("string").str.strip()

    # Parse account creation date
    users["account_created"] = pd.to_datetime(
        users["account_created"],
        errors="coerce",
    )

    # Numeric follower count
    users["follower_count"] = pd.to_numeric(
        users["follower_count"],
        errors="coerce",
    )

    # Standardize text fields
    users["location"] = (
        users["location"]
        .astype("string")
        .str.strip()
    )

    users["language"] = (
        users["language"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    return users


# ============================================================
# POST CLEANING
# ============================================================

def clean_posts(posts):
    """Clean and standardize the corrupted posts dataset."""

    posts = posts.copy()

    # --------------------------------------------------------
    # Preserve original row count for audit
    # --------------------------------------------------------

    original_rows = len(posts)

    # --------------------------------------------------------
    # Standardize IDs
    # --------------------------------------------------------

    posts["post_id"] = (
        posts["post_id"]
        .astype("string")
        .str.strip()
    )

    posts["user_id"] = (
        posts["user_id"]
        .astype("string")
        .str.strip()
    )

    # --------------------------------------------------------
    # Track missing values BEFORE cleaning
    # --------------------------------------------------------

    posts["platform_was_missing"] = posts["platform"].isna()
    posts["text_was_missing"] = posts["text_content"].isna()
    posts["likes_was_missing"] = posts["likes"].isna()

    # --------------------------------------------------------
    # Platform
    # --------------------------------------------------------

    posts["platform"] = (
        posts["platform"]
        .astype("string")
        .str.strip()
    )

    posts["platform"] = posts["platform"].fillna("Unknown")

    # --------------------------------------------------------
    # Text
    # --------------------------------------------------------

    posts["text_content"] = posts["text_content"].apply(clean_text)

    # --------------------------------------------------------
    # Numeric engagement fields
    # --------------------------------------------------------

    posts["likes"] = pd.to_numeric(
        posts["likes"],
        errors="coerce",
    )

    posts["shares"] = pd.to_numeric(
        posts["shares"],
        errors="coerce",
    )

    posts["comments"] = pd.to_numeric(
        posts["comments"],
        errors="coerce",
    )

    # Track invalid likes BEFORE replacing them
    posts["likes_was_invalid"] = posts["likes"] < 0

    # Negative likes are impossible in this dataset.
    # We do NOT convert them to positive values.
    posts.loc[posts["likes"] < 0, "likes"] = np.nan

    # --------------------------------------------------------
    # Timestamp
    # --------------------------------------------------------

    posts["timestamp"] = posts["timestamp"].apply(parse_timestamp)

    # --------------------------------------------------------
    # Remove exact duplicate records
    # --------------------------------------------------------

    exact_duplicates_removed = int(posts.duplicated().sum())

    posts = posts.drop_duplicates(
        keep="first"
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Derived engagement metric
    # --------------------------------------------------------
    #
    # If likes are missing, total engagement is also unknown.
    # We therefore do NOT assume a value for likes.
    #

    posts["engagement"] = (
        posts["likes"]
        + posts["shares"]
        + posts["comments"]
    )

    # --------------------------------------------------------
    # Standard column ordering
    # --------------------------------------------------------

    columns = [
        "post_id",
        "user_id",
        "platform",
        "text_content",
        "timestamp",
        "likes",
        "shares",
        "comments",
        "engagement",
        "platform_was_missing",
        "text_was_missing",
        "likes_was_missing",
        "likes_was_invalid",
    ]

    posts = posts[columns]

    cleaning_stats = {
        "original_rows": original_rows,
        "final_rows": len(posts),
        "exact_duplicates_removed": exact_duplicates_removed,
        "negative_likes_converted_to_missing": int(
            posts["likes_was_invalid"].sum()
        ),
        "platform_missing_originally": int(
            posts["platform_was_missing"].sum()
        ),
        "text_missing_originally": int(
            posts["text_was_missing"].sum()
        ),
        "likes_missing_originally": int(
            posts["likes_was_missing"].sum()
        ),
        "invalid_timestamps_after_cleaning": int(
            posts["timestamp"].isna().sum()
        ),
    }

    return posts, cleaning_stats


# ============================================================
# VALIDATION
# ============================================================

def validate(users, posts):
    """Run post-cleaning validation checks."""

    checks = {
        "users_rows": len(users),
        "posts_rows": len(posts),
        "duplicate_post_ids": int(
            posts["post_id"].duplicated().sum()
        ),
        "negative_likes": int(
            (posts["likes"] < 0).sum()
        ),
        "negative_shares": int(
            (posts["shares"] < 0).sum()
        ),
        "negative_comments": int(
            (posts["comments"] < 0).sum()
        ),
        "invalid_timestamps": int(
            posts["timestamp"].isna().sum()
        ),
        "missing_platform_after_cleaning": int(
            posts["platform"].isna().sum()
        ),
    }

    # Foreign-key validation
    valid_users = set(users["user_id"].dropna())

    unknown_users = int(
        (~posts["user_id"].isin(valid_users)).sum()
    )

    checks["unknown_user_ids"] = unknown_users

    return checks


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("DATA VORTEX - DATASET 01 CLEANING")
    print("=" * 60)

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Load raw data
    # --------------------------------------------------------

    print("\nLoading raw datasets...")

    users = pd.read_csv(USERS_FILE)
    posts = pd.read_csv(POSTS_FILE)

    print(f"Users loaded: {users.shape}")
    print(f"Posts loaded: {posts.shape}")

    # --------------------------------------------------------
    # Clean
    # --------------------------------------------------------

    print("\nCleaning users...")
    users_clean = clean_users(users)

    print("Cleaning posts...")
    posts_clean, cleaning_stats = clean_posts(posts)

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    print("\nRunning validation...")
    validation = validate(
        users_clean,
        posts_clean,
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    users_clean.to_csv(
        CLEAN_USERS_FILE,
        index=False,
    )

    posts_clean.to_csv(
        CLEAN_POSTS_FILE,
        index=False,
    )

    log = {
        "input_files": {
            "users": str(USERS_FILE),
            "posts": str(POSTS_FILE),
        },
        "output_files": {
            "users": str(CLEAN_USERS_FILE),
            "posts": str(CLEAN_POSTS_FILE),
        },
        "cleaning_statistics": cleaning_stats,
        "validation": validation,
        "decisions": [
            "Raw datasets were preserved and never overwritten.",
            "Exact duplicate post records were removed.",
            "Negative likes were treated as invalid and converted to missing.",
            "Missing platform values were standardized to 'Unknown'.",
            "Missing text was retained as missing rather than fabricated.",
            "HTML entities were decoded.",
            "HTML tags were removed.",
            "Control characters were removed.",
            "Whitespace was normalized.",
            "NULL-like text values were converted to missing.",
            "Mixed timestamp formats were converted to a common datetime representation.",
            "Engagement was calculated only from available numeric values; missing likes were not fabricated."
        ],
    }

    with open(
        CLEANING_LOG_FILE,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            log,
            f,
            indent=4,
            default=str,
        )

    # --------------------------------------------------------
    # Print summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CLEANING COMPLETE")
    print("=" * 60)

    print("\nCleaning statistics:")

    for key, value in cleaning_stats.items():
        print(f"{key}: {value}")

    print("\nValidation:")

    for key, value in validation.items():
        print(f"{key}: {value}")

    print("\nOutput files:")
    print(CLEAN_USERS_FILE)
    print(CLEAN_POSTS_FILE)
    print(CLEANING_LOG_FILE)

    print("\nDone.")


if __name__ == "__main__":
    main()