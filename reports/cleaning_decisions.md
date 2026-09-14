# Data Vortex — Dataset 01 Cleaning Decisions

## 1. Objective

The recovered Social Engine Dataset 01 contained missing values, duplicate
records, invalid engagement values, mixed timestamp formats, and corrupted
text. The objective of this cleaning process was to standardize the data while
preserving the original information and avoiding fabricated values.

The raw recovered files were preserved and were not overwritten.

---

## 2. Duplicate Records

### Finding

The recovered posts dataset contained 12,360 rows but only 12,000 unique
post IDs.

There were 360 exact duplicate rows.

### Decision

Exact duplicate records were removed, keeping the first occurrence.

### Reason

The duplicated records contained identical values across all fields.
Keeping multiple copies would artificially inflate post counts and engagement
statistics.

### Result

12,360 rows → 12,000 rows.

---

## 3. Negative Likes

### Finding

The recovered dataset contained negative values in the `likes` field.

### Decision

Negative likes were treated as invalid values and converted to missing
values (`NaN`).

### Reason

A negative like count is not a valid engagement count. The negative value
was not converted to a positive number because doing so would invent a value
that was not present in the recovered data.

### Result

No negative likes remain in the cleaned dataset.

---

## 4. Missing Platform Values

### Finding

Some posts did not contain a platform value.

### Decision

Missing platform values were standardized to:

`Unknown`

### Reason

Platform is categorical metadata. Replacing a missing category with
`Unknown` preserves the record without falsely assigning it to a specific
platform.

---

## 5. Missing Text

### Finding

Some posts had missing text content.

### Decision

Missing text was retained as missing rather than generating or guessing
content.

### Reason

The original text cannot be reliably reconstructed from the available
dataset. Fabricating text would compromise the integrity of the analysis.

---

## 6. Corrupted Text

The recovered text contained several forms of corruption.

### HTML entities

HTML entities were decoded.

Example:

`&amp;` → `&`

### HTML tags

HTML markup was removed while preserving the surrounding text.

### Control characters

Non-printing control characters were removed.

### Whitespace

Repeated whitespace was normalized.

### NULL-like values

Values representing missing text, such as `NULL`, were treated as missing
after other text-cleaning operations.

### Reason

These transformations standardize the textual representation without
inventing new content.

---

## 7. Timestamp Standardization

### Finding

The recovered posts contained three timestamp representations:

- DD-MM-YYYY format
- ISO-style datetime format
- Unix timestamp in seconds

### Decision

All supported timestamp representations were converted into a common
datetime representation.

Unix timestamps were interpreted as UTC before the timezone information
was removed for consistency with the timezone-naive dataset.

### Validation

No invalid timestamps remained after conversion.

---

## 8. Shares and Comments

No negative values were found in `shares` or `comments`.

Therefore, no negative-value correction was required for these fields.

Their original numeric values were retained.

---

## 9. User Relationships

Every post referenced a valid user ID from the users dataset.

Therefore, no post records were removed because of invalid user references.

---

## 10. Engagement Metric

A derived `engagement` field was created:

`engagement = likes + shares + comments`

When likes is missing, total engagement remains unavailable rather than
assuming or fabricating a likes value.

---

## 11. Data Provenance

The following files are maintained separately:

- `data/raw/Social_Engine_Users.csv`
- `data/raw/Social_Engine_Posts_Corrupted.csv`

Cleaned outputs are stored separately:

- `data/processed/cleaned_users.csv`
- `data/processed/cleaned_posts.csv`

The cleaning process is reproducible using:

`src/cleaning.py`

A machine-readable record of cleaning statistics and decisions is stored in:

`data/processed/cleaning_log.json`