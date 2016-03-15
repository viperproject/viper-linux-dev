from scripts import config


def create_upload_script(script_path, repository_name, calls):
    with open(script_path, 'w') as fp:
        fp.write('#!/bin/bash\n')
        fp.write('set -x\n')
        fp.write('set -v\n')
        fp.write('USER={}\n'.format(config.BINTRAY_USERNAME))
        fp.write('REP={}\n'.format(repository_name))
        fp.write('API_KEY=$1\n')
        url = 'URL="https://api.bintray.com/packages/$USER/$REP"\n'
        fp.write(url)

        for call in calls:
            fp.write('\n')
            fp.write('curl \\\n')
            fp.write('  "-u$USER:$API_KEY" \\\n')
            for key, value in call:
                if key == "$URL":
                    fp.write('  "$URL/{}" \\\n'.format(value))
                else:
                    fp.write("  {0} '{1}' \\\n".format(key, value))
            fp.write('  "$URL"\n')
            fp.write('\n')
