import os
import re
from dotenv import load_dotenv
import os

import googleapiclient.discovery
import googleapiclient.errors

# Load environment variables from .env file
load_dotenv()

# from the .env file
# This key was generated using the Google Console -> APIs and Services -> Credentials
# https://console.cloud.google.com/apis/api/youtube.googleapis.com/credentials
api_key = os.getenv("GOOGLE_API_KEY")  

# from the .env file
# Value in the URL of the channel
account_to_read_id: str | None = os.getenv("YOUTUBE_ACCOUNT_TO_READ")


# Set up the YouTube Data API client
api_service_name = "youtube"
api_version = "v3"


youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


video_titles = []

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

except googleapiclient.errors.HttpError as e:
    print(f"An error occurred while obtaining data from Youtube: {e}")

# Keep only values that have " ans" in them
FILTER = " ans"
video_titles = [title for title in video_titles if FILTER in title]


# Check if video_titles is empty
if len(video_titles) == 0:
    print("Youtube says that there are no videos with the given filter. Stopping.")
    exit(0)

# sanitize all video titles by replacing any of the following characters with "_" : \ / : * ? " < > | and spaces
video_titles = [re.sub(r'[\\/:*?"<>| ]', '_', title) for title in video_titles]

# Print the video titles
print("")
print(f"Found {len(video_titles)} videos:")
for title in video_titles:
    print(f"   {title}")


# get execution folder
current_folder = os.path.dirname(os.path.realpath(__file__))
DOWNLOADS_PATH = "../downloads"
downloads_folder = os.path.join(current_folder, DOWNLOADS_PATH)

# Create folder "../downloads" if it doesn't exist
if not os.path.exists(downloads_folder):
    os.mkdir(downloads_folder)


# for each value in video_titles, create a folder of the same name inside "../downloads" if it doesn't exist
folders = [os.path.join(downloads_folder, title) for title in video_titles]
for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)

# for each folder in "folders", check if there exists a mp4 file of the same name as the folder
to_download = []
print("")
for folder in folders:
    folder_name = os.path.basename(folder)
    video_file = folder_name + ".mp4"
    file_path = os.path.join(folder, video_file)
    if os.path.exists(file_path):
        print(f"  File '{video_file}' already there. Skipping.")
    else:
        to_download.append(folder_name)


# Print list of videos to download
print("")
print(f"Found {len(to_download)} videos to download:")
for title in to_download:
    print(f"   {title}")


