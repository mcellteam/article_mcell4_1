DST=`pwd`/result
mkdir -p $DST
cd ../membrane_localization/plotting/
./plot_17000.sh
#cp 05_Membrane_localization.png $DST/
#cp *.tiff $DST/Fig15.tiff
cp *.pdf $DST/Fig15.pdf