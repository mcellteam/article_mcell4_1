DST=`pwd`/result
mkdir -p $DST
cd ../snare_complex/plotting
./plot.sh
#cp snare_complex.png $DST/snare_complex.png
#cp snare_complex.png $DST/Fig12_snare_complex.png
cp *.tiff $DST/