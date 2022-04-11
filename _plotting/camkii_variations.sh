DST=`pwd`/result
mkdir -p $DST
cd ../CaMKII_model_variations/plotting
./plot.sh
cp half_in_PSD.png $DST/half_in_PSD.png
cp PSD.png $DST/PSD.png
cp PSD_transparent.png $DST/PSD_transparent.png
