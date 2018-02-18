import time
from django.template import Library

register = Library()


@register.filter
def handle_time_stamp(t1):
    delta_time = time.time() - t1 - 8*3600
    lt = time.localtime(t1)
    if delta_time > 24*3600:
        return time.strftime("%Y-%m-%d %H:%M:%S", lt)
    else:
        h = int(delta_time/3600)
        m = int((delta_time-3600*h)/60)
        if h:
            return "{}时{}分之前".format(h, m)
        else:
            return "{}分之前".format(m)
