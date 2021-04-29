import logging
import sys
import os
from hamfakedetbot import HamfakedetBot


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    api_key = os.getenv("API_KEY", None)
    port = os.getenv("PORT", 8443)
    if not api_key:
        sys.exit(1)

    heroku_url = os.getenv("HEROKU_URL", "")

    bot = HamfakedetBot(api_key)
    bot.start(url=heroku_url, port=port)


if __name__ == '__main__':
    main()
