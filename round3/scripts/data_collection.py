import os
import time
from datetime import datetime, timezone

import pandas as pd
import requests
from dotenv import load_dotenv


# =========================================================
# DATA VORTEX ROUND 3
# Public Reaction to a Platform Monetisation Change
# =========================================================


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "YOUTUBE_API_KEY was not found. "
        "Check the .env file in the project root."
    )

BASE_URL = "https://www.googleapis.com/youtube/v3"

OUTPUT_FILE = (
    "round3/data/raw/platform_monetisation_reaction.csv"
)

SEARCH_QUERIES = [
    "X monetization change",
    "X creator monetization",
    "X creator revenue sharing",
    "X monetization 2026",
    "X Original Content Rewards",
]

# Number of videos requested for each search query.
VIDEOS_PER_QUERY = 25

# Maximum comments collected per video.
COMMENTS_PER_VIDEO = 100


# ---------------------------------------------------------
# YOUTUBE API HELPER
# ---------------------------------------------------------

def youtube_get(endpoint, params):
    """Send a GET request to the YouTube Data API."""

    request_params = params.copy()
    request_params["key"] = API_KEY

    response = requests.get(
        f"{BASE_URL}/{endpoint}",
        params=request_params,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"YouTube API error {response.status_code}: "
            f"{response.text[:1000]}"
        )

    return response.json()


# ---------------------------------------------------------
# SEARCH VIDEOS
# ---------------------------------------------------------

def search_videos(query, max_results=VIDEOS_PER_QUERY):
    """Search YouTube for videos related to the assigned topic."""

    data = youtube_get(
        "search",
        {
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": "date",
            "maxResults": max_results,
        },
    )

    videos = []

    for item in data.get("items", []):

        video_id = item.get("id", {}).get("videoId")

        if not video_id:
            continue

        snippet = item.get("snippet", {})

        videos.append(
            {
                "video_id": video_id,
                "video_title": snippet.get(
                    "title",
                    "",
                ),
                "video_description": snippet.get(
                    "description",
                    "",
                ),
                "video_published_at": snippet.get(
                    "publishedAt",
                    "",
                ),
                "channel_id": snippet.get(
                    "channelId",
                    "",
                ),
                "channel_title": snippet.get(
                    "channelTitle",
                    "",
                ),
                "search_query": query,
            }
        )

    return videos


# ---------------------------------------------------------
# VIDEO STATISTICS
# ---------------------------------------------------------

def get_video_statistics(video_ids):
    """
    Get statistics for videos.

    YouTube videos.list accepts a maximum of 50 IDs
    in a single request, so IDs are processed in batches.
    """

    statistics = {}

    for start in range(
        0,
        len(video_ids),
        50,
    ):

        batch = video_ids[
            start:start + 50
        ]

        print(
            f"  Statistics batch "
            f"{start + 1}-{start + len(batch)}"
        )

        data = youtube_get(
            "videos",
            {
                "part": "statistics",
                "id": ",".join(batch),
            },
        )

        for item in data.get("items", []):

            stats = item.get(
                "statistics",
                {},
            )

            statistics[item["id"]] = {
                "video_view_count": int(
                    stats.get(
                        "viewCount",
                        0,
                    )
                ),
                "video_like_count": int(
                    stats.get(
                        "likeCount",
                        0,
                    )
                ),
                "video_comment_count": int(
                    stats.get(
                        "commentCount",
                        0,
                    )
                ),
            }

        # Respect API request spacing.
        if start + 50 < len(video_ids):
            time.sleep(5)

    return statistics


# ---------------------------------------------------------
# COLLECT COMMENTS
# ---------------------------------------------------------

