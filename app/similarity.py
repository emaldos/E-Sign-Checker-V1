import io, numpy as np
from PIL import Image

def _gray(data, size):
    return Image.open(io.BytesIO(data)).convert("L").resize(size)

def _ham(a, b):
    return bin(a ^ b).count("1")

def dhash_bits(data):
    arr = np.asarray(_gray(data, (9, 8)), dtype=np.int16)
    diff = arr[:, 1:] > arr[:, :-1]
    bits = diff.astype(np.uint8).flatten()
    v = 0
    for b in bits:
        v = (v << 1) | int(b)
    return v

def dhash_similarity(a, b):
    d = _ham(dhash_bits(a), dhash_bits(b))
    return (1.0 - d / 64.0) * 100.0

def pixel_similarity(a, b):
    A = np.asarray(_gray(a, (256, 256)), dtype=np.float32)
    B = np.asarray(_gray(b, (256, 256)), dtype=np.float32)
    diff = np.abs(A - B).mean()
    s = max(0.0, min(1.0, 1.0 - diff / 255.0))
    return s * 100.0

def combined_similarity(a, b, w_pixel=0.5, w_dhash=0.5):
    p = pixel_similarity(a, b)
    d = dhash_similarity(a, b)
    return w_pixel*p + w_dhash*d
