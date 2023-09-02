import datetime

def sid(src=None):
    if src == None:
        src = datetime.datetime.utcnow()
    res = datetime.datetime.strftime(src, "%Y%m%d%H%M%S%f")
    return res

def sft(src=None, fmt="s"):
    if fmt == "s":
        fmt = "%Y%m%d"
    elif fmt == "f":
        fmt = "%Y%m%d%H%M%S"
    if src == None:
        src = datetime.datetime.utcnow()
    res = datetime.datetime.strftime(src, fmt)
    return res