def collect_comments(
    video_id,
    video_info,
    max_comments=COMMENTS_PER_VIDEO,
):
    """Collect public top-level comments from a video."""

    comments = []

    page_token = None

    while len(comments) < max_comments:

        remaining = (
            max_comments
            - len(comments)
        )

        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": min(
                100,
                remaining,
            ),
            "textFormat": "plainText",
        }

        if page_token:
            params["pageToken"] = page_token

        data = youtube_get(
            "commentThreads",
            params,
        )

        items = data.get(
            "items",
            [],
        )

        if not items:
            break

        for item in items:

            top_comment = item.get(
                "snippet",
                {},
            ).get(
                "topLevelComment",
                {},
            )

            snippet = top_comment.get(
                "snippet",
                {},
            )

            comment_id = top_comment.get(
                "id"
            )

            if not comment_id:
                continue

            comments.append(
                {
                    "comment_id": comment_id,

                    "video_id": video_id,

                    "video_title": video_info.get(
                        "video_title",
                        "",
                    ),

                    "comment_text": snippet.get(
                        "textDisplay",
                        "",
                    ),

                    "comment_published_at": snippet.get(
                        "publishedAt",
                        "",
                    ),

                    "comment_updated_at": snippet.get(
                        "updatedAt",
                        "",
                    ),

                    "comment_like_count": int(
                        snippet.get(
                            "likeCount",
                            0,
                        )
                    ),

                    "comment_reply_count": int(
                        item.get(
                            "snippet",
                            {},
                        ).get(
                            "totalReplyCount",
                            0,
                        )
                    ),

                    "video_published_at": video_info.get(
                        "video_published_at",
                        "",
                    ),

                    "channel_title": video_info.get(
                        "channel_title",
                        "",
                    ),

                    "search_query": video_info.get(
                        "search_query",
                        "",
                    ),
                }
            )

            if len(comments) >= max_comments:
                break

        page_token = data.get(
            "nextPageToken"
        )

        if not page_token:
            break

        time.sleep(1)

    return comments


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print(
        "DATA VORTEX ROUND 3"
    )
    print(
        "Public Reaction to a Platform Monetisation Change"
    )
    print("=" * 60)

    collection_timestamp = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    # -----------------------------------------------------
    # 1. SEARCH FOR RELEVANT VIDEOS
    # -----------------------------------------------------

    print(
        "\nSearching YouTube..."
    )

    all_videos = {}

    for query in SEARCH_QUERIES:

        print(
            f"  Searching: {query}"
        )

        try:

            videos = search_videos(
                query
            )

            for video in videos:

                video_id = video[
                    "video_id"
                ]

                if video_id not in all_videos:
                    all_videos[
                        video_id
                    ] = video

        except RuntimeError as error:

            print(
                f"  Search failed: {error}"
            )

        # Avoid sending requests too quickly.
        time.sleep(5)

    videos = list(
        all_videos.values()
    )

    print(
        f"\nUnique videos found: "
        f"{len(videos)}"
    )

    if not videos:

        print(
            "No videos found."
        )

        return

    # -----------------------------------------------------
    # 2. GET VIDEO STATISTICS
    # -----------------------------------------------------

    print(
        "\nGetting video statistics..."
    )

    video_ids = [
        video["video_id"]
        for video in videos
    ]

    statistics = get_video_statistics(
        video_ids
    )

    for video in videos:

        stats = statistics.get(
            video["video_id"],
            {
                "video_view_count": 0,
                "video_like_count": 0,
                "video_comment_count": 0,
            },
        )

        video.update(
            stats
        )

    # -----------------------------------------------------
    # 3. COLLECT COMMENTS
    # -----------------------------------------------------

    print(
        "\nCollecting comments..."
    )

    all_comments = []

    for index, video in enumerate(
        videos,
        start=1,
    ):

        video_id = video[
            "video_id"
        ]

        print(
            f"[{index}/{len(videos)}] "
            f"{video['video_title'][:70]}"
        )

        try:

            comments = collect_comments(
                video_id,
                video,
                COMMENTS_PER_VIDEO,
            )

            all_comments.extend(
                comments
            )

            print(
                f"    Comments collected: "
                f"{len(comments)}"
            )

        except RuntimeError as error:

            print(
                f"    Skipped: {error}"
            )

        # Avoid excessive request frequency.
        time.sleep(2)

    # -----------------------------------------------------
    # 4. REMOVE DUPLICATE COMMENTS
    # -----------------------------------------------------

    if not all_comments:

        print(
            "\nNo comments were collected."
        )

        return

    df = pd.DataFrame(
        all_comments
    )

    before = len(df)

    df = df.drop_duplicates(
        subset=["comment_id"]
    ).reset_index(
        drop=True
    )

    duplicates_removed = (
        before - len(df)
    )

    print(
        f"\nDuplicate comments removed: "
        f"{duplicates_removed}"
    )

    # -----------------------------------------------------
    # 5. ADD VIDEO STATISTICS
    # -----------------------------------------------------

    video_lookup = {
        video["video_id"]: video
        for video in videos
    }

    df["video_view_count"] = (
        df["video_id"]
        .map(
            lambda x:
            video_lookup.get(
                x,
                {},
            ).get(
                "video_view_count",
                0,
            )
        )
    )

    df["video_like_count"] = (
        df["video_id"]
        .map(
            lambda x:
            video_lookup.get(
                x,
                {},
            ).get(
                "video_like_count",
                0,
            )
        )
    )

    df["video_comment_count"] = (
        df["video_id"]
        .map(
            lambda x:
            video_lookup.get(
                x,
                {},
            ).get(
                "video_comment_count",
                0,
            )
        )
    )

    # -----------------------------------------------------
    # 6. ENGAGEMENT METRICS
    # -----------------------------------------------------

    df["comment_engagement"] = (
        df["comment_like_count"]
        + df["comment_reply_count"]
    )

    df["video_engagement"] = (
        df["video_like_count"]
        + df["video_comment_count"]
    )

    # -----------------------------------------------------
    # 7. SOURCE / COLLECTION METADATA
    # -----------------------------------------------------

    df["source"] = "YouTube"

    df["collection_timestamp"] = (
        collection_timestamp
    )

    df["video_url"] = (
        "https://www.youtube.com/watch?v="
        + df["video_id"].astype(str)
    )

    # -----------------------------------------------------
    # 8. ORDER COLUMNS
    # -----------------------------------------------------

    preferred_columns = [
        "comment_id",
        "video_id",
        "video_title",
        "comment_text",
        "comment_published_at",
        "comment_updated_at",
        "comment_like_count",
        "comment_reply_count",
        "comment_engagement",
        "video_published_at",
        "video_view_count",
        "video_like_count",
        "video_comment_count",
        "video_engagement",
        "channel_title",
        "search_query",
        "source",
        "collection_timestamp",
        "video_url",
    ]

    existing_columns = [
        column
        for column in preferred_columns
        if column in df.columns
    ]

    df = df[
        existing_columns
    ]

    # -----------------------------------------------------
    # 9. SORT BY COMMENT TIME
    # -----------------------------------------------------

    df = df.sort_values(
        "comment_published_at",
        ascending=True,
    ).reset_index(
        drop=True
    )

    # -----------------------------------------------------
    # 10. SAVE DATASET
    # -----------------------------------------------------

    os.makedirs(
        os.path.dirname(
            OUTPUT_FILE
        ),
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    # -----------------------------------------------------
    # 11. SUMMARY
    # -----------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "COLLECTION COMPLETE"
    )

    print(
        "=" * 60
    )

    print(
        f"Videos found:          {len(videos)}"
    )

    print(
        f"Comments collected:    {len(df)}"
    )

    print(
        f"Unique comments:       {df['comment_id'].nunique()}"
    )

    print(
        f"Unique videos:         {df['video_id'].nunique()}"
    )

    print(
        f"Collection timestamp:  "
        f"{collection_timestamp}"
    )

    print(
        f"CSV saved to:          "
        f"{OUTPUT_FILE}"
    )

    print(
        "\nDataset columns:"
    )

    for column in df.columns:
        print(
            f"  - {column}"
        )


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main() 