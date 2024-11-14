
import  IPython.display as dsp

import base64
import io
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


def extract_pix(doc, pg_num, dpi = 300):
    page = doc.load_page(pg_num)
    pixmap = page.get_pixmap(dpi=dpi)
    return pixmap

def pix_to_pil(pix):
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

def improve_img(img_pil):
    # Enhance image for better OCR results
    enhancer = ImageEnhance.Contrast(img_pil)
    image_enhanced = enhancer.enhance(2)
    image_filtered = image_enhanced.filter(ImageFilter.SHARPEN)

    # Convert image to grayscale
    image_gray = image_filtered.convert('L')
    return image_gray

def pil_to_byte_arr(pil_img):
    img_byte_arr = io.BytesIO()
    pil_img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue() 

def draw_img(img_pil):
    img_byte_arr = io.BytesIO()
    img_pil.save(img_byte_arr, format='PNG')
    dsp.display(dsp.Image(data = img_byte_arr.getvalue(), width=600))