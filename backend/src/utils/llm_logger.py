import logging

# Create a logger with the name 'app'
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Set up logging to display logs on console and write them to a file
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# File handler
fh = logging.FileHandler("../app.log")
fh.setFormatter(formatter)
logger.addHandler(fh)

LOGGER = logger
