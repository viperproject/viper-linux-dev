from os import path

from scripts.config import *
from debian.utils import get_distribution_codename


BUILD_DIR = path.join(BUILD_DIR, 'debian')
BUILD_SCRIPT = path.join(BUILD_DIR, 'build')
COPY_SCRIPT = path.join(BUILD_DIR, 'copy')
REPOSITORY_SETUP_SCRIPT = path.join(
    BUILD_DIR, 'repository_setup')
UPLOAD_SCRIPT = path.join(BUILD_DIR, 'upload')
ARCHITECTURE = 'amd64'
DISTRIBUTION_CODENAME = get_distribution_codename()
REPOSITORY_NAME = 'deb'
