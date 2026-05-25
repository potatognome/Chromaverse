from Chromaspace.hsv import hsv_to_rgb

def test_hsv_to_rgb():
    assert hsv_to_rgb(0, 1, 1) == [255, 0, 0]
    assert hsv_to_rgb(120, 1, 1) == [0, 255, 0]
    assert hsv_to_rgb(240, 1, 1) == [0, 0, 255]
