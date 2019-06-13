#!/usr/bin/env python

#Hernando Martinez Vergara
#June 2019

# Transform all files specified using the first one to guide registration


# Make sure you are in the directory with the files you want to transform
# Have the channels as .tif files and make sure their properties are consistent
# Change them in imagej in ImageProperties (e.g. 25 x 25 x 25 micrometers)

import sys
import os
import shutil

elastixPath = '/mnt/c/Users/herny/Software/elastix-4.9.0-win64/elastix.exe'
transformixPath = '/mnt/c/Users/herny/Software/elastix-4.9.0-win64/transformix.exe'
paramFolder = '/mnt/c/Users/herny/OneDrive/Documents/GitHub/RegistrationToAllen/elastix_parameters/'
paramAffName = '01_ARA_affine.txt'
paramBSName = '02_ARA_bspline.txt'
allenrefFolder = '/mnt/c/Users/herny/Desktop/SWC/Data/Anatomy/ARA_25_micron_mhd/'
allenrefName = 'template.mhd'
allenRaw = 'template.raw'

#copy parameter files
shutil.copy(paramFolder+paramAffName, './')
shutil.copy(paramFolder+paramBSName, './')

#copy reference
shutil.copy(allenrefFolder+allenrefName, './')
shutil.copy(allenrefFolder+allenRaw, './')




#get the input file and perform the registration
if len(sys.argv) < 2:
    sys.exit('Not enough arguments, tell me at least one channel')

leadChannel = sys.argv[1]
print(leadChannel)
RegCommand = '{0} -f {1} -m {2} -p {3} -p {4} -out {5}'.format(
        elastixPath,
        allenrefName,
        leadChannel,
        paramAffName,
        paramBSName,
        './')
print('Running elastix')
print(RegCommand)
os.system(RegCommand)

# Rename elastix output
filename, _ = os.path.splitext(leadChannel)
leadChannelout = filename + '_reg.tif'
os.system('mv result.1.tiff {0}'.format(leadChannelout))


print('***** Applying transformation to other channels ******')

for channel in sys.argv[2:len(sys.argv)]:
    print('Transforming ' + channel)
    TraCom = '{0} -in {1} -out {2} -tp {3}'.format(
            transformixPath,
            channel,
            './',
            './TransformParameters.1.txt')
    print('Running transformix')
    print(TraCom)
    os.system(TraCom)

    # Rename
    filename, _ = os.path.splitext(channel)
    channelOut = filename + '_reg.tif'
    os.system('mv result.tiff {0}'.format(channelOut))

#clean up
os.system('rm IterationInfo*')
os.system('rm {0} {1}'.format(allenRaw, allenrefName))
    




