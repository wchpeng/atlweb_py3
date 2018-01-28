import hashlib
import time


# 加密
def get_user_hash(val):
    sha1 = hashlib.sha1()
    sha1.update((str(val)+str(time.time())).encode())
    return sha1.hexdigest()


def avatar_upload_path(instance, filename):
    suffix = filename[filename.rfind("."):]
    return "{}/{}{}".format(instance.userinfo.user_hash, get_user_hash(filename), suffix)
