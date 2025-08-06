# cs_image_dct.py
import numpy as np
import matplotlib.pyplot as plt
from skimage.data import astronaut
from skimage.transform import resize
from skimage.util import img_as_float
from scipy.fftpack import dct, idct
import spgl1

# -------------------------------
# 1. Load and preprocess image
# -------------------------------
image_rgb = img_as_float(astronaut())
image_gray = np.mean(image_rgb, axis=2)
image_resized = resize(image_gray, (128, 128), anti_aliasing=True)
h, w = image_resized.shape
N = h * w
x_true = image_resized.flatten()

# -------------------------------
# 2. Define DCT basis: x = idct2d(s)
# -------------------------------
def dct2d(img):
    return dct(dct(img.T, norm='ortho').T, norm='ortho')

def idct2d(coeff):
    return idct(idct(coeff.T, norm='ortho').T, norm='ortho')

# Flatten 2D DCT
s_true = dct2d(image_resized).flatten()

# -------------------------------
# 3. Random Gaussian measurements
# -------------------------------
m = 6000  # 更多测量提高成功率
A = np.random.randn(m, N)
A = A / np.linalg.norm(A, axis=0)  # 必须列归一化！

# Measurement: y = A @ x_true
y = A @ x_true

# -------------------------------
# 4. Define AΨ: A @ idct2d(s)
# -------------------------------
def apply_A_psi(s_vec):
    s_img = s_vec.reshape((h, w))
    x_img = idct2d(s_img)
    return A @ x_img.flatten()

def apply_AT_psi(y_vec):
    x_flat = A.T @ y_vec
    x_img = x_flat.reshape((h, w))
    s_img = dct2d(x_img)
    return s_img.flatten()

from scipy.sparse.linalg import LinearOperator
A_op = LinearOperator(
    shape=(m, N),
    matvec=lambda s: apply_A_psi(s),
    rmatvec=lambda y: apply_AT_psi(y)
)

# -------------------------------
# 5. Solve with SPGL1: recover s in DCT domain
# -------------------------------
sigma = 1e-4
s_init = np.zeros(N)
print("Starting SPGL1...")

try:
    s_rec, _, _, info = spgl1.spgl1(A_op, y, tau=0, sigma=sigma, x0=s_init, verbosity=3)
    print("SPGL1 finished.")
except Exception as e:
    print("SPGL1 failed:", str(e))
    s_rec = np.zeros(N)

# -------------------------------
# 6. Reconstruct image
# -------------------------------
if np.any(s_rec):
    s_rec_img = s_rec.reshape((h, w))
    x_rec_img = idct2d(s_rec_img)
else:
    x_rec_img = np.zeros((h, w))

# -------------------------------
# 7. Visualization (All English)
# -------------------------------
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(image_resized, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(x_rec_img, cmap='gray')
plt.title('Reconstructed Image')
plt.axis('off')

plt.subplot(1, 3, 3)
error_map = np.abs(image_resized - x_rec_img)
plt.imshow(error_map, cmap='hot', vmin=0, vmax=error_map.max())
plt.title('Error Map')
plt.colorbar()
plt.axis('off')

plt.suptitle('Compressive Sensing: Random Sampling + SPGL1 (DCT Sparsity)', fontsize=16)
plt.tight_layout()
plt.show()

# -------------------------------
# 8. Print Metrics (English)
# -------------------------------
l2_error = np.linalg.norm(image_resized - x_rec_img)
linf_error = np.max(np.abs(image_resized - x_rec_img))
psnr = 20 * np.log10(1.0 / (np.sqrt(np.mean((image_resized - x_rec_img)**2)) + 1e-8))

print(f"Compression: {N} -> {m}, Ratio = {N/m:.1f}x")
print(f"L2 Error: {l2_error:.4f}")
print(f"L∞ Error: {linf_error:.4f}")
print(f"PSNR: {psnr:.2f} dB")