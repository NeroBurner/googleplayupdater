#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#   common.py - part of the FDroid server tools
#   Copyright (C) 2010-13, Ciaran Gultnieks, ciaran@ciarang.com
#   Copyright (C) 2013-2014 Daniel Martí <mvdan@mvdan.cc>
#   Copyright (C) 2015  Neroburner
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import sys
import re
import subprocess
import logging

from googleplay_updater_cli.asynchronousfilereader import AsynchronousFileReader

config = None
options = None
env = None


def str_compat(text):
    if sys.version_info[0] >= 3: # python 3
        return text
    else: # Python 2
        return text.encode('utf8', 'replace')


# from fdroidserver
def read_config(opts, config_file='config.py'):
    """Read the repository config

    The config is read from config_file, which is in the current directory when
    any of the repo management commands are used.
    """
    global config, options, env

    if config is not None:
        return config
    if not os.path.isfile(config_file):
        logging.critical("Missing config file - is this a repo directory?")
        sys.exit(2)

    options = opts

    config = dict()
    config['sdk_path'] = '/opt/android-sdk/'
    config['build_tools'] = '23'

    global_vars = dict()
    cfg = dict()

    logging.debug("Reading %s" % config_file)
    with io.open("config.py", "rb") as f:
        code = compile(f.read(), "config.py", 'exec')
        exec(code, None, cfg)

    # don't overwrite already set configs
    for key in cfg:
        if not (key in config):
            config[key] = cfg[key]

    # There is no standard, so just set up the most common environment
    # variables
    env = os.environ
    orig_path = env['PATH']
    for n in ['ANDROID_HOME', 'ANDROID_SDK']:
        env[n] = config['sdk_path']

    return config


class PopenResult:
    returncode = None
    output = ''


def find_sdk_tools_cmd(cmd):
    '''find a working path to a tool from the Android SDK'''

    tooldirs = []
    if config is not None and 'sdk_path' in config and os.path.exists(config['sdk_path']):
        # try to find a working path to this command, in all the recent possible paths
        if 'build_tools' in config:
            build_tools = os.path.join(config['sdk_path'], 'build-tools')
            # if 'build_tools' was manually set and exists, check only that one
            configed_build_tools = os.path.join(build_tools, config['build_tools'])
            if os.path.exists(configed_build_tools):
                tooldirs.append(configed_build_tools)
            else:
                # no configed version, so hunt known paths for it
                for f in sorted(os.listdir(build_tools), reverse=True):
                    if os.path.isdir(os.path.join(build_tools, f)):
                        tooldirs.append(os.path.join(build_tools, f))
                tooldirs.append(build_tools)
        sdk_tools = os.path.join(config['sdk_path'], 'tools')
        if os.path.exists(sdk_tools):
            tooldirs.append(sdk_tools)
    tooldirs.append('/usr/bin')
    for d in tooldirs:
        if os.path.isfile(os.path.join(d, cmd)):
            return os.path.join(d, cmd)
    # did not find the command, exit with error message
    ensure_build_tools_exists(config)


def test_sdk_exists(thisconfig):
    if 'sdk_path' not in thisconfig:
        if 'aapt' in thisconfig and os.path.isfile(thisconfig['aapt']):
            return True
        else:
            logging.error("'sdk_path' not set in config.py!")
            return False
    if not os.path.exists(thisconfig['sdk_path']):
        logging.critical('Android SDK path "' + thisconfig['sdk_path'] + '" does not exist!')
        return False
    if not os.path.isdir(thisconfig['sdk_path']):
        logging.critical('Android SDK path "' + thisconfig['sdk_path'] + '" is not a directory!')
        return False
    for d in ['build-tools']:
        if not os.path.isdir(os.path.join(thisconfig['sdk_path'], d)):
            logging.critical('Android SDK path "%s" does not contain "%s/"!' % (
                thisconfig['sdk_path'], d))
            return False
    return True


def ensure_build_tools_exists(thisconfig):
    if not test_sdk_exists(thisconfig):
        sys.exit(3)
    build_tools = os.path.join(thisconfig['sdk_path'], 'build-tools')
    versioned_build_tools = os.path.join(build_tools, thisconfig['build_tools'])
    if not os.path.isdir(versioned_build_tools):
        logging.critical('Android Build Tools path "'
                         + versioned_build_tools + '" does not exist!')
        sys.exit(3)


def SdkToolsPopen(commands, cwd=None, output=True):
    cmd = commands[0]
    if cmd not in config:
        config[cmd] = find_sdk_tools_cmd(commands[0])
    return FDroidPopen([config[cmd]] + commands[1:],
                       cwd=cwd, output=output)


def FDroidPopen(commands, cwd=None, output=True):
    """
    Run a command and capture the possibly huge output.

    :param commands: command and argument list like in subprocess.Popen
    :param cwd: optionally specifies a working directory
    :returns: A PopenResult.
    """

    global env

    if cwd:
        cwd = os.path.normpath(cwd)
        logging.debug("Directory: %s" % cwd)
    logging.debug("> %s" % ' '.join(commands))

    result = PopenResult()
    p = None
    try:
        p = subprocess.Popen(commands, cwd=cwd, shell=False, env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError as e:
        raise BuildException("OSError while trying to execute " +
                             ' '.join(commands) + ': ' + str(e))

    reader = AsynchronousFileReader(p.stdout)
    while not reader.eof():
        for line in reader.readlines():
            result.output += line.decode('utf-8')

    reader.join()

    # TODO: why do we need that?
    result.returncode = p.wait()
    return result


# from NeroBurner
def getApkInfo(apkfile):
    '''
    Parse information from a given apk-file.

    :param apkfile: path to the apk-file to get the info from
    :returns: dict with id, versioncode and version
    '''
    thisinfo = dict()
    thisinfo['id'] = 'packagename'
    thisinfo['versioncode'] = 0
    thisinfo['version'] = '0.0.0'

    name_pat = re.compile(".*name='([a-zA-Z0-9._]*)'.*")
    vercode_pat = re.compile(".*versionCode='([0-9]*)'.*")
    vername_pat = re.compile(".*versionName='([^']*)'.*")

    p = SdkToolsPopen(['aapt', 'dump', 'badging', apkfile], output=False)
    if p.returncode != 0:
        # error while executing aapt
        logging.error("Failed to get apk information, skipping " + apkfile)
        return thisinfo
    for line in p.output.splitlines():
        if line.startswith("package:"):
            try:
                thisinfo['id'] = re.match(name_pat, line).group(1)
                thisinfo['versioncode'] = int(re.match(vercode_pat, line).group(1))
                thisinfo['version'] = re.match(vername_pat, line).group(1)
            except Exception as e:
                logging.error("Package matching failed: " + str(e))
                logging.info("Line was: " + line)
                sys.exit(1)

    return thisinfo
