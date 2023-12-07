import logging, os
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOGs_PATH = os.path.join(os.getcwd(),"logs",LOG_FILE.split(".")[0])
os.makedirs(LOGs_PATH,exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGs_PATH, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)