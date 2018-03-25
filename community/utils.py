from django.contrib.auth.models import User

import re
from community.models import LikeBlog


def select_page_range(page_range, n):
    if n < 3:
        return page_range[:5]
    elif n > len(page_range)-3:
        return page_range[-5:]
    else:
        return page_range[n-3:n+2]


def ridding_html_tag(content, length):
    return re.sub(r"<.+?>|\t|\r|\n", "", content).strip()[:length]


def whether_like(user, data):
    if not user.is_authenticated:
        _add_data_like_false(data)
        return
    li_like = tuple(LikeBlog.objects.filter(user_id=user.id).values_list("blog_id", flat=True))
    if isinstance(data, dict):
        data["like"] = True if data["id"] in li_like else False
    else:
        for temp in data:
            print(dict(temp))
            temp["like"] = True if dict(temp)["id"] in li_like else False


def _add_data_like_false(data):
    if isinstance(data, dict):
        data["like"] = False
    else:
        for temp in data:
            dict(temp)["like"] = False
