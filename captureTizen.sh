sdb root on
sdb shell xwd -root -out /tmp/screen.xwd
sdb pull /tmp/screen.xwd
convert screen.xwd -resize 50% screen.png

