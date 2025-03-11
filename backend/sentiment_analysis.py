import re
from collections import Counter
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

# ✅ Load Sentiment Analysis Model
sentiment_model = pipeline("sentiment-analysis")

# ✅ Common Stop Words
STOP_WORDS = {"the", "is", "and", "to", "a", "in", "of", "it", "this", "for", "on", "with", "that", "was", "are", "at"}

def clean_text(text):
    """Removes punctuation and converts text to lowercase."""
    text = re.sub(r'[^\w\s]', '', text.lower())  # Remove punctuation
    words = text.split()
    words = [word for word in words if word not in STOP_WORDS and len(word) > 2]  # Remove stop words and short words
    return words

def analyze_single_comment(comment):
    """Analyzes sentiment of a single comment."""
    if "comment" not in comment or not comment["comment"].strip():
        return None
    
    text = comment["comment"].strip()  # Remove extra spaces
    
    # ✅ Fix: Truncate long comments properly (limit to 512 tokens)
    words = text.split()[:512]  # Takes only first 512 words
    truncated_text = " ".join(words)  # Joins back to a string
    
    try:
        sentiment = sentiment_model(truncated_text)[0]['label']
    except Exception as e:
        print("Error analyzing comment:", truncated_text, "| Error:", str(e))
        sentiment = "ERROR"

    return {"user": comment["user"], "comment": truncated_text, "sentiment": sentiment}

def analyze_sentiment(comments):
    positive_count = 0
    negative_count = 0
    word_list = []

    # ✅ Use ThreadPoolExecutor for Parallel Processing
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(analyze_single_comment, comments))

    results = [res for res in results if res is not None]

    for res in results:
        if res["sentiment"] == "POSITIVE":
            positive_count += 1
        else:
            negative_count += 1

        word_list.extend(clean_text(res["comment"]))

    # ✅ Find the most common words for the word cloud
    word_counts = Counter(word_list).most_common(30)  # Get top 30 words

    return {
        "results": results,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "word_cloud": dict(word_counts)  # Convert to dictionary for frontend
    }
