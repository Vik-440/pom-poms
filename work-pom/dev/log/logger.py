import logging

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh_file = logging.FileHandler('pom-poms.log')
fh_file.setLevel(logging.INFO)
fh_file.setFormatter(formatter)
logger.addHandler(fh_file)