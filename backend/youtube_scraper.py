import requests

API_KEY = "api key"

def get_youtube_comments(video_id):
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={API_KEY}&maxResults=100"
    
    response = requests.get(url)
    
    # ✅ Print raw response to debug
    print("YouTube API Response:", response.json())  

    if response.status_code != 200:
        print("Error fetching comments:", response.json())
        return []

    data = response.json()

    # ✅ Check if 'items' exists
    if "items" not in data:
        print("No comments found or API quota exceeded.")
        return []

    comments = [
        {
            "user": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
            "comment": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        }
        for item in data["items"]
    ]
    
    return comments
