DST=`pwd`/result
mkdir -p $DST
cd ../performance/plotting/
./plot.sh
cp 05_Performance_larger_ratio.png $DST/ 
cp 05_Performance_smaller_ratio.png $DST/ 