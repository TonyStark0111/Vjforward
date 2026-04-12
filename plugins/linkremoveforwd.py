# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re

# Pattern to match http://, https://, t.me/, and @mentions
ALL_LINKS_PATTERN = re.compile(
    r'(https?://\S+|t\.me/\S+|@\S+)',
    re.IGNORECASE
)

def strip_all_links(text: str) -> str:
    """Remove URLs, t.me links, and @mentions."""
    if not text:
        return text
    return ALL_LINKS_PATTERN.sub('', text).strip()
