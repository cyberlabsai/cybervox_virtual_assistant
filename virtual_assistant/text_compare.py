import difflib

def compare(text_a, text_b):
    seq = difflib.SequenceMatcher(None, text_a, text_b)
    ratio = seq.ratio()
    ratio = "%.2f" % ratio
    return float(ratio)