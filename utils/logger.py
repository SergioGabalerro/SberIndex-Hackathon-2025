import logging, sys, os
def get_logger(name: str = 'app'):
    lvl = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=lvl,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(name)
