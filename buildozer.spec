[app]
title = ZKTeco Time Tool
package.name = zktecotimetool
package.domain = org.local
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0
requirements = python3,kivy,pyzk
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 35
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
