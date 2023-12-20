
import googleapiclient.discovery
import googleapiclient.errors

# Set up the YouTube Data API client
api_service_name = "youtube"
api_version = "v3"
api_key = "YOUR_API_KEY"  # Replace with your own API key

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

# Define the YouTube account username or channel ID
account_id = "YOUR_ACCOUNT_ID"  # Replace with the desired account username or channel ID

try:
    # Get the channel uploads playlist ID
    channels_response = youtube.channels().list(
        part="contentDetails",
        id=account_id
    ).execute()

    uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Get the most recent videos from the uploads playlist
    playlist_items_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=20
    ).execute()

    # Extract the video titles from the response
    video_titles = [item["snippet"]["title"] for item in playlist_items_response["items"]]

    # Print the video titles
    for title in video_titles:
        print(title)

except googleapiclient.errors.HttpError as e:
    print(f"An error occurred: {e}")
