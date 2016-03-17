from scripts import config


def create_curl_script(call_type, script_path, repository_name, calls):
    with open(script_path, 'w') as fp:
        fp.write('#!/bin/bash\n')
        fp.write('set -x\n')
        fp.write('set -v\n')
        fp.write('USER={}\n'.format(config.BINTRAY_USERNAME))
        fp.write('REP={}\n'.format(repository_name))
        fp.write('API_KEY=$1\n')
        url = 'URL="https://api.bintray.com/{}/$USER/$REP"\n'.format(
            call_type)
        fp.write(url)

        for call in calls:
            url = '$URL'
            fp.write('\n')
            fp.write('curl \\\n')
            fp.write('  "-u$USER:$API_KEY" \\\n')
            for key, value in call:
                if key == "$URL":
                    url = '$URL/{}'.format(value)
                else:
                    fp.write("  {0} '{1}' \\\n".format(key, value))
            fp.write('  "{}"\n'.format(url))
            fp.write('\n')


def create_upload_script(script_path, repository_name, calls):
    create_curl_script('content', script_path, repository_name, calls)


def create_repository_setup_script(script_path, repository_name, calls):
    create_curl_script('packages', script_path, repository_name, calls)
