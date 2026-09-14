# Data Vortex — Dataset 01 Forensic Data Audit

## Source files

- `Social_Engine_Users.csv`
- `Social_Engine_Posts_Corrupted.csv`

**Important:** The two original files should remain unchanged and be treated as RAW evidence.

## Executive summary

The Users table is structurally clean and can be used as a reference table. The Posts table is intentionally corrupted and contains duplicate records, missing values, invalid engagement values, mixed timestamp encodings, and text-formatting corruption.

### Users

- Rows: **1,500**
- Columns: **5**
- Duplicate rows: **0**
- Duplicate `user_id`: **0**
- Missing values: **0**
- Invalid `account_created` dates: **0**
- Follower count range: **109 – 49,944**
- Languages: **10**
- Locations: **33**

### Posts

- Rows: **12,360**
- Unique `post_id`: **12,000**
- Exact duplicate rows: **360**
- `post_id` values appearing more than once: **352**
- Missing platform: **1,846**
- Missing text: **1,746**
- Missing likes: **1,858**
- Negative likes: **525**
- Negative shares: **0**
- Negative comments: **0**
- Unknown `user_id` values: **0**

### Timestamp corruption

All timestamps fall into one of three detectable representations:

- DD-MM-YYYY: **3,622**
- ISO-8601: **4,950**
- Unix seconds: **3,788**

After format-aware parsing, the valid range is **2024-05-01 through 2025-04-30**, with no unparseable timestamps.

### Text corruption

Detected:

- HTML entities: **341**
- HTML tags: **663**
- NULL-like tokens: **0**
- Control characters: **10,614**
- Multiple whitespace sequences: **0**

## Recommended cleaning decisions

These are **recommendations for review**, not yet applied:

1. Preserve both original CSVs unchanged.
2. Remove exact duplicate post rows after recording the duplicate count.
3. For duplicated `post_id` values, verify that the duplicated records are identical before keeping one record per post.
4. Parse all timestamp formats into one canonical datetime column.
5. Treat negative likes as invalid/missing rather than converting `-x` to `x`; converting the sign would fabricate a value.
6. Keep missing text missing unless a defensible reconstruction rule exists.
7. Normalize text by decoding HTML entities, removing markup tags, normalizing whitespace, and converting explicit NULL markers to missing where appropriate.
8. Handle missing platform explicitly rather than guessing the platform.
9. Validate that every post `user_id` exists in the Users table.
10. Re-run all quality checks after cleaning and document every transformation.

## Important anomaly principle

A statistical outlier is not automatically a data error. For example, a post with extremely high engagement may be a legitimate viral post. Invalid values such as negative likes should be treated as data-quality errors.

## Next phase

After approving the cleaning rules:

**RAW → CLEANING → VALIDATION → EDA → REPORT → GITHUB → SUBMISSION**

