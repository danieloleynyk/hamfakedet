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
    logger.info('starting hamfakedet bot...')
    api_key = os.getenv("TELEGRAM_TOKEN", None)
    if not api_key:
        logger.error('no api_key')
        sys.exit(1)

    bot = HamfakedetBot(api_key)
    bot.start()


if __name__ == '__main__':
    main()
