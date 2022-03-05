DST=`pwd`/result
mkdir -p $DST
cd ../hybrid_circadian_clock/plotting
./plot.sh

cp hybrid_averages_fast.png hybrid_averages_slow_particle.png hybrid_peaks.png hybrid_averages_slow_hybrid.png hybrid_low_pass_nfsim.png $DST
