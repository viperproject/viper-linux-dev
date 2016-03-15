import platform


def get_distribution_codename():
    """ A helper function for getting distribution codename
    """
    distname, version, codename = platform.linux_distribution()
    return codename
