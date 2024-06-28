MAPPINGS = {
    "chatgpt": {
        "userName": "name",
        "content": "content",
        "score": "score",
        "thumbsUpCount": "likes",
        "at": "created_date",
    },
    "netflix": {
        "created": "created_date",
        "content": "content",
        "score": "score",
        "likes": "likes",
    },
    "spotify": {
        "Time_submitted": "created_date",
        "Review": "content",
        "Rating": "score",
        "Total_thumbsup": "likes",
    },
}

DATA_ROOT = "data"


# reviewId, userName, content, score, thumbsUpCount, reviewCreatedVersion, at, appVersion
# id, name, content, score, likes, created, at, version
# Time_submitted, Review, Rating, Total_thumbsup, Reply
