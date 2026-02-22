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
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a
android.allow_backup = True

# REMOVE THESE TWO LINES:
# android.skip_update = False
# android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
