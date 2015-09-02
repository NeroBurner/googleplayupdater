#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
from __future__ import print_function
from __future__ import absolute_import

import os, sys
import logging
import argparse

import config # user-credentials

from ext_libs.googleplay_api.googleplay import GooglePlayAPI #GooglePlayAPI
from ext_libs.googleplay_api.googleplay import LoginError
from ext_libs.androguard.core.bytecodes import apk as androguard_apk #Androguard

def connect():
    api = GooglePlayAPI(androidId=config.ANDROID_ID, lang=config.LANG)
    try :
        api.login(config.GOOGLE_LOGIN, config.GOOGLE_PASSWORD, config.AUTH_TOKEN)
    except LoginError, exc:
        logging.error("Connection to PlayStore failed: %s" % exc)
        return None

    logging.info("Connection to GooglePlayStore established")
    return api

def update(playstore_api, apk_folder_path):
    # search for apks in given folder
    list_of_apks = [filename for filename in os.listdir(apk_folder_path) if os.path.splitext(filename)[1] == ".apk"]
    if len(list_of_apks) <= 0:
        print("No apks found in folder %s" % apk_folder_path)
        sys.exit(0)

    # create a list of apks, just keep the newest
    apks_to_update = dict()
    for filename in list_of_apks:
        filepath = os.path.join(apk_folder_path, filename)
        a = androguard_apk.APK(filepath)
        apk_version_code = int(a.get_androidversion_code())
        packagename = a.get_package()

        logging.info("Found apk %s : %s : %d" % (filepath, packagename, apk_version_code))

        if packagename in apks_to_update:
            if apks_to_update[packagename] < apk_version_code:
                logging.info("Found newer local version %s : %d -> %d" % (packagename, apks_to_update[packagename], apk_version_code))
                apks_to_update[packagename] = apk_version_code

        else:
            logging.info("Set new  local apk %s : %d" % (packagename, apk_version_code))
            apks_to_update[packagename] = apk_version_code

    # are there still apks to check? If not something went wrong
    if len(apks_to_update) <= 0:
        logging.error("No apks to update after non-empty apk-list. Something went wrong!")
        sys.exit(1)

    # search for the apks on googleplaystore
    for packagename, version_code in apks_to_update.items():
        local_version_code = int(version_code)
        logging.info("Checking apk %s : %d" % (packagename, local_version_code))

        # get infos of the store-version
        m = playstore_api.details(packagename)
        doc = m.docV2
        store_version_code = int(doc.details.appDetails.versionCode)

        if store_version_code == 0:
            logging.warning("Got store_version_code == 0 for package %s : %d" % (packagename, local_version_code))
            continue

        # check if there is an update
        if store_version_code > local_version_code:
            # download apk from store
            print("Updating apk %s : %d -> %d" % (packagename, local_version_code, store_version_code))
            try:
                data = playstore_api.download(packagename, store_version_code)
            except Exception as exc:
                logging.error("failed to download %s : %s" % (packagename, exc))
                continue
            else:
                # save downloaded apk under '<packagename>_<version>.apk'
                filename = "%s_%d.apk" % (packagename, store_version_code)
                filepath = os.path.join(apk_folder_path, filename)

                try:
                    open(filepath, "wb").write(data)
                except IOError, exc:
                    logging.error("cannot write to disk %s : %s" % (packagename, exc))
                    continue
                logging.info("Downloaded apk %s : %d to file %s" % (packagename, store_version_code, filename))
        else:
            logging.info("No newer apk found.")

def synopsis():
    print("Usage: %s [-v] <apk_folder_path>" % sys.argv[0])
    print("\t-v\t verbose output")

def main():
    global config, options

    # Parse command line...
    parser = argparse.ArgumentParser(description='Fetch updates for local apks from GooglePlayStore')
    parser.add_argument('apk_folder_path',
            help='absolute or relative path to folder containing the apks to update')
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
            help="be more verbose")
    # TODO: --config flag
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    # get apk_folder_path
    if not os.path.isdir(args.apk_folder_path):
        logging.error("given <apk_folder_path> is not a directory: %s" % args.apk_folder_path)
        parser.print_help()
        sys.exit(1)

    # connect to Google Play Store
    playstore_api = connect()
    if playstore_api == None:
        logging.error("Connection to PlayStore failed. Check provided credencials in config.py")
        sys.exit(1)

    # update local apks
    update(playstore_api, args.apk_folder_path)

if __name__ == '__main__':
    main()


