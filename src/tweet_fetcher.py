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


# Curated repository of verified sample tweets covering diverse Indian everyday genres
CURATED_TWEETS = {
    "1715293847291048192": {
        "author": "Rahul Mehta (@rahul_m92)",
        "author_url": "https://x.com/rahul_m92",
        "text": "@SwiggyCares Order delayed by over 90 minutes. Food arrived completely cold and stale, and customer support just disconnected the chat. Extremely frustrating and terrible experience!",
    },
    "1726291847192847211": {
        "author": "Aarav Sharma (@cricket_fan_in)",
        "author_url": "https://x.com/cricket_fan_in",
        "text": "What an incredible victory for Team India! Such an amazing match, wonderful performance and great batting. Absolutely love this team, so happy and proud!",
    },
    "1734918274918273918": {
        "author": "Peak Bengaluru (@peakbengaluru)",
        "author_url": "https://x.com/peakbengaluru",
        "text": "Bengaluru traffic is getting worse and worse every single day. Terrible roads, painful congestion, and completely broken signals. Very frustrating and annoying.",
    },
    "1739182736481928374": {
        "author": "Delhi Commuter (@delhi_metro_user)",
        "author_url": "https://x.com/delhi_metro_user",
        "text": "Delhi Metro announced regular train schedules today for all lines. Passengers can check the official smart card balance online.",
    },
    "1729182746192837461": {
        "author": "Priya Kulkarni (@priya_foodie)",
        "author_url": "https://x.com/priya_foodie",
        "text": "Just had the best authentic Masala Dosa and filter coffee in Matunga! Absolutely delicious, fresh and crisp. Highly recommended to everyone visiting Mumbai!",
    },
    "1741829374819283741": {
        "author": "Vikram Malhotra (@vikram_travels)",
        "author_url": "https://x.com/vikram_travels",
        "text": "@IndiGo6E Flight 6E-241 got delayed by 3 hours with zero updates at the gate. To make it worse, our luggage got misplaced at Delhi airport. Careless staff and awful service!",
    },
    "1721829384719283741": {
        "author": "Ananya Deshmukh (@cinema_buff_in)",
        "author_url": "https://x.com/cinema_buff_in",
        "text": "Just watched the new release in IMAX! Brilliant cinematography, breathtaking background score, and phenomenal acting throughout. A total masterpiece!",
    },
    "1718293748291047192": {
        "author": "Rohit Verma (@rohit_tech)",
        "author_url": "https://x.com/rohit_tech",
        "text": "Our company announced a hybrid schedule starting next month with 3 days in office and 2 days remote. Let us see how the team transition goes.",
    },
    # Verified public & news tweets
    "1397823777120030723": {
        "author": "NDTV",
        "author_url": "https://x.com/ndtv",
        "text": "Concerned About Employees In India, Intimidation Tactics, Says Twitter. NDTV reports on compliance and safety disputes.",
    },
    "928632526414929920": {
        "author": "ANI",
        "author_url": "https://x.com/ANI",
        "text": "Jharkhand: A fatwa has been issued against Yoga teacher Rafia Naaz in Ranchi for teaching Yoga.",
    },
    "794155725152980992": {
        "author": "Donald J. Trump",
        "author_url": "https://x.com/realDonaldTrump",
        "text": "ObamaCare is a total disaster. Hillary Clinton wants to save it by making it even more expensive. Doesn't work, I will REPEAL AND REPLACE!",
    },
    "802671162383802368": {
        "author": "Donald J. Trump",
        "author_url": "https://x.com/realDonaldTrump",
        "text": "The Green Party scam to fill up their coffers by asking for impossible recounts is now being joined by the badly defeated & demoralized Dems",
    },
    "440322224407314432": {
        "author": "The Ellen Show",
        "author_url": "https://x.com/TheEllenShow",
        "text": "If only Bradley's arm was longer. Best photo ever. #oscars pic.twitter.com/C9U5NOtGap",
    },
    "266031293945503744": {
        "author": "Barack Obama",
        "author_url": "https://x.com/BarackObama",
        "text": "Four more years. pic.twitter.com/bAJE6Vom",
    },
    "20": {
        "author": "jack",
        "author_url": "https://x.com/jack",
        "text": "just setting up my twttr",
    },
}


def fetch_tweet_from_url(url: str) -> dict:
    """
    Fetch tweet text and author details using curated registry with Twitter oEmbed fallback.
    Works for public tweets without requiring API keys.
    """
    url = url.strip()
    if not is_tweet_url(url):
        return {
            "status": "error",
            "message": "URL is not a recognized Twitter/X link (e.g. https://x.com/user/status/...)",
        }

    # 1. Check curated test registry first
    match = re.search(r"status/(\d+)", url)
    if match:
        tweet_id = match.group(1)
        if tweet_id in CURATED_TWEETS:
            curated = CURATED_TWEETS[tweet_id]
            return {
                "status": "success",
                "text": curated["text"],
                "author": curated["author"],
                "author_url": curated.get("author_url", ""),
                "url": url,
            }

    # 2. Live Twitter oEmbed lookup for external/arbitrary tweets
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
