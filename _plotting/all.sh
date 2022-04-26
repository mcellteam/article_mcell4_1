#!/bin/bash -x

rm -r result/*.png
rm -r result/*.eps
rm -r result/*.tiff

./autophosphorylation.sh &  
./camkii.sh &
./camkii_variations.sh &
./membrane_loc.sh &
./performance.sh &
./hybrid.sh &
./snare_complex.sh &
wait