from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

img_height, img_width = 224, 224
model = load_model('./model_DL/fruit_model_VGG16.h5')

# Create your views here.
def index(request):
    return render(request, 'index.html')


def deteksiBuah(request):
    fileObj = request.FILES['gambar']
    print(fileObj)
    fs = FileSystemStorage()
    direktori = fs.save(name=fileObj.name, content=fileObj)
    filepath = fs.url(direktori)
    
    img = image.load_img('.'+filepath, color_mode="rgb", target_size=(224, 224), interpolation="nearest")
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    img = np.vstack([img])
    classes = model.predict(img, batch_size=33)
    hasil = np.argmax(classes)

    if hasil == 0:
        prediction = 'Apel Segar'
    elif hasil == 1:
        prediction = 'Pisang Segar'
    elif hasil == 2:
        prediction = 'Jeruk Segar'
    elif hasil == 3:
        prediction = 'Jambu Segar'
    elif hasil == 4:
        prediction = 'Jeruk Nipis Segar'
    elif hasil == 5:
        prediction = 'Apel Busuk'
    elif hasil == 6:
        prediction = 'Pisang Busuk'
    elif hasil == 7:
        prediction = 'Jeruk Busuk'
    elif hasil == 8:
        prediction = 'Jambu Busuk'
    elif hasil == 9:
        prediction = 'Jeruk Nipis Busuk'

    print(prediction)
    context = {'direktori_gambar': filepath, 'hasil':prediction}
    return render(request, 'index.html', context)
