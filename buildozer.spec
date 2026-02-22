[app]
title = Udhar Expense Manager
package.name = udharexpense
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.1,pillow,sqlite3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True

# REMOVE this line:
# android.sdk_path = ~/.buildozer/android/platform/android-sdk

[buildozer]
log_level = 2
warn_on_root = 1
