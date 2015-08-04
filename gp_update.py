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

from __future__ import absolute_import
from __future__ import print_function
from __future__ import absolute_import

import os, sys
import logging

import config # user-credentials

from ext_libs.googleplay_api.googleplay import GooglePlayAPI #GooglePlayAPI
from ext_libs.googleplay_api.googleplay import LoginError
from ext_libs.androguard.core.bytecodes import apk as androguard_apk #Androguard

def connect():
	api = GooglePlayAPI(androidId=config.ANDROID_ID, lang=config.LANG)
	try :
		api.login(config.GOOGLE_LOGIN, config.GOOGLE_PASSWORD, config.AUTH_TOKEN)
	except LoginError, exc:
		logging.error("Error: Connection to PlayStore failed: %s" % exc)
		return None

	logging.info("Info: Connection to GooglePlayStore established")
	return api

def update(playstore_api, apk_folder_path):
	# search for apks in given folder
	list_of_apks = [filename for filename in os.listdir(apk_folder_path) if os.path.splitext(filename)[1] == ".apk"]
	if len(list_of_apks) <= 0:
		print("No apks found in folder %s" % apk_folder_path)
		sys.exit(0)

	# create a list of apks, just keep the newest
	apks_to_update = dict()
	for position, filename in enumerate(list_of_apks):
		filepath = os.path.join(apk_folder_path, filename)
		a = androguard_apk.APK(filepath)
		apk_version_code = a.get_androidversion_code()
		packagename = a.get_package()

		logging.info("Info: Found apk %s : %s : %s" % (filepath, packagename, apk_version_code))

		if packagename in apks_to_update:
			if apks_to_update[packagename] < apk_version_code:
				apks_to_update[packagename] = apk_version_code
		else:
			apks_to_update[packagename] = apk_version_code

	if len(apks_to_update) <= 0:
		logging.error("Error: No apks to update after non-empty apk-list. Something went wrong!")
		sys.exit(1)

	# search for the apks on googleplaystore
	for packagename, version_code in apks_to_update.items():
		local_version_code = int(version_code)
		logging.info("Info: Checking apk %s : %d" % (packagename, local_version_code))

		m = playstore_api.details(packagename)
		doc = m.docV2
		store_version_code = int(doc.details.appDetails.versionCode)

		if store_version_code == 0:
			continue
		if store_version_code > local_version_code:
			# download apk from store
			print("Updating apk %s : %d -> %d" % (packagename, local_version_code, store_version_code))
			try:
				data = playstore_api.download(packagename, store_version_code)
			except Exception as exc:
				logging.error("Error: failed to download %s : %s" % (packagename, exc))
				continue
			else:
				# save downloaded apk under '<packagename>_<version>.apk'
				filename = "%s_%d.apk" % (packagename, store_version_code)
				filepath = os.path.join(apk_folder_path, filename)
				
				try:
					open(filepath, "wb").write(data)
				except IOError, exc:
					logging.error("Error: cannot write to disk %s : %s" % (packagename, exc))
					continue
				logging.info("Info: Downloaded apk %s : %d : %s" % (packagename, store_version_code, filename))
		else:
			logging.info("Info: No newer apk found.")



	# call 'fdroid --clean'

def synopsis():
	print("Usage: %s [-v] <apk_folder_path>" % sys.argv[0])
	print("\t-v\t verbose output")

def main():
	print(sys.argv)
	min_argc = 2
	path_index = 1

	# Check arguments
	if "-v" in sys.argv:
		min_argc += 1
		path_index += 1
		logging.basicConfig(level=logging.INFO)

	# TODO: --config flag

	if len(sys.argv) < min_argc:
		synopsis()
		sys.exit(1)

	# get apk_folder_path
	apk_folder_path = sys.argv[path_index]
	if not os.path.isdir(apk_folder_path):
		print("Error: given <apk_folder_path> is not a directory: %s" % apk_folder_path)
		synopsis()
		sys.exit(1)
	
	# connect to Google Play Store
	playstore_api = connect()
	if playstore_api == None:
		print("Error: Connection to PlayStore failed. Check provided credencials in config.py")
		sys.exit(1)

	# update local apks
	update(playstore_api, apk_folder_path)

if __name__ == '__main__':
  main()


