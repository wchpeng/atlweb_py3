from rongcloud import RongCloud

from atlweb_py3.settings import rong_app_secret, rong_app_key


def get_rong_init():
    return RongCloud(app_key=rong_app_key, app_secret=rong_app_secret)


def get_rong_token(user_info):
    r = get_rong_init().User.getToken(
        userId=user_info.user_hash,
        name=user_info.username,
        portraitUri=user_info.avatar.url
    )
    return r.result["token"]


def send_rong_private(from_id, to_id):
    r = get_rong_init().Message.publishPrivate(
        fromUserId=from_id,
        toUserId=to_id,
        objectName="RC:TxtMsg",
        content='{"content":"你好啊", "extra":"222"}'
    )
    print(dir(r))
    return r.result
