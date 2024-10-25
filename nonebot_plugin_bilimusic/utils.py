def parse_bvid(bvid: str):
    if 'https://www.bilibili.com/' in bvid:
        bvid = [segment for segment in bvid.split('?') if segment][0]
        bvid = [segment for segment in bvid.split('/') if segment][-1]
        return bvid
    return bvid
