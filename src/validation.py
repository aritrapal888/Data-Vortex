"""
Data Vortex - Independent Validation

This script validates the cleaned datasets independently of the cleaning
pipeline. It checks structural integrity, data quality, relationships,
timestamps, engagement values, and remaining text corruption.
"""

from pathlib import Path
import html
import re

import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

USERS_FILE = PROCESSED_DIR / "cleaned_users.csv"
POSTS_FILE = PROCESSED_DIR / "cleaned_posts.csv"


# ============================================================
# TEXT CHECKS
# ============================================================

def contains_html(value):
    """Check whether text still contains HTML tags."""

    if pd.isna(value):
        return False

    return bool(re.search(r"<[^>]*>", str(value)))


def contains_html_entity(value):
    """Check whether common HTML entities remain."""

    if pd.isna(value):
        return False

    text = str(value)

    # Detect encoded entities such as &amp;, &lt;, &#39;, etc.
    return bool(
        re.search(
            r"&(?:[a-zA-Z]+|#\d+|#x[0-9A-Fa-f]+);",
            text,
        )
    )


def contains_control_character(value):
    """Check for remaining control characters."""

    if pd.isna(value):
        return False

    return bool(
        re.search(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]",
            str(value),
        )
    )


# ============================================================
# VALIDATION HELPERS
# ============================================================

