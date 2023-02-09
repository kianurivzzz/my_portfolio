def check_file(filename):
    allowed_file = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp']

    if filename.split('.')[-1] in allowed_file:
        return True
    return False
