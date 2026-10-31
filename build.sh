#!/bin/bash
set -e
cd "$(dirname "$0")"
SDK=/opt/android-sdk
BT=$SDK/build-tools/34.0.0
AJ=$SDK/platforms/android-34/android.jar
rm -rf build
mkdir -p build/compiled build/classes build/dex build/gen
$BT/aapt2 compile --dir res -o build/res.zip
$BT/aapt2 link -o build/app-unsigned.apk -I $AJ --manifest AndroidManifest.xml -R build/res.zip \
  -A assets --java build/gen --min-sdk-version 24 --target-sdk-version 34 \
  --version-code 1 --version-name 1.0 --auto-add-overlay
javac -nowarn -encoding UTF-8 -source 8 -target 8 -bootclasspath $AJ -classpath $AJ -d build/classes \
  $(find src build/gen -name "*.java")
$BT/d8 --lib $AJ --min-api 24 --release --output build/dex $(find build/classes -name "*.class")
cp build/app-unsigned.apk build/app-withdex.apk
(cd build/dex && zip -q -X ../app-withdex.apk classes.dex)
$BT/zipalign -f -p 4 build/app-withdex.apk build/app-aligned.apk
$BT/apksigner sign --ks rike.keystore --ks-pass pass:stepxstudio --key-pass pass:stepxstudio \
  --out build/Rike.apk build/app-aligned.apk
$BT/apksigner verify build/Rike.apk
echo "BUILD OK"
