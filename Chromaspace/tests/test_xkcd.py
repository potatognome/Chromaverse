from Chromaspace.xkcd import rgb_distance

def test_rgb_distance():
    assert round(rgb_distance([0,0,0], [0,0,0]), 6) == 0
    assert round(rgb_distance([255,0,0], [0,255,0]), 6) == 360.624458
