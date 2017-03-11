import numpy as np
import cv2
import os

from django.http import HttpResponse,HttpResponseRedirect
from .models import  Document,Opencv, Opencv2
from .forms import DocumentForm,FormOpencv,ResizerInputs
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .Processor import worker

img_path=''
wk = worker()
def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('resizer:index'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'resizer/index.html',
        {'documents': documents, 'form': form}
    )

def resizer_op(request):
    return resizer_op_fetch_img(request)
def compress_op(request):
    return compress_op_fetch_img(request)
def enhance_op(reqest):
    pass


def resizer_op_fetch_img(request):
    form = FormOpencv(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = Opencv(imagem = request.FILES['imagem'])
        obj.save()
        image_path = get_Image_path(obj)
        data = True

        return render(request, 'resizer/forms.html', {'form': form, 'data': data})
    else:
        form = FormOpencv()


    return render(request,'resizer/forms.html',{'form':form})

def resize_op_fetch_param(request):
    #fetch all the parameters
    h = request.POST.get('height')
    w = request.POST.get('width')
    m = request.POST.get('resize_method')
    global img_path
    height = int(h);weight=int(w);method=str(m)
    processed_img = wk.setResize(img_path,height,weight,True,method)
    cv2.imwrite("resizer/static/documents/resized_img.jpg",processed_img)
    data = True
    processed = True
    return render(request, 'resizer/forms.html',{'data': data,'processed':processed})

def compress_op_fetch_img(request):
    form = FormOpencv(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = Opencv(imagem=request.FILES['imagem'])
        obj.save()
        image_path = get_Image_path(obj)
        data = True

        return render(request, 'resizer/compress_form.html', {'form': form, 'data': data})
    else:
        form = FormOpencv()

    return render(request, 'resizer/compress_form.html', {'form': form})


def compress_op_fetch_param(request):
    pass


def get_Image_path(obj):
    img_db = obj.imagem
    print img_db
    img_read = img_db.read()
    img_np = np.asarray(bytearray(img_read),dtype="uint8")
    img_op = cv2.imdecode(img_np,cv2.IMREAD_UNCHANGED)

    #delete the previous temp files
    if os.path.isfile('resizer/static/documents/temp_img.jpg'):
        try:
            os.remove('resizer/static/documents/temp_img.jpg')
        except OSError:
            pass

    #Create a local_temp file for processing
    cv2.imwrite('resizer/static/documents/temp_img.jpg',img_op)
    global  img_path
    img_path = 'resizer/static/documents/temp_img.jpg'

    return img_path

