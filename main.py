import logging
import sys
import os
from bot import Bot


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    api_key = os.getenv("API_KEY", None)
    if not api_key:
        sys.exit(1)

    heroku_url = os.getenv("HEROKU_URL", "")
    port = os.getenv("PORT", 5000)

    bot = Bot(api_key)
    bot.start(port, heroku_url)


if __name__ == '__main__':
    main()
