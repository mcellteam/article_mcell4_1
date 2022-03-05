#!/bin/bash -x

./autophosphorylation.sh &  
./camkii.sh &
./membrane_loc.sh &
./performance.sh &
wait