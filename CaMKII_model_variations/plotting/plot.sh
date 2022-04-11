python ../../_plotting/scripts/plot_trajectories_single_plot.py -m4 ../PSD_transparent/react_data_wm -o PSD_transparent --camkii -t 3 -l labels.txt -i A & 	
python ../../_plotting/scripts/plot_trajectories_single_plot.py -m4 ../PSD/react_data_wm -o PSD --camkii -t 3 -l labels.txt -i B &
python ../../_plotting/scripts/plot_trajectories_single_plot.py -m4 ../half_in_PSD/react_data_wm -o half_in_PSD --camkii -t 3 -l labels.txt -i C & 
wait