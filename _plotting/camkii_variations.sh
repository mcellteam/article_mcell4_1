DST=`pwd`/result
mkdir -p $DST
mkdir -p $DST/pdf
mkdir -p $DST/png
cd ../CaMKII_model_variations/plotting
./plot.sh
#cp half_in_PSD.png $DST/half_in_PSD.png
#cp PSD.png $DST/PSD.png
#cp PSD_transparent.png $DST/PSD_transparent.png

#cp *.tiff $DST/
cp Fig14.png $DST/png/
cp Fig14.pdf $DST/pdf/
