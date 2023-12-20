class Video:
    def __init__(self, video_id, title, sanitized_title, folder, file):
        self.video_id = video_id
        self.title = title
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.sanitized_title = sanitized_title
        self.folder=folder
        self.file=file
