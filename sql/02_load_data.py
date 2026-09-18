import csv
import sqlite3
from pathlib import Path

# Project root = folder containing this script's parent directory
BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "sql" / "data_vortex.db"
SCHEMA_PATH = BASE_DIR / "sql" / "01_schema.sql"

USERS_CSV = BASE_DIR / "data" / "processed" / "cleaned_users.csv"
POSTS_CSV = BASE_DIR / "data" / "processed" / "cleaned_posts.csv"


def clean_value(value):
    """Convert empty CSV values to None for SQLite NULL."""
    if value is None:
        return None

    value = value.strip()

    return value if value != "" else None


def to_int(value):
    """Convert numeric and boolean-like CSV values to integers."""
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    if value.lower() == "true":
        return 1

    if value.lower() == "false":
        return 0

    return int(float(value))


def main():
    print("Starting Data Vortex SQL database setup...")

    # Remove old database so the process is reproducible.
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("Removed previous database.")

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON;")

        # Create tables and indexes.
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)

        print("Schema created successfully.")

        # -------------------------
        # Load Users
        # -------------------------
        with USERS_CSV.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            users = [
                (
                    row["user_id"],
                    row["location"],
                    row["language"],
                    row["account_created"],
                    to_int(row["follower_count"]),
                )
                for row in reader
            ]

        connection.executemany(
            """
            INSERT INTO users (
                user_id,
                location,
                language,
                account_created,
                follower_count
            )
            VALUES (?, ?, ?, ?, ?);
            """,
            users,
        )

        print(f"Loaded {len(users):,} users.")

        # -------------------------
        # Load Posts
        # -------------------------
        with POSTS_CSV.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            posts = []

            for row in reader:
                posts.append(
                    (
                        row["post_id"],
                        row["user_id"],
                        row["platform"],
                        clean_value(row["text_content"]),
                        row["timestamp"],
                        to_int(row["likes"]),
                        to_int(row["shares"]),
                        to_int(row["comments"]),
                        to_int(row["engagement"]),
                        to_int(row["platform_was_missing"]),
                        to_int(row["text_was_missing"]),
                        to_int(row["likes_was_missing"]),
                        to_int(row["likes_was_invalid"]),
                    )
                )

        connection.executemany(
            """
            INSERT INTO posts (
                post_id,
                user_id,
                platform,
                text_content,
                timestamp,
                likes,
                shares,
                comments,
                engagement,
                platform_was_missing,
                text_was_missing,
                likes_was_missing,
                likes_was_invalid
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            posts,
        )

        connection.commit()

        print(f"Loaded {len(posts):,} posts.")

        # -------------------------
        # Validation
        # -------------------------
        user_count = connection.execute(
            "SELECT COUNT(*) FROM users;"
        ).fetchone()[0]

        post_count = connection.execute(
            "SELECT COUNT(*) FROM posts;"
        ).fetchone()[0]

        invalid_users = connection.execute(
            """
            SELECT COUNT(*)
            FROM posts p
            LEFT JOIN users u
                ON p.user_id = u.user_id
            WHERE u.user_id IS NULL;
            """
        ).fetchone()[0]

        duplicate_post_ids = connection.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT post_id
                FROM posts
                GROUP BY post_id
                HAVING COUNT(*) > 1
            );
            """
        ).fetchone()[0]

        print("\nDATABASE VALIDATION")
        print("-------------------")
        print(f"Users: {user_count:,}")
        print(f"Posts: {post_count:,}")
        print(f"Posts with invalid user_id: {invalid_users}")
        print(f"Duplicate post IDs: {duplicate_post_ids}")

        if user_count != 1500:
            raise ValueError("Expected exactly 1,500 users.")

        if post_count != 12000:
            raise ValueError("Expected exactly 12,000 posts.")

        if invalid_users != 0:
            raise ValueError("Found posts referencing unknown users.")

        if duplicate_post_ids != 0:
            raise ValueError("Found duplicate post IDs.")

        print("\nSUCCESS: SQL database created and validated.")
        print(f"Database: {DB_PATH}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()