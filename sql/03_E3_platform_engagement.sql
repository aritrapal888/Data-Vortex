-- E3 — Average Engagement by Platform
-- Calculate average likes, shares, comments and total engagement
-- for each platform.
-- Posts with missing likes are excluded from engagement averages.

SELECT
    platform,
    COUNT(*) AS post_count,
    ROUND(AVG(likes), 2) AS avg_likes,
    ROUND(AVG(shares), 2) AS avg_shares,
    ROUND(AVG(comments), 2) AS avg_comments,
    ROUND(AVG(engagement), 2) AS avg_total_engagement
FROM posts
WHERE likes IS NOT NULL
  AND engagement IS NOT NULL
GROUP BY platform
ORDER BY avg_total_engagement DESC;