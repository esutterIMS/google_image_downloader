import rembg
import os
from PIL import Image
  
for folder in os.listdir('dataset'):
    if not os.path.exists('results/' + folder):
        os.makedirs('results/' + folder)
    for file in os.listdir('dataset/' + folder):
        
        # Processing the image
        input = Image.open('dataset/' + folder + '/' + file)

        # Removing the background from the given Image
        output = rembg.remove(input,)

        file = file.replace('jpg', 'png')
        file = file.replace('jpeg', 'png')
        file = file.replace('webp', 'png')

        #Saving the image in the given path
        output.save('results/' + folder + '/' + file)