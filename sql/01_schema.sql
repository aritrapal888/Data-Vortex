PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    location TEXT NOT NULL,
    language TEXT NOT NULL,
    account_created DATE NOT NULL,
    follower_count INTEGER NOT NULL CHECK (follower_count >= 0)
);

CREATE TABLE posts (
    post_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    platform TEXT NOT NULL,
    text_content TEXT,
    timestamp DATETIME NOT NULL,
    likes INTEGER,
    shares INTEGER NOT NULL CHECK (shares >= 0),
    comments INTEGER NOT NULL CHECK (comments >= 0),
    engagement INTEGER,
    platform_was_missing INTEGER NOT NULL DEFAULT 0,
    text_was_missing INTEGER NOT NULL DEFAULT 0,
    likes_was_missing INTEGER NOT NULL DEFAULT 0,
    likes_was_invalid INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX idx_posts_user_id
    ON posts(user_id);

CREATE INDEX idx_posts_platform
    ON posts(platform);