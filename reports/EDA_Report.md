# Data Vortex — Dataset 01 EDA Report

## 1. Executive Summary

This report presents the exploratory data analysis performed on the recovered
and cleaned Social Engine Dataset 01.

The final cleaned dataset contains:

- 1,500 unique users
- 12,000 unique posts
- 6 platform categories, including `Unknown`
- 10 user languages
- 33 user locations

The analysis examines user demographics, platform activity, posting trends,
engagement behavior, user influence, content characteristics, and anomalies.

The overall analysis indicates that platform, follower count, and text length
do not show strong relationships with average engagement in this dataset.
Posting activity remains relatively stable across the observed one-year period.

---

## 2. Dataset Overview

### Users

The cleaned users dataset contains 1,500 users and five fields:

| Column | Description |
|---|---|
| `user_id` | Unique identifier for a user |
| `location` | User's recorded location |
| `language` | User's recorded language |
| `account_created` | Account creation date |
| `follower_count` | Number of followers |

No missing values remain in the users dataset.

### Posts

The cleaned posts dataset contains 12,000 unique posts.

The main fields include:

| Column | Description |
|---|---|
| `post_id` | Unique post identifier |
| `user_id` | User who created the post |
| `platform` | Platform associated with the post |
| `text_content` | Cleaned post text |
| `timestamp` | Standardized post timestamp |
| `likes` | Valid likes value where available |
| `shares` | Number of shares |
| `comments` | Number of comments |
| `engagement` | `likes + shares + comments` when likes are available |

Additional provenance columns record whether important fields were originally
missing or invalid.

---

## 3. User Demographics

The dataset contains 10 languages distributed relatively evenly across the
1,500 users.

The largest language group is Chinese (`zh`) with 168 users, followed by
Japanese (`ja`) and Hindi (`hi`) with 156 users each.

The dataset contains 33 locations. The largest observed locations include:

- Barcelona, Spain — 56 users
- Shanghai, China — 56 users
- Los Angeles, USA — 55 users
- Munich, Germany — 54 users
- Dubai, UAE — 53 users
- Mumbai, India — 53 users

Follower counts range from 109 to 49,944.

The mean follower count is approximately 24,964, while the median is
approximately 24,741.5.

The relatively similar mean and median suggest that the follower distribution
does not appear to be dominated by a small number of extremely large accounts.

---

## 4. Platform and Posting Activity

The cleaned dataset contains six platform categories:

| Platform | Posts | Percentage |
|---|---:|---:|
| Facebook | 2,074 | 17.28% |
| YouTube | 2,073 | 17.28% |
| Twitter | 2,049 | 17.08% |
| Reddit | 2,031 | 16.93% |
| Instagram | 1,989 | 16.58% |
| Unknown | 1,784 | 14.87% |

The identified platforms have relatively similar posting volumes.

The `Unknown` category is retained because the original platform information
was unavailable for those records. These values were not fabricated.

### Monthly posting activity

Monthly post volume remains close to approximately 1,000 posts per month.

The observed monthly counts range from:

- February 2025 — 914 posts
- August 2024 — 1,015 posts

Overall, the data does not show a sustained upward or downward posting trend.

---

## 5. Engagement Analysis

Engagement is defined as:

`likes + shares + comments`

when all required values are available.

Of the 12,000 cleaned posts:

- 9,677 posts (80.64%) have known likes and therefore known engagement.
- 2,323 posts (19.36%) have unavailable likes.

Missing likes were not treated as zero because doing so would introduce
artificially low engagement values.

### Likes

For posts with available likes:

- Mean: approximately 2,493.5
- Median: approximately 2,502
- Minimum: 0
- Maximum: 5,000

### Shares

- Mean: approximately 1,007.2
- Median: approximately 1,018
- Minimum: 0
- Maximum: 2,000

### Comments

- Mean: approximately 504.3
- Median: approximately 503
- Minimum: 0
- Maximum: 1,000

### Total engagement

For posts with known engagement:

- Mean: approximately 4,006.4
- Median: approximately 4,009
- Minimum: 153
- Maximum: 7,893

The close relationship between mean and median suggests that total engagement
is not strongly dominated by extreme observations.

---

## 6. Engagement by Platform

Average total engagement is relatively similar across platforms.

| Platform | Average Engagement |
|---|---:|
| YouTube | 4,048.88 |
| Instagram | 4,040.06 |
| Facebook | 4,014.40 |
| Reddit | 4,001.24 |
| Unknown | 3,970.31 |
| Twitter | 3,958.98 |

