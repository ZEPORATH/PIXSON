'''
    THE STATEMENTS IN  def main() ARE JUST FOR TESTING,
    THE MAIN IMPORTANCE IS ON THE WORKER CLASS AND ITS METHODS
    REGARDING THE ENTRY POINT AND EXIT POINTS, THERE WILL BE CONTROLLER CLASS
    CLASS WORKER -- FINISHED
    CONTROLLER CLASS - PENDING (CONTROLS ALL SORTS OF ENTRY AND EXIT POINTS)

'''
import cv2
import numpy as np
import os
from PIL import Image as Im


class worker:
    def __init__(self):
        pass

    def setResize(self, image1, H, W,advance_op, method):
        ##User can choose which interpolation method to use for resizing
        # cv2.INTER_NEAREST
        # cv2.INTER_LINEAR
        # cv2.INTER_AREA
        # cv2.INTER_CUBIC
        # cv2.INTER_LANCZOS4
        m = {
            'cv2.INTER_NEAREST':cv2.INTER_NEAREST,
            'cv2.INTER_LINEAR':cv2.INTER_LINEAR,
            'cv2.INTER_AREA':cv2.INTER_AREA,
            'cv2.INTER_CUBIC':cv2.INTER_CUBIC,
            'cv2.INTER_LANCZOS4':cv2.INTER_LANCZOS4,
        }
        image = cv2.imread(image1,-1)
        if advance_op == True:
            self.resized = cv2.resize(image, (W, H), interpolation=m[method])
        else:
            self.resized = cv2.resize(image, (W, H), interpolation=cv2.INTER_CUBIC)
        return self.resized

    def setCompressor(self, path, size):
        fileinfo = os.stat(path)
        orig_size = fileinfo.st_size
        res_size = orig_size
        quality1 = 100
        res_path = path
        image = cv2.imread(path, -1)
        if orig_size < size:
            return image
        else:
            im = Im.open(path)
            while (res_size >= size and quality1 >= 0):
                quality1 -= 5
                im.save('res_compress_img.jpg', quality=quality1, optimise=True)
                res_size = os.stat('res_compress_img.jpg').st_size
            image = cv2.imread('res_compress_img.jpg', -1)
            return image

            '''
            This code segment is bit buggy, and will be paid attention in later imporovents


            i = 0
            while res_size >= size:

                im = Im.open(res_path)
                while (res_size>=size and quality1 >= 0):
                    quality1 -= 5
                    print "inside while" , i
                    im.save('res_compress_img.jpg',quality = quality1, optimise = True)
                    res_size = os.stat('res_compress_img.jpg').st_size
                print quality1
                #im.save('res_compress_img.jpg',quality = quality1, optimise = True)
                quality1 = 100
                #im.save('res_compress_img.jpg',quality = quality1, optimise = True)
                res_size = os.stat('res_compress_img.jpg').st_size
                res_path = 'res_compress_img.jpg'
                i += 1
        image = cv2.imread('res_compress_img.jpg',-1)
        return image



            im = Im.open(path)
            while(res_size > size and quality>=0):
                quality -= 10
                cv2.imwrite('res_compress_img.jpg', image,[int(cv2.IMWRITE_PNG_COMPRESSION),9])
                res_size = os.stat('res_compress_img.jpg').st_size
        res = cv2.imread('res_compress_img.jpg',-1)
        return res
    '''

    def fileInfo(self, path):
        # Returns a list of strings with basic file info
        name = os.path.basename(path)
        size = os.stat(path).st_size
        filetype = name.split('.')[-1]
        l = []
        l.append(name);
        l.append(size), l.append(filetype)
        return l

    def setSharpen(self, path, param, typeof):
        # generating the kernels
        # kernel_sharpen_1 = simple_sharpening
        # kernel_sharpen_2 = excessive_sharpening
        # kernel_sharpen_3 = Edge_sharpening
        # case 4 = Gaussian Unsgarp Masking, param, plays a role here
        #        use of case 4 , should be avoided, it's complete implementation is pending
        kernel_sharpen_1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        kernel_sharpen_2 = np.array([[1, 1, 1], [1, -7, 1], [1, 1, 1]])
        kernel_sharpen_3 = np.array([[-1, -1, -1, -1, -1],
                                     [-1, 2, 2, 2, -1],
                                     [-1, 2, 8, 2, -1],
                                     [-1, 2, 2, 2, -1],
                                     [-1, -1, -1, -1, -1]]) / 8.0
        img = cv2.imread(path, -1)
        if typeof == 1:
            output1 = cv2.filter2D(img, -1, kernel_sharpen_1)
            return output1
        elif typeof == 2:
            output2 = cv2.filter2D(img, -1, kernel_sharpen_2)
            return output2
        elif typeof == 3:
            output3 = cv2.filter2D(img, -1, kernel_sharpen_3)
            return output3
        elif typeof == 4:
            # Unsharp Mask technique
            gaussian3 = cv2.GaussianBlur(img, (9, 9), 25.0)
            unsharp_img = cv2.addWeighted(img, 1.6, gaussian3, -0.5, 0, img)
            return unsharp_img

    def setContrast(self, path, param, flag, optimise_flag):
        if flag == 'auto':
            '''
            img = cv2.imread(path,-1)
            #convert to yuv form, for better equalization
            img_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)

            #equalize Histogram of the Y- channel
            img_yuv[:,:,0] = cv2.equalizeHist(img[:,:,0])

            #convert YUV back to RGB
            img_out = cv2.cvtColor(img_yuv,cv2.COLOR_YUV2BGR)

            return img_out
            '''
            img = cv2.imread(path, -1)
            return histogram_equalize(img)
        else:
            img = cv2.imread(path, -1)
            contrast = param[0]
            # brightnes = param[1]
            from PIL import ImageEnhance
            im = Im.open(path)
            enhancer = ImageEnhance.Contrast(im)
            if contrast < 50:

                factor = contrast * 0.02
                enhancer.enhance(factor).save('contrast_img.jpg', optimise=optimise_flag)
                return cv2.imread('contrast_img.jpg', -1)
            elif contrast > 50:
                factor = contrast * 0.02
                enhancer.enhance(factor).save('contrast_img.jpg', optimise=optimise_flag)
                return cv2.imread('contrast_img.jpg', -1)
            else:
                return img

    def setBrightness(self, path, params, flag_gama, optimise_flag):
        # Gammma Enhancement focuses on your perceptionto colors
        # also known as power law transform
        # if params -s for gamma , it must be in range 0 - 3.5
        if flag_gama == True:
            image = cv2.imread(path, -1)
            gama = params[1]
            adjusted = adjust_gamma(image, gama)
            cv2.imwrite('Brightness_img.jpg', adjusted)
            return cv2.imread('Brightness_img.jpg')
        else:
            # Here PArams value should not exceed 300
            from PIL import ImageEnhance
            im = Im.open(path)
            enhancer = ImageEnhance.Contrast(im)
            factor = params[1] * 0.02

            enhancer.enhance(factor).save('Brightness_img.jpg', optimise=optimise_flag)
            return cv2.imread('Brightness_img.jpg')

    def setRotate(self, path, angle):
        img = Im.open(path)
        img2 = img.rotate(angle)
        img2.save('rotated_img.jpg')
        return cv2.imread('rotated_img.jpg')


def main():
    w = worker()
    img = cv2.imread('photo.jpg', -1)
    # res2 = w.setCompressor('photo.jpg',20480)
    print w.fileInfo('aurora.jpg')
    # cv2.imwrite('sharpen_image.jpg',w.setSharpen('photo.jpg',0,4))
    # cv2.imwrite('contrast_image.jpg',w.setContrast('photo.jpg',[100,50],'no auto',optimize_flag= True))
    # w.setBrightness('photo.jpg',[0,300],False,True)
    # w.setRotate('photo.jpg',90)


def histogram_equalize(img):
    b, g, r = cv2.split(img)
    red = cv2.equalizeHist(r)
    green = cv2.equalizeHist(g)
    blue = cv2.equalizeHist(b)
    return cv2.merge((blue, green, red))


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


# if __name__ == "__main__":
#     main()