def check(condition, message, failures):
    """Record a failed validation check."""

    status = "PASS" if condition else "FAIL"

    print(f"[{status}] {message}")

    if not condition:
        failures.append(message)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 65)
    print("DATA VORTEX - INDEPENDENT CLEANED DATA VALIDATION")
    print("=" * 65)

    failures = []

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    users = pd.read_csv(
        USERS_FILE,
        low_memory=False,
    )

    posts = pd.read_csv(
        POSTS_FILE,
        low_memory=False,
    )

    print("\nLoaded:")
    print(f"Users: {users.shape}")
    print(f"Posts: {posts.shape}")

    # --------------------------------------------------------
    # 1. Expected structure
    # --------------------------------------------------------

    expected_user_columns = {
        "user_id",
        "location",
        "language",
        "account_created",
        "follower_count",
    }

    expected_post_columns = {
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
    }

    check(
        expected_user_columns.issubset(users.columns),
        "Users dataset contains all required columns",
        failures,
    )

    check(
        expected_post_columns.issubset(posts.columns),
        "Posts dataset contains all required columns",
        failures,
    )

    # --------------------------------------------------------
    # 2. Row counts
    # --------------------------------------------------------

    check(
        len(users) == 1500,
        "Users row count is 1,500",
        failures,
    )

    check(
        len(posts) == 12000,
        "Posts row count is 12,000 after duplicate removal",
        failures,
    )

    # --------------------------------------------------------
    # 3. Duplicate checks
    # --------------------------------------------------------

    duplicate_rows = int(posts.duplicated().sum())

    duplicate_post_ids = int(
        posts["post_id"].duplicated().sum()
    )

    check(
        duplicate_rows == 0,
        "No exact duplicate post rows remain",
        failures,
    )

    check(
        duplicate_post_ids == 0,
        "No duplicate post IDs remain",
        failures,
    )

    check(
        users["user_id"].duplicated().sum() == 0,
        "No duplicate user IDs remain",
        failures,
    )

    # --------------------------------------------------------
    # 4. User/post relationship
    # --------------------------------------------------------

    valid_user_ids = set(
        users["user_id"].dropna().astype(str)
    )

    post_user_ids = set(
        posts["user_id"].dropna().astype(str)
    )

    unknown_user_ids = post_user_ids - valid_user_ids

    check(
        len(unknown_user_ids) == 0,
        "Every post references a valid user",
        failures,
    )

    # --------------------------------------------------------
    # 5. Missing platform
    # --------------------------------------------------------

    missing_platform = int(
        posts["platform"].isna().sum()
    )

    check(
        missing_platform == 0,
        "No missing platform values remain",
        failures,
    )

    check(
        "Unknown" in set(posts["platform"]),
        "Missing platforms are represented by 'Unknown'",
        failures,
    )

    # --------------------------------------------------------
    # 6. Engagement validation
    # --------------------------------------------------------

    negative_likes = int(
        (posts["likes"] < 0).sum()
    )

    negative_shares = int(
        (posts["shares"] < 0).sum()
    )

    negative_comments = int(
        (posts["comments"] < 0).sum()
    )

    check(
        negative_likes == 0,
        "No negative likes remain",
        failures,
    )

    check(
        negative_shares == 0,
        "No negative shares remain",
        failures,
    )

    check(
        negative_comments == 0,
        "No negative comments remain",
        failures,
    )

    # --------------------------------------------------------
    # 7. Engagement calculation
    # --------------------------------------------------------

    calculated_engagement = (
        posts["likes"]
        + posts["shares"]
        + posts["comments"]
    )

    engagement_matches = (
        posts["engagement"].fillna(-1)
        == calculated_engagement.fillna(-1)
    )

    check(
        engagement_matches.all(),
        "Engagement values match likes + shares + comments",
        failures,
    )

    # --------------------------------------------------------
    # 8. Timestamp validation
    # --------------------------------------------------------

    timestamps = pd.to_datetime(
        posts["timestamp"],
        errors="coerce",
    )

    invalid_timestamps = int(
        timestamps.isna().sum()
    )

    check(
        invalid_timestamps == 0,
        "All cleaned timestamps are valid",
        failures,
    )

    if invalid_timestamps == 0:

        minimum_timestamp = timestamps.min()
        maximum_timestamp = timestamps.max()

        print(
            f"    Timestamp range: "
            f"{minimum_timestamp} → {maximum_timestamp}"
        )

    # --------------------------------------------------------
    # 9. Text corruption validation
    # --------------------------------------------------------

    html_tags_remaining = int(
        posts["text_content"]
        .apply(contains_html)
        .sum()
    )

    html_entities_remaining = int(
        posts["text_content"]
        .apply(contains_html_entity)
        .sum()
    )

    control_chars_remaining = int(
        posts["text_content"]
        .apply(contains_control_character)
        .sum()
    )

    check(
        html_tags_remaining == 0,
        "No HTML tags remain in text",
        failures,
    )

    check(
        html_entities_remaining == 0,
        "No HTML entities remain in text",
        failures,
    )

    check(
        control_chars_remaining == 0,
        "No control characters remain in text",
        failures,
    )

    # --------------------------------------------------------
    # 10. NULL-like text validation
    # --------------------------------------------------------

    def is_null_like(value):
        if pd.isna(value):
            return False

        return bool(
            re.fullmatch(
                r"(?i)null[\s&;]*",
                str(value).strip(),
            )
        )

    null_like_remaining = int(
        posts["text_content"]
        .apply(is_null_like)
        .sum()
    )

    check(
        null_like_remaining == 0,
        "No NULL-like text tokens remain as text",
        failures,
    )

    # --------------------------------------------------------
    # 11. User data validation
    # --------------------------------------------------------

    users["account_created"] = pd.to_datetime(
        users["account_created"],
        errors="coerce",
    )

    invalid_account_dates = int(
        users["account_created"].isna().sum()
    )

    check(
        invalid_account_dates == 0,
        "All user account creation dates are valid",
        failures,
    )

    check(
        (users["follower_count"] >= 0).all(),
        "Follower counts are non-negative",
        failures,
    )

    # --------------------------------------------------------
    # 12. Final missingness report
    # --------------------------------------------------------

    print("\nRemaining missing values:")

    print("\nUsers:")
    print(users.isna().sum())

    print("\nPosts:")
    print(posts.isna().sum())

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 65)

    if failures:
        print("VALIDATION RESULT: FAILED")
        print("=" * 65)

        print("\nFailed checks:")

        for failure in failures:
            print(f"- {failure}")

        raise SystemExit(1)

    else:
        print("VALIDATION RESULT: PASSED")
        print("=" * 65)
        print("\nAll independent validation checks passed.")


if __name__ == "__main__":
    main()