YouTube has the highest observed average engagement, while Twitter has the
lowest.

However, the difference between platforms is relatively small. Therefore,
platform choice alone does not appear to strongly differentiate average
engagement in this dataset.

The `Unknown` category should also be interpreted separately because its
original platform information could not be recovered.

---

## 7. User Influence and Engagement

User-level statistics were calculated by joining post activity with the
cleaned user dataset.

The correlation between follower count and average post engagement is:

**-0.0042**

This is effectively zero.

Therefore, within this recovered dataset, users with larger follower counts
do not necessarily receive higher average engagement per post.

Users were also divided into follower-count quartiles. Each quartile contains
375 users.

The quartile-level engagement values remain relatively similar, reinforcing
the conclusion that follower count is not strongly associated with average
post engagement.

---

## 8. Content and Text Analysis

Of the 12,000 cleaned posts:

- 10,240 contain text
- 1,760 have missing text

Missing text was retained as missing rather than replaced with fabricated
content.

For posts with available text:

- Mean text length: approximately 117.63 characters
- Median text length: 118 characters
- Minimum text length: 6 characters
- Maximum text length: 172 characters

The correlation between text length and total engagement is:

**-0.0145**

This is effectively zero.

Therefore, the available evidence does not indicate a meaningful relationship
between post length and engagement.

---

## 9. Anomaly and Outlier Analysis

The cleaned dataset was evaluated using the 1.5 × IQR rule.

No IQR-based statistical outliers were detected for:

- Total engagement
- Likes

A small number of zero values were observed:

- 1 post with zero likes
- 5 posts with zero shares
- 13 posts with zero comments

These values were retained because zero engagement is logically valid.

The major anomalies in the original recovered data were data-quality issues
rather than statistical outliers. These included:

- Duplicate post records
- Negative likes
- Missing platform values
- Missing likes
- Missing text
- Mixed timestamp formats
- Corrupted text containing HTML entities/tags, NULL-like tokens, and control
  characters

These issues were addressed during preprocessing according to the documented
cleaning methodology.

---

## 10. Key Findings

### Finding 1 — Platform activity is broadly balanced

No identified platform dominates the recovered post volume. Each identified
platform contributes approximately 16.6%–17.3% of posts.

### Finding 2 — Platform has limited explanatory power for engagement

Average engagement varies only modestly between platforms. YouTube records the
highest average engagement, but the difference is relatively small.

### Finding 3 — Follower count is not associated with average engagement

The follower-count correlation is approximately -0.0042, effectively zero.

### Finding 4 — Text length is not associated with engagement

The text-length correlation is approximately -0.0145, also effectively zero.

### Finding 5 — Posting volume is relatively stable

Monthly posting activity stays close to 1,000 posts per month without a clear
long-term upward or downward trend.

### Finding 6 — Missing engagement data is substantial

19.36% of cleaned posts do not have usable likes and therefore cannot have
reliable total engagement calculated.

These records were retained and excluded only from analyses requiring known
engagement.

### Finding 7 — Data-quality corruption was more important than statistical
outliers

The primary reconstruction challenges involved duplicate records, invalid
negative likes, missing values, mixed timestamp representations, and corrupted
text.

After cleaning, independent validation confirmed that the cleaned dataset
contains unique post IDs, valid user relationships, non-negative engagement
values, valid timestamps, and normalized text.

---

## 11. Limitations

The analysis has several limitations.

1. Missing likes prevent reliable engagement calculations for 19.36% of posts.
2. Missing platform information prevents platform-specific interpretation for
   14.87% of posts.
3. Correlation does not establish causation.
4. The lack of association between follower count and engagement does not mean
   follower count can never influence engagement in other datasets.
5. The `Unknown` platform category represents unrecovered source information
   and should not be interpreted as an actual social-media platform.
6. Statistical outlier detection depends on the chosen method; the absence of
   IQR outliers does not prove that every observation is typical.

---

## 12. Conclusion

The recovered Social Engine dataset was successfully reconstructed,
standardized, cleaned, and validated.

The exploratory analysis shows a relatively balanced multi-platform dataset
with stable posting activity and broadly similar engagement levels across
platforms.

The strongest analytical conclusion is that neither follower count nor text
length has a meaningful linear relationship with average engagement in this
dataset.

The remaining missing values are explicitly retained where recovering the
original value would require fabrication. This preserves analytical integrity
while allowing reliable analysis of the observations with complete engagement
data.