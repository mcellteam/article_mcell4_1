DST=`pwd`/result
mkdir -p $DST
cd ../membrane_localization/plotting/
./plot_17000.sh
cp 05_Membrane_localization.png $DST/ 