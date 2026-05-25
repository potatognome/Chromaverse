from Chromaspace.tone import get_tone_label

def test_tone_label():
    assert get_tone_label('vivid', 'bright') == 'vivid-bright'
    assert get_tone_label('soft', 'dark') == 'soft-dark'
