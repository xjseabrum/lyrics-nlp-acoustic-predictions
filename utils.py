# Utility functions for the project

# Speeding up API calls
# See https://blog.devgenius.io/best-way-to-speed-up-a-bulk-of-http-requests-in-python-4ec75badabed#df95

# import asyncio
# import aiohttp
# from aiolimiter import AsyncLimiter
# limiter = AsyncLimiter(1, 0.125)

import re

def stutter_removal(lyrics:str) -> str:
    """
    Remove rhythmic `stutters` from lyrics.
    Ex: "M-M-M-My name is..." -> "My name is..."
    """
    out = re.sub(r"\S?([A-Za-z]\-)+", "", lyrics)
    return out

def remove_genius_embed(lyrics:str) -> str:
    """
    Remove the NUMBERembed that appears at the end of lyrics from Genius.
    Ex: "...yeah176Embed" -> "...yeah"
    """
    out = re.sub(r"([0-9]+)?Embed", "", lyrics)
    return out