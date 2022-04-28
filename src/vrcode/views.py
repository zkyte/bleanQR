import qrcode, base64, requests, urllib.request
from django.shortcuts import render
from django.conf import settings  
from rest_framework.response import Response
from rest_framework.decorators import api_view
from PIL import Image
from uuid import uuid4

from .models import QRCode
from .serializers import InputSerializer, QRCodeSerializer
from .utils import GenerateVCF

# Create your views here.
@api_view(['POST'])
def generate_VCFQR(request):
# #     # {"fname" : "John", "mname" : "", "lname" : "Doe",  "email" : "me@example.org", "phone" : "+1234567", "image" : "https://images.unsplash.com/photo-1612151855475-877969f4a6cc?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8aGQlMjBpbWFnZXxlbnwwfHwwfHw%3D&w=1000&q=80", 
# "role" : "Software developer", "company" : "Zkyte Technologies",  "address_1" : "Fez street No. 3", "address_2" : "Wuse 2, Nigeria Abuja", "remark" : "i'm looking forward to being a competent computer analyst making sure all challenges are duly met in the shortest possible time and clients/customers are well served."}
    data    = {}
    fname   = request.data.get("fname", "")
    lname   = request.data.get("lname", "")
    email   = request.data.get("email", "")
    image   = request.data.get("image", "")
    phone   = request.data.get("phone", "")
    url     = request.data.get("url", "")
    role    = request.data.get("role", "")
    company = request.data.get("company", "")
    remark    = request.data.get("remark", "")
    address_1 = request.data.get("address_1", "")
    address_2 = request.data.get("address_2", "")

    name = "{0};{1}".format(lname, fname)
    dname = "{0} {1}".format(lname, fname)
    user_id = str(uuid4())
    image_path = "{0}/{1}/{2}.png".format(settings.MEDIA_ROOT, "QR", user_id)
    vcf_path = "{0}/{1}/{2}.vcf".format(settings.MEDIA_ROOT, "VCF", user_id)
    error = False
    serializer = InputSerializer(data=request.data)

    try :
        image_formats = ("image/png", "image/jpeg", "image/gif", "image/jpg")
        ext = {"image/png" : "png", "image/jpeg" : "jpeg", "image/gif" : "gif", "image/jpg" : "jpg"}
        site = urllib.request.urlopen(image)
        meta = site.info()

        if meta["content-type"] in image_formats:
            print("it is an image")
            f_name = settings.MEDIA_ROOT + "/photo/Compressed_" + user_id + "." + ext.get(meta["content-type"])
            im = Image.open(requests.get(image, stream=True).raw)
            im.save(fname, ext.get(meta["content-type"]).upper(), optimize = True, quality = 10)
            img_str = "data:image/"+ ext.get(meta["content-type"]) +";base64," + base64.b64encode(requests.get(image, stream=True).content).decode()
            # print(img_str)
  
        else:
            error = True
            msg = "No image found at " + image
    except Exception as e:
        error = True
        msg = str(e)

    if error:
        data["status"] = 400
        data["msg"] = "Wrong Input Provided for image: " + msg 
    elif not serializer.is_valid():
        data["status"] = 400
        data["msg"] = "Wrong Input Provided " + str(serializer.errors)
    else:
        param = {
            "name" : name,
            "dname" : dname,
            "email" : email,
            # "image" : img_str,
            "phone": phone,
            "role" : role,
            "company" : company,
            "url" : url,
            "remark" : remark,
            "address_1" : address_1,
            "address_2" : address_2,


        }

        GenerateVCF(param, vcf_path).generateVCFString()
        with open(vcf_path) as f:
            txt = f.read()

        qr = qrcode.QRCode(
            version=40,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )

        qr.add_data(txt)
        qr.make(fit = False)
        img = qr.make_image()

        # img = qrcode.make(txt)
        img.save(image_path)

        qr = QRCode.objects.create(user_id = user_id, name = dname, img="media/QR/" + user_id + ".png")

        qr_data = QRCodeSerializer(qr).data
        data["status"] = 200
        data["msg"] = "QR code generated succefully"
        data["qr_url"] = qr_data.get("get_image", "")


    return Response(data)
