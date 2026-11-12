import os
import json
import time
from datetime import datetime

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError(
        "YOUTUBE_API_KEY not found. Check your .env file."
    )

SEARCH_QUERY = "artificial intelligence"

MAX_SEARCH_RESULTS = 25
VIDEOS_TO_SAVE = 10

MAX_COMMENTS_PER_VIDEO = 50

OUTPUT_DIR = "data/raw/youtube"


# ============================================================
# CREATE YOUTUBE CLIENT
# ============================================================

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


# ============================================================
# SEARCH VIDEOS
# ============================================================

def search_videos():

    print("=" * 40)
    print("SEARCHING YOUTUBE")
    print("=" * 40)

    print(f"Search query: {SEARCH_QUERY}")

    request = youtube.search().list(
        part="snippet",
        q=SEARCH_QUERY,
        type="video",
        maxResults=MAX_SEARCH_RESULTS,
        order="relevance"
    )

    response = request.execute()

    video_ids = []

    for item in response.get("items", []):

        video_id = item["id"]["videoId"]

        video_ids.append(video_id)

    print(f"Candidate videos found: {len(video_ids)}")

    return video_ids


# ============================================================
# GET VIDEO DETAILS
# ============================================================

def get_video_details(video_ids):

    if not video_ids:
        return []

    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )

    response = request.execute()

    videos = []

    for item in response.get("items", []):

        snippet = item.get("snippet", {})
        statistics = item.get("statistics", {})

        video = {
            "video_id": item["id"],
            "title": snippet.get("title", ""),
            "description": snippet.get("description", ""),
            "channel_id": snippet.get("channelId", ""),
            "channel_name": snippet.get("channelTitle", ""),
            "published_at": snippet.get("publishedAt", ""),
            "view_count": int(
                statistics.get("viewCount", 0)
            ),
            "like_count": int(
                statistics.get("likeCount", 0)
            ),
            "comment_count": int(
                statistics.get("commentCount", 0)
            ),
            "comments": []
        }

        videos.append(video)

    return videos


# ============================================================
# GET COMMENTS
# ============================================================

def get_comments(video_id):

    comments = []

    next_page_token = None

    while len(comments) < MAX_COMMENTS_PER_VIDEO:

        remaining = MAX_COMMENTS_PER_VIDEO - len(comments)

        max_results = min(100, remaining)

        try:

            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                pageToken=next_page_token,
                textFormat="plainText"
            )

            response = request.execute()

        except HttpError as error:

            error_text = str(error)

            if "commentsDisabled" in error_text:

                print(
                    f"  Comments disabled: {video_id}"
                )

            else:

                print(
                    f"  Comment API error for {video_id}: "
                    f"{error}"
                )

            break

        for item in response.get("items", []):

            snippet = item["snippet"]

            top_comment = snippet["topLevelComment"]

            comment_snippet = top_comment["snippet"]

            comment = {
                "comment_id": top_comment.get("id", ""),
                "author": comment_snippet.get(
                    "authorDisplayName",
                    ""
                ),
                "author_channel_id": comment_snippet.get(
                    "authorChannelId",
                    {}
                ).get("value", ""),
                "text": comment_snippet.get(
                    "textDisplay",
                    ""
                ),
                "published_at": comment_snippet.get(
                    "publishedAt",
                    ""
                ),
                "updated_at": comment_snippet.get(
                    "updatedAt",
                    ""
                ),
                "like_count": int(
                    comment_snippet.get(
                        "likeCount",
                        0
                    )
                )
            }

            comments.append(comment)

        next_page_token = response.get(
            "nextPageToken"
        )

        if not next_page_token:
            break

        time.sleep(0.2)

    return comments


# ============================================================
# MAIN COLLECTION
# ============================================================

def collect_youtube_data():

    video_ids = search_videos()

    if not video_ids:

        print("No videos found.")

        return

    print()
    print("=" * 40)
    print("GETTING VIDEO DETAILS")
    print("=" * 40)

    videos = get_video_details(video_ids)

    print(f"Video details received: {len(videos)}")

    # Keep only the first requested number of videos.
    videos = videos[:VIDEOS_TO_SAVE]

    total_comments = 0
    videos_with_comments = 0

    print()
    print("=" * 40)
    print("COLLECTING COMMENTS")
    print("=" * 40)

    for index, video in enumerate(videos, start=1):

        print()
        print(
            f"Processing video {index}/{len(videos)}"
        )

        print(
            f"Video ID: {video['video_id']}"
        )

        comments = get_comments(
            video["video_id"]
        )

        video["comments"] = comments

        comment_count = len(comments)

        total_comments += comment_count

        if comment_count > 0:
            videos_with_comments += 1

        print(
            f"Comments collected: {comment_count}"
        )

    # ========================================================
    # FINAL DATA OBJECT
    # ========================================================

    output = {
        "metadata": {
            "collected_at": datetime.utcnow().isoformat() + "Z",
            "search_query": SEARCH_QUERY,
            "videos_requested": VIDEOS_TO_SAVE,
            "videos_saved": len(videos),
            "videos_with_comments": videos_with_comments,
            "total_comments_collected": total_comments
        },
        "videos": videos
    }

    # ========================================================
    # SAVE RAW JSON
    # ========================================================

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = os.path.join(
        OUTPUT_DIR,
        f"youtube_{timestamp}.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=2
        )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 50)
    print("YOUTUBE DATA COLLECTION COMPLETE")
    print("=" * 50)

    print(
        f"Videos saved: {len(videos)}"
    )

    print(
        f"Videos with comments: "
        f"{videos_with_comments}"
    )

    print(
        f"Total comments: {total_comments}"
    )

    print(
        f"Saved file: {output_file}"
    )

    print("=" * 50)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    collect_youtube_data()