#!/usr/bin/env python3

import bcrypt
import json
import os
import subprocess
import sys

sys.path.append('lib/')

from charmhelpers.core.hookenv import action_fail, action_get, action_set
from charmhelpers.core.host import chownr, pwgen


def add_user(args):
    options = action_get()
    password = options.get('password', None)
    if not password:
        password = pwgen(16)
    hashed = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    opts = {
        'password': hashed,
        'log': True,
        'awayMessage': '',
        'networks': [],
        'sessions': [],
        'clientSettings': {}
    }
    path = '/etc/thelounge/users/{}.json'.format(options['user'])
    with open(path, 'w+') as f:
        f.write(json.dumps(opts, indent=4))
    chownr(path, 'thelounge', 'thelounge')
    action_set({
        'password': password,
        'user': options['user'],
    })


def list_users(args):
    action_set({
        'users': subprocess.check_output(
            ['sudo', '-u', 'thelounge', 'thelounge', 'list']).decode('utf-8')
    })


def delete_user(args):
    try:
        subprocess.check_call([
            'sudo', '-u', 'thelounge',
            'thelounge', 'remove', action_get('user')])
    except subprocess.CalledProcessError as e:
        action_fail(e)
        return
    action_set({
        'success': True,
    })


# A dictionary of all the defined actions to callables (which take
# parsed arguments).
ACTIONS = {
    "add-user": add_user,
    'delete-user': delete_user,
    'list-users': list_users,
}


def main(args):
    action_name = os.path.basename(args[0])
    try:
        action = ACTIONS[action_name]
    except KeyError:
        return "Action %s undefined" % action_name
    else:
        try:
            action(args)
        except Exception as e:
            action_fail(str(e))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
