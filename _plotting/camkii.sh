DST=`pwd`/result
mkdir -p $DST
mkdir -p $DST/pdf
mkdir -p $DST/png
cd ../camkii_only_output_data/plotting
./plot.sh
#cp Ca.png $DST/05_CaMKII_01_Ca.png
#cp CaM1C.png $DST/05_CaMKII_02_CaM1C.png
#cp CaM1N.png $DST/05_CaMKII_03_CaM1N.png
#cp KCaM2N.png $DST/05_CaMKII_04_KCaM2N.png
#cp *.tiff $DST/
cp Fig14.png $DST/png/
cp Fig14.pdf $DST/pdf/
