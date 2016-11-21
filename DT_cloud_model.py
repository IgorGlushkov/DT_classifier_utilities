# -*- coding: UTF-8 -*-
import os
import glob
import tarfile

# path to data
datadir='d:\DT\cloud_data'
# path to training
traindir='d:\DT\cloud_trainings'
# presence
presence=os.path.join(traindir,'cloud.shp')
# absence
absence=os.path.join(traindir,'nocloud.shp')
#merge points
merge_train_points='cloud_train_points.shp'
#model
model='d:\DT\model\model_cloud.yaml'
#result
result='d:\DT\\result'

#unzip in separate folders
scenes = glob.glob(os.path.join(datadir, '*gz'))
for scene in scenes:
    try:
		a = tarfile.open(scene)
		scene_name = scene.split('.')[0]
		a.extractall(path=os.path.join(datadir,scene_name))
		a.close()
    except IOError:
        False
		
	
#remove BQA bands
for subdir, dirs, files in os.walk(datadir):
	bands=glob.glob(os.path.join(subdir, '*BQA.TIF'))
	if bands == []:
	   continue
	else:
	   command= 'rm %s' % (bands[0])
	   print command
	   os.system(command)
	   
#remove panchromatic bands
for subdir, dirs, files in os.walk(datadir):
	bands=glob.glob(os.path.join(subdir, '*B8.TIF'))
	if bands == []:
	   continue
	else:
	   command= 'rm %s' % (bands[0])
	   print command
	   os.system(command) 
		
#create train points from selected scenes
for subdir, dirs, files in os.walk(datadir):
	bands=glob.glob(os.path.join(subdir, '*.TIF'))
	if bands == []:
	   continue
	else:
	   bands=' '.join(bands)
	   train_points=os.path.join(traindir, str(os.path.basename(subdir))+'train_points.shp')
	   command= 'classifier.bat --input_rasters %s --save_train_layer %s --presence %s --absence %s' % (bands,train_points,presence,absence)
	   print command
	   os.system(command)

#merge trainings with null values removing
commandlist=[]
driver='ESRI Shapefile'
trainings=glob.glob(os.path.join(traindir, '*train_points.shp'))
for training in trainings:
	if commandlist == []:
	   merge_train=os.path.join(traindir, merge_train_points)
	   command='ogr2ogr -f \"%s\" %s %s -where \"Band_1 > 0\"' % (driver,merge_train,training)
	   merge_name = merge_train_points.split('.')[0]
	   command1='ogr2ogr -f \"%s\" -update -append  %s %s -nln %s -where \"Band_1 > 0\"' % (driver,merge_train,training,merge_name)
	   commandlist.append(command)
	   commandlist.append(command1)
	else:
	   merge_train=os.path.join(traindir, merge_train_points)
	   #remove ext
	   merge_name = merge_train_points.split('.')[0]
	   command='ogr2ogr -f \"%s\" -update -append  %s %s -nln %s -where \"Band_1 > 0\"' % (driver,merge_train,training,merge_name)
	   commandlist.append(command)

#run merge shp 
#f = open('%s\com.txt' % (traindir), 'w')
for command in commandlist:
	#f.write(command+'\n')
	os.system(command)
#f.close()
	

#create model
if os.path.isfile(os.path.join(traindir,merge_train_points)):
   try:
      merge_train=os.path.join(traindir,merge_train_points)
      command='classifier.bat --use_train_layer %s --save_model %s' % (merge_train,model)
      os.system(command)
   except IOError:
      False

#classify
for subdir, dirs, files in os.walk(datadir):
	bands=glob.glob(os.path.join(subdir, '*.TIF'))
	if bands == []:
	   continue
	else:
	   bands=' '.join(bands)
	   output=os.path.join(result, str(os.path.basename(subdir))+'out_cloud.tif')
	   command= 'classifier.bat --input_rasters %s --use_model %s --classify %s --generalize 3' % (bands,model,output)
	   print command
	   os.system(command)
	
