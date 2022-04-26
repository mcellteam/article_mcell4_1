DST=`pwd`/result
mkdir -p $DST
cd ../hybrid_circadian_clock/plotting
./plot.sh

#cp \
#	hybrid_averages_fast.png \
#	hybrid_averages_hybrid_slow.png \
#	hybrid_averages_particle_slow.png \
#	hybrid_low_pass_nfsim.png \
#	hybrid_peaks.png \
#	$DST

cp *.tiff $DST/