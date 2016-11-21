# -*- coding: UTF-8 -*-
import os
import glob

# path to data
datadir='d:\DT\data'
# path to training
traindir='d:\DT\\trainings'
# presence
presence=os.path.join(traindir,'cut1.shp')
# absence
absence=os.path.join(traindir,'nochange.shp')
#result
result='d:\DT\\result'

for subdir, dirs, files in os.walk(datadir):
	scenes=glob.glob(os.path.join(subdir, '*.tif'))
	if scenes == []:
	   continue
	else:
	   scenes=' '.join(scenes)
	   output=os.path.join(result, str(os.path.basename(subdir))+'out.tif')
	   model=os.path.join(result, str(os.path.basename(subdir))+'model.yaml')
	   train_points=os.path.join(result, str(os.path.basename(subdir))+'train_points.shp')
	   # command DTclassifier
	   command= 'classifier.bat --input_rasters %s --save_train_layer %s --save_model %s --presence %s --absence %s --classify %s --generalize 3' % (scenes,train_points,model,presence,absence,output)
	   #run command
	   os.system(command)