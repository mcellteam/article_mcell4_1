DST=`pwd`/result
mkdir -p $DST
mkdir -p $DST/pdf
mkdir -p $DST/png
cd ../membrane_localization/plotting/
./plot_17000.sh
#cp 05_Membrane_localization.png $DST/
#cp *.tiff $DST/Fig15.tiff
cp Fig16.png $DST/png/
cp Fig16.pdf $DST/pdf/