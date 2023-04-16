from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
import keras.utils as image
import numpy as np
import magic
#import base64
import cv2
import keras

img_height, img_width = 224, 224
model = load_model('./model_DL/melanoma-classification_1.h5') # rotten-fresh-fruit-classification, fruit_model_VGG16

def unduhGambar(request):
    return HttpResponse('Ini harusnya ngedownload')

def upGambar(request):
    return render(request, 'index.html')

# def artikel(request):
#     return render(request, 'blog.html')

def hair_remove_3(image):
    # convert image to grayScale
    (Blue, Green, Red) = cv2.split(image)
    grayScale = Red

    #resize
    image_resize = cv2.resize(image, (512,512), interpolation = cv2.INTER_AREA)
    grayScale = cv2.resize(grayScale, (512,512), interpolation = cv2.INTER_AREA)
    
    # kernel for morphologyEx
    kernel = cv2.getStructuringElement(1,(23,23))
    
    # apply MORPH_BLACKHAT to grayScale image
    blackhat = cv2.morphologyEx(grayScale, cv2.MORPH_BLACKHAT, kernel)

    # apply thresholding to blackhat
    ret,threshold = cv2.threshold(blackhat,10,255,cv2.THRESH_BINARY)

    # inpaint with original image and threshold image
    final_image = cv2.inpaint(image_resize,threshold,1,cv2.INPAINT_TELEA)
    
    return image_resize, final_image

def deteksiBuah(request):
    fileObj = request.FILES['gambar'] if 'gambar' in request.FILES else False
    filepath =''
    prediction = ''
    if(fileObj):
        print(fileObj.name)
        nama = fileObj.name
        # extension = fileObj.name.split('.')[1]
        # print(type(extension))
        # valid_extensions = ['jpg', 'jpeg']
        # if extension.lower() not in valid_extensions:
        #     print("masuk error")
        #     context_error = {'hasil':'File bukan .JPEG atau .JPG'}
        #     return render(request,'index.html', context_error)

        fs = FileSystemStorage()
        direktori = fs.save(name=fileObj.name, content=fileObj)
        filepath = fs.url(direktori)
        filename = filepath.split('.')[0]
        print("direktori: ", direktori)
        print("filepath: ", filepath)
        print("file name: ", filename)
        
        fileType = magic.from_file('./media/'+direktori)
        print("Tipe file adalah:" , fileType)
        if not "JPEG" in fileType:
            print("masuk error")
            context_error = {'hasil':'File bukan .JPEG atau .JPG'}
            return render(request,'index.html', context_error)

        img = cv2.imread('.'+filepath)#[...,::-1]
        img_512, img_hair_free = hair_remove_3(img)

        
        otsu_val, image_segment = cv2.threshold(cv2.cvtColor(img_hair_free, cv2.COLOR_RGB2GRAY),
                                        0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,)
        try:
            cv2.imwrite('.'+filename+'_HairFree.JPG',img_hair_free)
            cv2.imwrite('.'+filename+'_segment.JPG', image_segment)
            cv2.imwrite('.'+filename+'_512.JPG', img_512)
        except:
            print("Imwrite bebas rambut gagal")
        (Red, Green, Blue) = cv2.split(img_hair_free)
        img_arr = cv2.merge((Red, Green, Blue, image_segment))
        img_arr = cv2.resize(img_arr, (224,224))
        img_arr_expand = np.expand_dims(img_arr, axis=0)

        img_stack = np.vstack([img_arr_expand])
        classes = model.predict(img_stack)
        print(classes)
        hasil = np.argmax(classes)
        print(hasil)
        
        if hasil==0:
            prediction = 'Melanoma'
        elif hasil==1:
            prediction = 'Non-Melanoma'
    else:
        prediction = "Masukkan Gambar terlebih dahulu"    
    context = {'direktori_gambar': filename+'_512.JPG', 'hasil':prediction, 'img_seg': filename+'_segment.JPG', 'hair_free':filename+'_HairFree.JPG', 'nama_file':nama}
    return render(request, 'hasilPrediksi.html', context)
