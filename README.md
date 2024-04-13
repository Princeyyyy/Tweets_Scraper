# Tweet Scraper

Tweet Scraper is a Python script that leverages the Tweety and Scrapfly libraries to fetch tweets from a specific Twitter user, scrape additional details from each tweet, and save the collected data into a CSV file. This script provides a basic implementation, and with a deeper understanding of both libraries, you can develop more sophisticated applications.

## Prerequisites

Before using Tweet Scraper, ensure you have the following:

- Python installed on your system.
- Access to the Twitter API by signing up for a Twitter Account.
- Access to the Scrapfly API by creating an account on the Scrapfly website. Scrapfly offers 1000 free requests per month in their free tier.

## Requirements

Before running the script, make sure you have the following modules installed:

- asyncio
- csv
- tweety
- typing
- json
- jmespath
- scrapfly
- loguru

You can install these modules using pip:

```bash
pip install tweety scrapfly loguru
```

2. Clone the Tweet Scraper repository to your local machine:

```bash
git clone https://github.com/Princeyyyy/Tweets_Scraper.git
```

## Usage

1. **Set Up Authentication**:
   - Obtain your Twitter Account credentials (username and password) for Tweety.
   - Obtain your Scrapfly API key after creating an account on the Scrapfly website.

2. **Customize the Script**:
   - Open the `tweets_stream.py` script and update the authentication credentials for Tweety and Scrapfly.
   - Customize any other settings or parameters as needed, such as the target Twitter user and scraping configurations.

3. **Run the Script**:
   - Execute the script using Python:

```bash
python tweets_stream.py
```

4. **Review Output**:
   - The script will fetch tweets from the specified Twitter user, scrape additional details from each tweet using Scrapfly, and save the collected data into a CSV file named `tweet_details.csv`.

## Notes

- A sample csv of what the expected output is provided in the Github repository.
- Scrapfly offers 1000 free requests per month in their free tier.
- Ensure that sensitive information such as API keys and passwords are stored securely and not shared publicly.
- For more information on Tweety and Scrapfly, refer to their respective documentation:
  - Tweety: [https://github.com/mahrtayyab/tweety](https://github.com/mahrtayyab/tweety)
  - Scrapfly: [https://scrapfly.io/docs/](https://scrapfly.io/docs/)
- Feel free to ask questions if you have any and have fun with the project 😊

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.