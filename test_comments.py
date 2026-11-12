import os
import time
import ssl
import httplib2

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")

if not api_key:
    raise ValueError("YouTube API key missing in .env")

video_id = "qv9u1DX1YRk"

for attempt in range(1, 4):

    print(f"\nAttempt {attempt}/3")

    try:

        http = httplib2.Http(timeout=30)

        youtube = build(
            "youtube",
            "v3",
            developerKey=api_key,
            http=http,
            cache_discovery=False
        )

        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=10,
            textFormat="plainText"
        ).execute(num_retries=2)

        comments = response.get("items", [])

        print("Comments found:", len(comments))

        for item in comments:

            comment = item["snippet"]["topLevelComment"]["snippet"]

            print("\nAuthor:", comment.get("authorDisplayName"))
            print("Comment:", comment.get("textDisplay"))

        break

    except HttpError as error:

        print("YouTube API error:", error)
        break

    except (ssl.SSLError, httplib2.HttpLib2Error, OSError) as error:

        print("Connection error:", type(error).__name__, str(error))

        if attempt < 3:
            print("Retrying in 5 seconds...")
            time.sleep(5)

    except Exception as error:

        print("Unexpected error:", type(error).__name__, str(error))
        break