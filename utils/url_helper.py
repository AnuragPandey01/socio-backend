def extract_public_id(url):
    return url.split('/')[-1].split('.')[0]