#!/usr/bin/python3


class License:
    """ Information about a license.

    +   ``short_name`` – name accepted by https://bintray.com/ API.
    """

    def __init__(self, short_name, full_name, url):
        self.short_name = short_name
        self.full_name = full_name
        self.url = url


class Package:
    """ Information about a package that is idenpendent from the format
    used.

    +   ``name`` – name of package.
    +   ``license`` – a tuple of all licenses under which the content
        of package is licensed. Note that if content is double-licensed,
        only one license should be chosen.
    +   ``vcs_url`` – URL of the repository where the source code is
        hosted.
    +   ``omit`` – True if this package should not be included in the
        repository.
    """

    def __init__(self, name, licenses, vcs_url=None, omit=False):
        if vcs_url is None and not omit:
            raise Exception("Invalid package: {0}.".format(name))
        self.full_name = name
        try:
            self.licenses = tuple(licenses)
        except TypeError:
            self.licenses = licenses,
        self.prefix, self.name, self.version = name.split(' # ')
        self.version = self.version.replace('-SNAPSHOT', '.0')
        if self.prefix:
            self.long_name = '{}.{}'.format(self.prefix, self.name)
        else:
            self.long_name = self.name
        self.vcs_url = vcs_url
        self.omit = omit

    def check(self, file_name):
        return file_name.startswith(self.long_name)
