class Config():
    CLIENT_ID = ""
    CLIENT_SECRET = ""
    API_KEY = ""

    REDIRECT_HOSTNAME = "localhost"
    REDIRECT_PORT = 8080
    REDIRECT_CALLBACK = "callback"

    REDIRECT_URI = f"http://{REDIRECT_HOSTNAME}:{REDIRECT_PORT}/{REDIRECT_CALLBACK}"

    REQUIRED_SCOPES = [
        "wait_read",
        "wait_write",
        "coll_read",
        "coll_write",
        "notes_read",
        "notes_write"
    ]

    ITAD_URI = "https://isthereanydeal.com"
    ITAD_API_URI = "https://api.isthereanydeal.com"