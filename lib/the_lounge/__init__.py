import logging
import subprocess
import urllib.request
from charmhelpers.core.hookenv import (
    config,
    log
)


def download():
    url = config()['source']
    log("About to download {}".format(url))
    file_name, headers = urllib.request.urlretrieve(url)
    log("Downloaded to {}".format(file_name))
    return file_name


def install(deb_path):
    try:
        log("About to install the file at {}".format(deb_path))
        subprocess.check_call(['dpkg', '-i', deb_path])
    except subprocess.CalledProcessError as e:
        logging.warning('Failed to install thelounge: {}'.format(e))
        raise RuntimeError('Failed to install thelounge: {}'.format(e))
