import os,sys
import subprocess as sp
import bionetgen
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf

'''This script runs mcell & bionetgen from the same bngl model & plot the results together
GCG
02.10.22
'''


print('snare_complex: running...')
# print('snare_complex: current directory = ', os.getcwd()) /Users/joelyancey/MCell/article_mcell4/_plotting
# print('sys.path[0] = ', sys.path[0])  /Users/joelyancey/MCell/article_mcell4/snare_complex/plotting
os.chdir(sys.path[0])

plt.style.use(['../../_plotting/styles/plot_trajectories_single_plot.mplstyle','../../_plotting/styles/master.mplstyle'])

pdf_name = 'snare_complex.pdf'
pdf = matplotlib.backends.backend_pdf.PdfPages(pdf_name)

python_path ='/Applications/Blender-2.93-CellBlender/blender.app/Contents/Resources/2.93/python/bin/python3.9'
run_file = 'model.py'
tdir = '../mcellsim/'
#run mcell
Proc = sp.call([python_path, run_file],cwd = tdir)
if Proc != 0:
 print('MCell did not run')
else:
 print('MCell sim done')

# for Windows:f
# replace C:\\cmw2021\\ with the actual path where you unpacked CellBlender
# python_path = 'C:\\cmw2021\\Blender-2.93-CellBlender\\2.93\\python\\bin\\python3.9.exe'

#directories for bionetgen files
dir =  'Scene_model.bngl'
outdir = './output_folder/'
tdir = '../bngl/'
# #run bionetgen
Proc = sp.call(['bionetgen','run','-i',dir,'-o',outdir],cwd = tdir)
if Proc != 0:
    print('BIONETGEN did not run')
else:
    print('BIONETGEN run')

## for Windows:
#exe_ext = ''
#if os.name == 'nt':
#    exe_ext = '.exe'
#Proc = sp.call(['bionetgen' + exe_ext,'run','-i',dir,'-o',outdir],cwd = tdir)

#Load mcell output
mc_snare_syn = np.genfromtxt('../mcellsim/react_data/seed_00001/SNARE_sync.dat',
                      dtype=float,
                      delimiter=' ')
#
mc_snare_asyn = np.genfromtxt('../mcellsim/react_data/seed_00001/SNARE_async.dat',
                      dtype=float,#
                      delimiter=' ')
mc_vrel = np.genfromtxt('../mcellsim/react_data/seed_00001/V_release.dat',
                      dtype=float,#
                      delimiter=' ')

# #Load bionetgen output
bng = np.genfromtxt('../bngl/output_folder/Scene_model.gdat',
                      skip_header=1,
                       dtype=float,
                       delimiter=' ')
#
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.9, left = 0.15, bottom =0.15, top = 0.95)
#
ax.plot(bng[:,0],bng[:,2],'r',linestyle = 'dashdot',label = 'BNGL ODE SNARE_sync')
ax.plot(bng[:,0],bng[:,4],'g',label = 'BNGL SNARE_async')
ax.plot(bng[:,0],bng[:,6],'b',label = 'BNGL ODE V release')
ax.plot(mc_snare_syn[:,0],mc_snare_syn[:,1],'r',linestyle = '--',label = 'MCell SNARE_sync')
ax.plot(mc_snare_asyn[:,0],mc_snare_asyn[:,1],'g',label = 'MCell SNARE_async')
ax.plot(mc_vrel[:,0],mc_vrel[:,1],'b',label = 'MCell V release')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.legend(loc='upper left')
#plt.ylim(0,8000)
#plt.xlim(0,3.5e-4)
#
plt.xlabel('Time (sec)')
plt.ylabel('# SNARE_async or SNARE_sync')
# plt.savefig('snare.png')
# plt.show()
pdf.savefig(fig)
plt.show()
plt.close()
print('snare_complex: done.')
