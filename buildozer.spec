[app]
title = Udhar Expense Manager
package.name = udharexpense
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,db
version = 1.0
requirements = python3,kivy==2.2.1,sqlite3,matplotlib
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.1
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.private_storage = True
android.logcat_filters = *:S python:D
android.arch = arm64-v8a
p4a.local_recipes = 
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
[buildozer]
log_level = 2
warn_on_root = 1
