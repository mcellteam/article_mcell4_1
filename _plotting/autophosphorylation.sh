DST=`pwd`/result
mkdir -p $DST
mkdir -p $DST/pdf
mkdir -p $DST/png
cd ../autophosporylation/plotting
#./plot_mcell4.sh
#./plot_mcell3.sh
#./plot_nfsim.sh
./plot_combined.sh

#cp mcell3.png $DST/05_Autophosphorylation_MCell3.png
#cp mcell4.png $DST/05_Autophosphorylation_MCell4.png
#cp nfsim.png $DST/05_Autophosphorylation_NFSim.png
#cp *.tiff $DST/
cp Fig16.png $DST/png/
cp Fig16.pdf $DST/pdf/