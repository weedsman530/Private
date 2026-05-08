طريقة استخراج APK من GitHub بدون لينكس على جهازك

1) اعملي حساب على GitHub.
2) اعملي Repository جديد، ويفضل يكون Private.
3) ارفعي محتويات هذا المجلد كما هي داخل الريبو، وليس ملف ZIP نفسه.
   لازم يظهر في الصفحة الرئيسية للريبو:
   - main.py
   - buildozer.spec
   - README_AR.txt
   - .github/workflows/build-apk.yml

مهم: لو فولدر .github مش ظاهر في ويندوز، ارفعي الملفات بالسحب والإفلات كلها، أو استخدمي خيار Add file > Upload files في GitHub.

4) بعد الرفع، افتحي تبويب Actions من أعلى صفحة الريبو.
5) اختاري Build Android APK.
6) اضغطي Run workflow.
7) بعد ما يخلص، افتحي آخر Run.
8) انزلي تحت عند Artifacts.
9) حملي zkteco-time-tool-apk.
10) فكّي الضغط، هتلاقي ملف APK.

تثبيت APK على Android:
- انسخي APK على الموبايل.
- افتحيه.
- لو طلب Allow install from unknown sources وافقي.

إعدادات الشبكة المطلوبة:
البصمة:
IP Address:   192.168.1.201
Subnet Mask:  255.255.255.0
Gateway:      192.168.1.1
Port:         4370
DHCP:         Off

الراوتر:
LAN IP:       192.168.1.1
DHCP:         On
DHCP Range:   192.168.1.2 إلى 192.168.1.200

الموبايل:
- متصل على نفس Wi-Fi
- IP مثل 192.168.1.20 أو أي 192.168.1.xxx

اختبار مهم:
قبل استخدام التطبيق نزلي أي تطبيق Ping من الموبايل وجربي:
192.168.1.201
لو فيه Reply، التطبيق غالبا هيشتغل.
