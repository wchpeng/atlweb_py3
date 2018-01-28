from utils.uauth import get_user_hash


def picture_upload_path(instance, filename):
    suffix = filename[filename.rfind("."):]
    return "{}/{}/{}/{}{}".format(
        instance.userinfo.user_hash,
        "albums",
        instance.userinfo.latest_albums,
        get_user_hash(filename), suffix)
