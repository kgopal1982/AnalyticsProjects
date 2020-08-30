#Set this to False if you dont want to create empry directory in the modified folder
CREATE_DIRECTORY = True

import os
orig_data_path = 'C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\Datasets\\Hnd\\Sample\\orig_img\\'
mod_data_path = 'C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\Datasets\\Hnd\\Sample\\mod_img\\'

#create empty directory in modified path
if (CREATE_DIRECTORY == True):
    for entry in os.listdir(orig_data_path):
        if os.path.isdir(os.path.join(orig_data_path, entry)):            
            dir_name = mod_data_path + entry
            os.mkdir(dir_name)

#here we are trying to create augmentated dataset based on input datasets
from keras.preprocessing.image import ImageDataGenerator

#orig_data_set = 'C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\Datasets\\Hnd\\Sample\\Img\\Sample005\\'
#aug_data_set = 'C:\\Users\\ekrigos\\Desktop\\DataS\\REVA\\finalyearProj\\OCR\\kanadda\\Datasets\\Hnd\\Sample\\Aug_Img\\Sample005\\'

#dataset = ImageDataGenerator()


#image = dataset.flow_from_directory(orig_data_set,target_size=(50,50),save_to_dir = aug_data_set, class_mode='categorical',save_prefix = "Aug_", batch_size=10)
#image.next()

# Importing necessary functions 
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img 

# Initialising the ImageDataGenerator class. 
# We will pass in the augmentation parameters in the constructor. 
datagen = ImageDataGenerator( 
		rotation_range = 40, 
		shear_range = 0.2, 
		zoom_range = 0.2, 
		brightness_range = (0.5, 1.5)) 

#Create augmented images from a single image and save it

def create_aug_images(img,aug_path):
	
    # Loading a sample image 
    
    # Converting the input sample image to an array 
    x = img_to_array(img) 
    # Reshaping the input image 
    x = x.reshape((1, ) + x.shape) 
    
    # Generating and saving augmented samples 
    # using the above defined parameters. 
    i = 0
    for batch in datagen.flow(x, batch_size = 1, 
    						save_to_dir = aug_path, 
    						save_prefix ='Aug_', save_format ='jpeg'): 
    	i += 1
    	if i > 40: 
    		break


#img = load_img(orig_data_set + 'img001-001.png') 
#create_aug_images(img)



# for fileName in os.listdir(orig_data_path):
#    print(fileName)
#    img = load_img(orig_data_path + '\\' + fileName)
#    create_aug_images(img,mod_data_path)


        
for entry in os.listdir(orig_data_path):
    if os.path.isdir(os.path.join(orig_data_path, entry)):  
        print(entry)
        print('orig_path is')
        orig_path = orig_data_path + entry
        print(orig_path)
        print('aug_path is')
        aug_path = mod_data_path + entry
        print(aug_path)
        for fileName in os.listdir(orig_path):
            print('fileName is')
            print(fileName)
            imgPath = orig_path + '\\' + fileName
            img = load_img(imgPath)
            create_aug_images(img,aug_path)


