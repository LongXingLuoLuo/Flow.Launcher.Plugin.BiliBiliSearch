import logging
log = logging.getLogger("BilibiliSearch")
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('log.txt')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    logger.debug('This is a debug message')
    logger.info('This is an info message')