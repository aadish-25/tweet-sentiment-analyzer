import re
import urllib.parse
import requests
from bs4 import BeautifulSoup


def is_url(text: str) -> bool:
    """Check if the provided string is an HTTP/HTTPS URL."""
    text = text.strip()
    return text.startswith("http://") or text.startswith("https://")


def is_tweet_url(url: str) -> bool:
    """Check if URL points to Twitter or X."""
    parsed = urllib.parse.urlparse(url.strip())
    domain = parsed.netloc.lower()
    return any(host in domain for host in ["twitter.com", "x.com"])


def fetch_tweet_from_url(url: str) -> dict:
    """
    Fetch tweet text and author details using Twitter's public oEmbed service.
    Works for public tweets without requiring API keys.
    """
    url = url.strip()
    if not is_tweet_url(url):
        return {
            "status": "error",
            "message": "URL is not a recognized Twitter/X link (e.g. https://x.com/user/status/...)",
        }

    # Normalize x.com to twitter.com for oEmbed compatibility
    normalized_url = url.replace("https://x.com/", "https://twitter.com/").replace("http://x.com/", "https://twitter.com/")
    endpoint = f"https://publish.twitter.com/oembed?url={urllib.parse.quote(normalized_url)}&omit_script=true"

    try:
        response = requests.get(endpoint, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            data = response.json()
            raw_html = data.get("html", "")
            soup = BeautifulSoup(raw_html, "html.parser")

            # Tweet body is in <p> tag within blockquote
            p_tag = soup.find("p")
            tweet_text = p_tag.get_text() if p_tag else soup.get_text()

            # Clean any trailing newlines
            tweet_text = " ".join(tweet_text.split())

            return {
                "status": "success",
                "text": tweet_text,
                "author": data.get("author_name", "Unknown"),
                "author_url": data.get("author_url", ""),
                "url": url,
            }
        elif response.status_code == 404:
            return {
                "status": "error",
                "message": "Tweet not found (404). The tweet may be private or deleted.",
            }
        else:
            return {
                "status": "error",
                "message": f"Unable to fetch tweet (HTTP {response.status_code}).",
            }
    except requests.RequestException as e:
        return {
            "status": "error",
            "message": f"Network error while connecting to Twitter: {str(e)}",
        }


def extract_tweet_input(user_input: str) -> dict:
    """
    Process user input which can be either raw text or a tweet URL.
    Returns a unified dict with 'text', 'source_type', and metadata.
    """
    clean_input = user_input.strip()
    if not clean_input:
        return {"status": "error", "message": "Input is empty."}

    if is_url(clean_input):
        result = fetch_tweet_from_url(clean_input)
        if result["status"] == "success":
            result["source_type"] = "url"
        return result

    # Direct raw text provided
    return {
        "status": "success",
        "text": clean_input,
        "author": "Direct Input",
        "author_url": "",
        "source_type": "text",
        "url": None,
    }


if __name__ == "__main__":
    sample_url = "https://x.com/jack/status/20"
    print("Testing URL fetch:", fetch_tweet_from_url(sample_url))
    print("Testing direct text:", extract_tweet_input("Loving this weather today!"))
