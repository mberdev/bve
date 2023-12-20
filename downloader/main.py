import os
from dotenv import load_dotenv

import googleapiclient.discovery
import googleapiclient.errors

# Load environment variables from .env file
load_dotenv()

# Set up the YouTube Data API client
api_service_name = "youtube"
api_version = "v3"

# from the .env file
# This key was generated using the Google Console -> APIs and Services -> Credentials
# https://console.cloud.google.com/apis/api/youtube.googleapis.com/credentials
api_key = os.getenv("GOOGLE_API_KEY")  

# from the .env file
# Value in the URL of the channel
account_to_read_id: str | None = os.getenv("YOUTUBE_ACCOUNT_TO_READ")


youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)



try:
    # Get the channel uploads playlist ID
    channels_response = youtube.channels().list(
        part="contentDetails",
        id=account_to_read_id
    ).execute()

    uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Get the most recent videos from the uploads playlist
    LIMIT = 40
    playlist_items_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=LIMIT
    ).execute()

    # Extract the video titles from the response
    video_titles = [item["snippet"]["title"] for item in playlist_items_response["items"]]

    # Print the video titles
    for title in video_titles:
        print(title)

    # Keep only values that have " ans" in them
    FILTER = " ans"
    video_titles = [title for title in video_titles if FILTER in title]

    # get execution folder
    current_folder = os.path.dirname(os.path.realpath(__file__))
    DOWNLOADS_PATH = "../downloads"
    downloads_folder = os.path.join(current_folder, DOWNLOADS_PATH)

    # Create folder "../downloads" if it doesn't exist
    if not os.path.exists(downloads_folder):
        os.mkdir(downloads_folder)


except googleapiclient.errors.HttpError as e:
    print(f"An error occurred: {e}")
