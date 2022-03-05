#!/bin/bash -x

rm -r result/*.png

./autophosphorylation.sh &  
./camkii.sh &
./membrane_loc.sh &
./performance.sh &
./hybrid.sh &
wait