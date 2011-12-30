cd ~/Desktop
chmod 755 chmod755.sh
./chmod755.sh
cd ~
rm -rf iPhone4iOS5
rm -rf wilhelmtell-iosplayground
hg clone https://code.google.com/p/iphone-dataprotection/
cd ~/Desktop
rm -rf iPhone4iOS5
rm -rf wilhelmtell-iosplayground
cd ~
mv wilhelmtell-iosplayground iPhone4iOS5
cp -R -f iPhone4iOS5 ~/Desktop/iPhone4iOS5
cd ~/Desktop/iPhone4iOS5
make -C img3fs/
curl -O -L https://sites.google.com/a/iphone-dev.com/files/home/redsn0w_mac_0.9.10b3.zip
unzip redsn0w_mac_0.9.10b3.zip
cp redsn0w_mac_0.9.10b3/redsn0w.app/Contents/MacOS/Keys.plist .
cp ~/Desktop/iPhone3\,1_5.0.1_9A405_Restore.ipsw ~/Downloads/iPhone4iOS5/
python python_scripts/kernel_patcher.py ~/Desktop/iPhone3\,1_5.0.1_9A405_Restore.ipsw
sh ./make_ramdisk_n90ap.sh