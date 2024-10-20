def parse_bvid(bvid: str):
    if bvid.startswith('https://'):
        bvid = [segment for segment in bvid.split('?') if segment][0]
        bvid = [segment for segment in bvid.split('/') if segment][-1]
        return bvid
    return bvid
