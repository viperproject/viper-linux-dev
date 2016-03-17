import json


from scripts import config
from scripts.uploader import create_repository_setup_script as cr


def create_repository_setup_script(
        packages,
        repository_setup_script,
        repository_name):
    """ Creates a shell script that creates packages on BinTray
    repository.
    """
    calls = [
        (
          ('-X', 'POST'),
          ('-H', 'Content-Type: application/json'),
          ('-d', json.dumps({
                'name': package.package.long_name,
                'desc': package.short_description,
                'licenses': [
                    license.short_name
                    for license in package.package.licenses
                    ],
                'vcs_url': package.package.vcs_url,
                }))
          )
        for package in packages
        if not package.package.omit
        ]
    cr(
        repository_setup_script,
        repository_name,
        calls)
