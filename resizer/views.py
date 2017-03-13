import numpy as np
import cv2
import os
from PIL import Image as Im


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
def enhance_op(request):
    return enhance_op_fetch_img(request)


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
        global image_path
        image_path = get_Image_path(obj)
        data = True

        return render(request, 'resizer/compress_form.html', {'form': form, 'data': data})
    else:
        form = FormOpencv()

    return render(request, 'resizer/compress_form.html', {'form': form})


def compress_op_fetch_param(request):
    size = request.POST.get('size')
    print size
    s = int(size)
    global img_path
    print img_path
    compressed_img = wk.CompressorController(img_path,s)

    data = True
    processed = True
    return render(request, 'resizer/compress_form.html', {'data': data, 'processed': processed})

def enhance_op_fetch_img(request):
    form = FormOpencv(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = Opencv(imagem=request.FILES['imagem'])
        obj.save()
        image_path = get_Image_path(obj)
        data = True

        return render(request, 'resizer/enhance_form.html', {'form': form, 'data': data})
    else:
        form = FormOpencv()
    return render(request, 'resizer/enhance_form.html', {'form': form})


def enhance_op_fetch_param(request):
    Brightness = request.POST.get('Brightness')
    gamma = request.POST.get('gamma')
    Sharpeness = request.POST.get('Sharpeness')
    sharpen_method = request.POST.get('sharpen_method')
    Contrast = request.POST.get('Contrast')
    EqualizeHist  = request.POST.get('EqualizeHist')
    print Brightness,gamma,sharpen_method,Sharpeness,Contrast,EqualizeHist
    if os.path.isfile('resizer/static/documents/enhanced_img.jpg'):
        try:
            os.remove('resizer/static/documents/enhanced_img.jpg')
            print "Successfully Deleted"
        except OSError:
            pass
    global img_path
    path_res = img_path
    b = float(Brightness)
    if b <= 0 :
        if gamma==1:g=True
        else: g = False
        brighten_img = wk.setBrightness(img_path,b,g,True)
        path_res = 'resizer/static/documents/enhanced_img.jpg'
        cv2.imwrite(path_res,brighten_img)

    s = int(Sharpeness)
    if s<=0:
        s_m = int(sharpen_method)
        sharpen_img = wk.setSharpen(path_res,s,s_m)
        path_res = 'resizer/static/documents/enhanced_img.jpg'
        cv2.imwrite(path_res, sharpen_img)

    c = int(Contrast)
    if c<=0:
        print "In contrast"
        if EqualizeHist==1:e_h=True
        else:e_h=False
        contrast_img = wk.setContrast(path_res,c,e_h,True)
        path_res = 'resizer/static/documents/enhanced_img.jpg'
        cv2.imwrite(path_res, contrast_img)
    data = True
    processed = True
    return render(request, 'resizer/enhance_form.html', {'data': data, 'processed': processed})

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
            print "Successfully Deleted"
        except OSError:
            pass

    #Create a local_temp file for processing
    cv2.imwrite('resizer/static/documents/temp_img.jpg',img_op)
    global  img_path
    img_path = 'resizer/static/documents/temp_img.jpg'

    return img_path

