#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.join(os.environ['CHARM_DIR'], 'lib'))

from charmhelpers.core import (
    hookenv,
)
import the_lounge as the_lounge

hooks = hookenv.Hooks()


@hooks.hook('install')
def install():
    hookenv.log('Installing the_lounge')


@hooks.hook('config-changed')
def config_changed():
    hookenv.log('Upgrading the_lounge config')
    # Do things!
    hookenv.status_set('active', 'the_lounge is ready')


@hooks.hook('start')
def start():
    hookenv.log('Starting the_lounge')


@hooks.hook('stop')
def stop():
    hookenv.log('Stopping the_lounge')


@hooks.hook('upgrade-charm')
def upgrade_charm():
    hookenv.log('Upgrading the_lounge')


@hooks.hook('update-status')
def update_status():
    hookenv.log('Checking the_lounge status')


if __name__ == "__main__":
    # execute a hook based on the name the program is called by
    hooks.execute(sys.argv)
