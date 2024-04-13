import asyncio
import csv
from tweety import Twitter
from typing import Dict
import json
import jmespath
from scrapfly import ScrapeConfig, ScrapflyClient
from loguru import logger as log

# Note this is my my personal config.py file that has been git ignorned because it has sensitive data
from config import twitter_username, twitter_password, scrapfly_key

# Initialize Twitter session
app = Twitter("session")
app.sign_in(twitter_username, twitter_password)

# Initialize Scrapfly client
SCRAPFLY = ScrapflyClient(key=scrapfly_key)


# Base configuration for scraping
BASE_CONFIG = {
    "asp": True,  # Anti Scraping Protection bypass feature
    "render_js": True,  # Use headless browsers for scraping
}

# Exception class for Twitter web app crashes
class TwitterWebAppCrashException(Exception):
    """Exception raised when the Twitter web app crashes too many times"""


# Function to scrape tweet details using Scrapfly
async def scrape_tweet(url: str) -> Dict:
    """Scrape a single tweet page for Tweet details"""

    result = await _scrape_twitter_app(url, wait_for_selector="[data-testid='tweet']")
    _xhr_calls = result.scrape_result["browser_data"]["xhr_call"]
    tweet_call = [f for f in _xhr_calls if "TweetResultByRestId" in f["url"]]
    for xhr in tweet_call:
        if not xhr["response"]:
            continue
        data = json.loads(xhr["response"]["body"])
        return parse_tweet(data['data']['tweetResult']['result'])


# Function to scrape tweet details using Scrapfly, with retry logic
async def _scrape_twitter_app(url: str, _retries: int = 0, **scrape_config) -> Dict:
    """Scrape X.com (Twitter) page and scroll to the end of the page if possible"""

    if not _retries:
        log.info("scraping {}", url)
    else:
        log.info("retrying {}/2 {}", _retries, url)
    result = await SCRAPFLY.async_scrape(
        ScrapeConfig(url, auto_scroll=True, lang=[
                     "en-US"], **scrape_config, **BASE_CONFIG)
    )
    if "Something went wrong, but" in result.content:
        if _retries > 2:
            raise TwitterWebAppCrashException(
                "Twitter web app crashed too many times")
        return await _scrape_twitter_app(url, _retries=_retries + 1, **scrape_config)
    return result


# Function to parse tweet details
def parse_tweet(data: Dict) -> Dict:
    """Parse X.com (Twitter) tweet JSON dataset for the relevant fields"""

    result = jmespath.search(
        """{
        created_at: legacy.created_at,
        favorite_count: legacy.favorite_count,
        bookmark_count: legacy.bookmark_count,
        quote_count: legacy.quote_count,
        reply_count: legacy.reply_count,
        retweet_count: legacy.retweet_count,
        quote_count: legacy.quote_count,
        text: legacy.full_text,
        is_quote: legacy.is_quote_status,
        is_retweet: legacy.retweeted,
        language: legacy.lang,
        user_id: legacy.user_id_str,
        conversation_id: legacy.conversation_id_str,
        source: source,
        views: views.count
    }""",
        data,
    )

    return result


# Function to retrieve tweets, scrape details, and save to CSV
async def retrieve_tweets_and_scrape():
    target_username = "elonmusk"
    user = app.get_user_info(target_username)
    all_tweets = app.get_tweets(user)

    with open("tweet_details.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "tweet_id", "created_at", "favorite_count", "bookmark_count", "quote_count", "reply_count",
            "retweet_count", "text", "is_quote", "is_retweet", "language",
            "user_id", "conversation_id", "source", "views",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for tweet in all_tweets:
            tweet_details = {
                "tweet_id": tweet.id,
            }

            # Scrape additional details for the tweet
            scraped_details = await scrape_tweet(tweet.url)

            if scraped_details:
                tweet_details.update(scraped_details)

            # Write tweet details to CSV
            writer.writerow(tweet_details)

# Run the retrieval, scraping, and saving process
asyncio.run(retrieve_tweets_and_scrape())
