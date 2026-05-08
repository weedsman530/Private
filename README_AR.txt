تطبيق Android لتغيير وقت وتاريخ جهاز ZKTeco من الموبايل.

الإعداد الافتراضي داخل التطبيق:
Device IP: 192.168.1.201
Port: 4370

طريقة البناء على Linux أو WSL:
1) ثبت المتطلبات:
   sudo apt update
   sudo apt install -y python3-pip git zip unzip openjdk-17-jdk
   pip3 install --user buildozer cython

2) ادخل مجلد المشروع:
   cd zkteco_mobile_app

3) ابني APK:
   buildozer -v android debug

4) ستجد APK داخل مجلد:
   bin/

ملاحظات الشبكة:
- جهاز البصمة يكون متوصل بالراوتر بسلك LAN.
- الموبايل يكون على نفس Wi-Fi بتاع نفس الراوتر.
- IP البصمة ثابت: 192.168.1.201
- الراوتر يفضل يكون 192.168.1.1
- الموبايل يأخذ IP مثل 192.168.1.20 أو 192.168.1.50
- تأكد أن Port 4370 غير مقفول وأن البصمة متاحة على الشبكة.

اختبار الاتصال من Android:
- افتح تطبيق Ping من المتجر وجرب ping 192.168.1.201
- لو جاب Reply التطبيق غالبا هيشتغل.
