

test_image = "./data/images/(9)A2789015.1.png"


def get_byte_string_from_image(file):
    with open(file, 'rb') as f:
        btye_string = f.read()
    return btye_string


if __name__ == "__main__":
    print(get_byte_string_from_image(test_image))
