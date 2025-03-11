from fastapi import FastAPI
from pydantic import BaseModel
from youtube_scraper import get_youtube_comments
from sentiment_analysis import analyze_sentiment
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Pydantic Model for Requests
class CommentRequest(BaseModel):
    comments: list

@app.get("/")
def home():
    return {"message": "YouTube Sentiment Analysis API"}

@app.get("/fetch_comments")
def fetch_comments(video_id: str):
    if len(video_id) != 11 or "https" in video_id or "/" in video_id:
        return {"error": "Invalid video ID. Please provide only the 11-character video ID."}

    comments = get_youtube_comments(video_id)
    return {"comments": comments if comments else "No comments found"}

@app.post("/analyze")
def analyze(request: CommentRequest):
    if not request.comments:
        return {"error": "No comments provided for analysis"}
    
    print("Incoming Comments for Analysis:", request.comments)  # ✅ Debugging Log
    
    try:
        return analyze_sentiment(request.comments)
    except Exception as e:
        print("Error in Sentiment Analysis:", str(e))  # ✅ Log any errors
        return {"error": "Internal Server Error during sentiment analysis"}

