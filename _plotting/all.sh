#!/bin/bash -x

rm -r result/*.png

./autophosphorylation.sh &  
./camkii.sh &
./camkii_variations.sh &
./membrane_loc.sh &
./performance.sh &
./hybrid.sh &
wait