#
# authmanager.py
#
# Copyright (C) 2008 Andrew Resch <andrewresch@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA    02110-1301, USA.
#

import os.path
import random
import stat

import deluge.component as component
import deluge.configmanager as configmanager

class AuthManager(component.Component):
    def __init__(self):
        component.Component.__init__(self, "AuthManager")
        self.auth = {}

    def start(self):
        self.__load_auth_file()

    def stop(self):
        self.auth = {}

    def shutdown(self):
        pass

    def authorize(self, username, password):
        """
        Authorizes users based on username and password

        :param username: str, username
        :param password: str, password
        :returns: True or False
        :rtype: bool

        """

        if username not in self.auth:
            return False

        if self.auth[username] == password:
            return True

        return False

    def __load_auth_file(self):
        auth_file = configmanager.get_config_dir("auth")
        # Check for auth file and create if necessary
        if not os.path.exists(auth_file):
            # We create a 'localclient' account with a random password
            try:
                from hashlib import sha1 as sha_hash
            except ImportError:
                from sha import new as sha_hash
            open(auth_file, "w").write("localclient:" + sha_hash(str(random.random())).hexdigest())
            # Change the permissions on the file so only this user can read/write it
            os.chmod(auth_file, stat.S_IREAD | stat.S_IWRITE)

        # Load the auth file into a dictionary: {username: password, ...}
        f = open(auth_file, "r")
        for line in f:
            if line.startswith("#"):
                # This is a comment line
                continue
            username, password = line.split(":")
            self.auth[username] = password
