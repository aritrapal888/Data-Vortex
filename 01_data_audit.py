import pandas as pd
import re

USERS = "data/raw/Social_Engine_Users.csv"
POSTS = "data/raw/Social_Engine_Posts_Corrupted.csv"

users = pd.read_csv(USERS)
posts = pd.read_csv(POSTS)

print("USERS:", users.shape)
print("POSTS:", posts.shape)
print("\nUsers missing:\n", users.isna().sum())
print("\nPosts missing:\n", posts.isna().sum())
print("\nExact duplicate posts:", posts.duplicated().sum())
print("Duplicate post IDs:", posts.post_id.duplicated().sum())
print("Negative likes:", (posts.likes < 0).sum())
print("Negative shares:", (posts.shares < 0).sum())
print("Negative comments:", (posts.comments < 0).sum())
print("Unknown user IDs:", (~posts.user_id.isin(set(users.user_id))).sum())

s = posts.timestamp.astype(str)
print("\nTimestamp formats:")
print("DD-MM-YYYY:", s.str.fullmatch(r"\d{2}-\d{2}-\d{4}").sum())
print("ISO:", s.str.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}").sum())
print("Unix seconds:", s.str.fullmatch(r"\d{10}").sum())

text = posts.text_content.fillna("").astype(str)
print("\nText corruption:")
print("HTML entities:", text.str.contains(r"&[A-Za-z]+;", regex=True).sum())
print("HTML tags:", text.str.contains(r"<[^>]+>", regex=True).sum())
print("NULL-like tokens:", text.str.contains(r"(?i)\bnull\b", regex=True).sum())
print("Control characters:", text.str.contains(r"[\x00-\x1f\x7f]", regex=True).sum())
