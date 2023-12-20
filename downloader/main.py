import os
import re
from dotenv import load_dotenv
import os
import subprocess

import googleapiclient.discovery
import googleapiclient.errors

from model import Video

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


videos_data = []

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
        part="contentDetails, snippet",
        playlistId=uploads_playlist_id,
        maxResults=LIMIT
    ).execute()

    
    # Extract the video titles from the response
    videos_data = [(item["snippet"]["title"], item["contentDetails"]["videoId"]) for item in playlist_items_response["items"]]

except googleapiclient.errors.HttpError as e:
    print(f"An error occurred while obtaining data from Youtube: {e}")


# get execution folder
current_folder = os.path.dirname(os.path.realpath(__file__))
DOWNLOADS_PATH = "../downloads"
downloads_folder = os.path.join(current_folder, DOWNLOADS_PATH)

# Create folder "../downloads" if it doesn't exist
if not os.path.exists(downloads_folder):
    os.mkdir(downloads_folder)



videos = []
for d in videos_data:
    video = d[0]
    video_id = d[1]
    sanitized_title = re.sub(r'[\\/:*?"<>| ]', '_', video)
    folder = os.path.join(downloads_folder, sanitized_title)
    video_file = sanitized_title + ".mp4"
    file_path = os.path.join(folder, video_file)

    video = Video(video_id, video, sanitized_title, folder, file_path)
    videos.append(video)

# Keep only values that have " ans" in them
FILTER = " ans"
videos = [video for video in videos if FILTER in video.title]


# Check if video_titles is empty
if len(videos) == 0:
    print("Youtube says that there are no videos with the given filter. Stopping.")
    exit(0)


# Print the video titles
print("")
print(f"Found {len(videos)} videos:")
for video in videos:
    print(f"   {video.title}")




# for each value in video_titles, create a folder of the same name inside "../downloads" if it doesn't exist
for folder in [v.folder for v in videos]:
    if not os.path.exists(folder):
        os.mkdir(folder)

# for each folder in "folders", check if there exists a mp4 file of the same name as the folder
to_download = []
print("")
for video in videos:
    ignorefile = os.path.join(video.folder, "ignore")
    if os.path.exists(video.file): 
        # This is actually broken because "real name" versus "sanitized name". 
        # It's OK because the downloader is smart enough and knows to skip anyways.
        print(f"  File '{video.file}' already there. Skipping.")
    elif os.path.exists(ignorefile):
        print(f"  File '{ignorefile}' exists. Skipping.")
    else:
        to_download.append(video)


# Print list of videos to download
print("")
print(f"Found {len(to_download)} videos to download:")
for video in to_download:
    print(f"   {video.title}")


# for each value in to_download, call downloader
DOWNLOADER_PATH = "../yt-dlp/yt-dlp_win.2023.11.16/yt-dlp.exe"
downloader = os.path.join(current_folder, DOWNLOADER_PATH)
if not os.path.exists(downloader):
    print(f"  File '{downloader}' does not exist. Cannot continue!")
    exit(1)


for video in to_download:
    try:
        print(f"Downloading '{video.title}'...")
        command = f"{downloader} --paths \"{video.folder}\" {video.url}"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\033[91mError while downloading '{video.title}': {e}\033[0m")
        print("\033[0m")  # Reset color to default


print("\033[92mAll done!")
print("\033[0m")  # Reset color to default
