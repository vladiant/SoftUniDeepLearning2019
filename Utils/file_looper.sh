#!/bin/bash
PREFIX="./Dataset2/"
EXTEN="jpg"
FILES=$PREFIX*.$EXTEN

strindex() { 
  x="${1%%$2*}"
  [[ "$x" = "$1" ]] && echo -1 || echo "${#x}"
}

for f in $FILES
do
  pos=`strindex "$f" "$EXTEN"`
  suffix=${f:0:pos-${#EXTEN}+2}
  f_dist=${suffix}"_mask.png"

  if [ -f "$f" ] && [ ! -f "$f_dist" ]; then
    /home/vladiant/Workplace/Barcode/Barcode_1D/build/iyBarcode --file=$f
#    echo $f
#    echo $f_dist
  fi
  
done
