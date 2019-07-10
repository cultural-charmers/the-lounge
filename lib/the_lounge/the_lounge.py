import subprocess
import urllib.request


def download():
    url = ("https://github.com/thelounge/thelounge/releases/"
           "download/v3.0.1/thelounge_3.0.1-1_all.deb")
    file_name, headers = urllib.request.urlretrieve(url)
    return file_name


def install(deb_path):
    try:
        subprocess.check_call(['dpkg', '-i', deb_path])
    except subprocess.CalledProcessError as e:
        logging.warning('Failed to install thelounge: {}'.format(e))
        raise RuntimeError('Failed to install thelounge: {}'.format(e))