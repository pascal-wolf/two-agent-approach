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

REDIS_URL = "redis://localhost:6379"

REDIS_INDEX_NAME = "reviews-main-v5"

REDIS_SCHEMA = "redis_schema.yaml"
