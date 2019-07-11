#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.fetch import (
    apt_install,
    filter_installed_packages,
)
from charmhelpers.core.host import (
    service_restart,
    service_resume,
    service_pause,
)
from charmhelpers.core.templating import render

from charmhelpers.core import (
    hookenv,
)
import the_lounge as the_lounge

hooks = hookenv.Hooks()


@hooks.hook('install')
def install():
    hookenv.log('Installing the_lounge')
    packages = filter_installed_packages(
        ['nodejs', 'nginx', 'python3-bcrypt']
    )
    hookenv.log("About to install {}".format(packages))
    apt_install(packages)
    the_lounge.install(the_lounge.download())


@hooks.hook('config-changed')
def config_changed():
    hookenv.log('Upgrading the_lounge config')

    config = hookenv.config()
    opts = {
        'server_name': config.get('server-name', '_'),
        'public': str(config.get('public', False)).lower(),
    }
    render('nginx.conf', '/etc/nginx/sites-enabled/thelougne.conf', opts)
    try:
        os.remove('/etc/nginx/sites-enabled/default')
    except FileNotFoundError:
        # We've already gotten around to this
        pass
    render('config.js', '/etc/thelounge/config.js', opts)
    service_restart('nginx')
    service_restart('thelounge')

    hookenv.status_set('active', 'Unit is ready')


@hooks.hook('start')
def start():
    hookenv.log('Starting the_lounge')
    service_resume('thelounge')


@hooks.hook('stop')
def stop():
    hookenv.log('Stopping the_lounge')
    service_pause('thelounge')


@hooks.hook('upgrade-charm')
def upgrade_charm():
    hookenv.log('Upgrading the_lounge')


@hooks.hook('update-status')
def update_status():
    hookenv.log('Checking the_lounge status')


if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    hooks.execute(sys.argv)
