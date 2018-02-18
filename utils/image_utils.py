import time
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from utils.uauth_utils import get_user_hash


def picture_upload_path(instance, filename):
    """指定上传的路径"""
    suffix = filename[filename.rfind("."):]
    return "{}/{}/{}/{}{}".format(
        instance.user.userinfo.user_hash,
        "albums",
        instance.user.userinfo.latest_albums,
        get_user_hash(filename), suffix)


def transform_datetime_to_timestamp(data):
    """把data里的字典里的add_date和mod_date转化为时间戳"""
    for temp in data:
        if "add_date" in temp:
            temp["add_date"] = time.mktime(temp["add_date"].timetuple())
        if "mod_date" in temp:
            temp["mod_date"] = time.mktime(temp["mod_date"].timetuple())


def handle_upload_pic(pic):
    """处理上传的图片，使他成为一个正方形"""
    im_pic = Image.open(pic)
    w, h = im_pic.size
    if w == h:
        return Image
    if w > h:
        w_start = (w-h)*0.618
        box = (w_start, 0, w_start+h, h)
        region = im_pic.crop(box)
    else:
        h_start = (h-w)*0.618
        box = (0, h_start, w, h_start+w)
        region = im_pic.crop(box)

    region_io = BytesIO()
    region.save(region_io, format=im_pic.format)
    # pic_file = ContentFile(region_io.getvalue())
    pic_file = InMemoryUploadedFile(region_io, None, pic.name, pic.content_type, pic.size, None)

    return pic_file
