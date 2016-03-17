from os import path

from scripts.config import *


BUILD_DIR = path.join(BUILD_DIR, 'homebrew')
REPOSITORY_SETUP_SCRIPT = path.join(
    BUILD_DIR, 'repository_setup')
UPLOAD_SCRIPT = path.join(BUILD_DIR, 'upload')
REPOSITORY_NAME = 'generic'
