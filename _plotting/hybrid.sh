DST=`pwd`/result
mkdir -p $DST
mkdir -p $DST/pdf
mkdir -p $DST/png
cd ../hybrid_circadian_clock/plotting
./plot.sh

#cp \
#	hybrid_averages_fast.png \
#	hybrid_averages_hybrid_slow.png \
#	hybrid_averages_particle_slow.png \
#	hybrid_low_pass_nfsim.png \
#	hybrid_peaks.png \
#	$DST

#cp *.tiff $DST/
cp Fig22.png $DST/png/
cp Fig22.pdf $DST/pdf/
cp Fig23.png $DST/png/
cp Fig23.pdf $DST/pdf/