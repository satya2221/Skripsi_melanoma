from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, 'index.html') 


def deteksiBuah(request):
    fileObj = request.FILES['gambar']
    print(fileObj)
    fs = FileSystemStorage()
    direktori = fs.save(name=fileObj.name, content=fileObj)
    filepath = fs.url(direktori)

    context = {'direktori_gambar':filepath}
    return render(request, 'index.html', context) 