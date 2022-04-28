DST=`pwd`/result
mkdir -p $DST
mkdir -p $DST/png
mkdir -p $DST/pdf
cd ../performance/plotting/
./plot.sh
#cp 05_Performance_larger_ratio.png $DST/
#cp 05_Performance_smaller_ratio.png $DST/

#cp 05_Performance_larger_ratio.pdf $DST/
#cp 05_Performance_smaller_ratio.pdf $DST/


#cp *.eps $DST/
#cp *.tiff $DST/
cp Fig17.png $DST/png/
cp Fig17.pdf $DST/pdf/