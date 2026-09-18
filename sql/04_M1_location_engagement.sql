-- M1 — Which Locations Generate the Most Engagement?
-- Join users and posts, aggregate engagement by location,
-- and rank locations from highest to lowest total engagement.

SELECT
    u.location,
    COUNT(p.post_id) AS post_count,
    SUM(p.engagement) AS total_engagement
FROM users AS u
INNER JOIN posts AS p
    ON u.user_id = p.user_id
WHERE p.engagement IS NOT NULL
GROUP BY u.location
ORDER BY total_engagement DESC;