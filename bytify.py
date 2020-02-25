

test_image = "./data/images/(9)A2789015.1.png"

def get_sample_byte_string():
    with open(test_image, 'rb') as f:
        btye_string = f.read()
    return btye_string
