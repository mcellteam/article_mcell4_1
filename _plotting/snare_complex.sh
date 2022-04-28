DST=`pwd`/result
mkdir -p $DST
mkdir -p $DST/pdf
mkdir -p $DST/png
cd ../snare_complex/plotting
./plot.sh
#cp snare_complex.png $DST/snare_complex.png
#cp snare_complex.png $DST/Fig12_snare_complex.png
#cp *.tiff $DST/Fig12.tiff
cp Fig12.png $DST/png/
cp Fig12.pdf $DST/pdf/