# ============================================================
# Chapter 6: Image Processing
# "From MATLAB to Python for Engineers and Scientists"
# Python Reference Code
# Install: pip install opencv-python scikit-image Pillow
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import skimage
from skimage import filters, morphology, measure, exposure
from skimage.morphology import disk
import warnings
warnings.filterwarnings('ignore')


# ============================================================
# A NOTE ON PYTHON IMAGE LIBRARIES
# ============================================================
# Unlike MATLAB's single Image Processing Toolbox, Python has
# three commonly used libraries, each with strengths:
#
#  OpenCV (cv2)      — fast, industry-standard, great for real-time
#                      and computer vision pipelines
#  scikit-image      — NumPy-native, Pythonic, best for scientific work
#  Pillow (PIL)      — simple file I/O, basic transforms, format support
#
# Recommendation:
#   Use scikit-image for scientific/engineering analysis (closest to MATLAB)
#   Use OpenCV when speed matters or for video/camera work
#   Use Pillow for reading/writing image files and simple operations
#
# This chapter shows all three so you can choose the right tool.


# ============================================================
# 6.1 Reading, Displaying, and Writing Images
# ============================================================

# --- Using scikit-image (recommended for science) ---
img_rgb  = skimage.io.imread('sample.jpg')       # uint8 H×W×3
img_gray = skimage.io.imread('sample_gray.jpg')  # uint8 H×W

# --- Using OpenCV ---
img_cv   = cv2.imread('sample.jpg')              # reads as BGR, not RGB!
img_cv_gray = cv2.imread('sample_gray.jpg', cv2.IMREAD_GRAYSCALE)

# *** CRITICAL: OpenCV uses BGR channel order, not RGB ***
# MATLAB imread → RGB  (red channel first)
# OpenCV imread → BGR  (blue channel first)
# If you read with OpenCV and display/process expecting RGB, colors will be wrong.
# Always convert when needed:
img_cv_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

# Display with matplotlib (always use RGB)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].imshow(img_rgb);      axes[0].set_title('Original RGB');  axes[0].axis('off')
axes[1].imshow(img_gray, cmap='gray'); axes[1].set_title('Grayscale'); axes[1].axis('off')
plt.tight_layout(); plt.savefig('ch6_read.png', dpi=150); plt.show()

# Convert RGB to grayscale
from skimage.color import rgb2gray
img_gray_f = rgb2gray(img_rgb)          # returns float64 in [0,1]  — MATLAB: rgb2gray returns uint8
img_gray_u = (img_gray_f * 255).astype(np.uint8)   # convert back to uint8 if needed

# Image properties
print(img_rgb.shape)        # (H, W, 3)   — MATLAB: size(img) = [H, W, 3]
print(img_rgb.dtype)        # uint8
print(img_rgb.max())        # 255

# Write image
skimage.io.imsave('output_gray.png', img_gray_u)     # MATLAB: imwrite(gray,'output_gray.png')
skimage.io.imsave('output_rgb.jpg',  img_rgb)


# ============================================================
# 6.2 Pixel Access and Array Operations
# ============================================================
# Images in Python are just NumPy arrays — use standard indexing.

img = skimage.io.imread('sample.jpg')

# Access pixel — note [row, col] = [y, x] order
pixel = img[100, 200, :]    # all channels   — MATLAB: img(100,200,:)
red   = img[100, 200, 0]    # red channel    — MATLAB: img(100,200,1)

# Crop region of interest (ROI)
roi = img[50:200, 80:300, :]    # MATLAB: img(50:200, 80:300, :)
                                 # Note: Python end is exclusive, MATLAB end is inclusive

# Convert to float for arithmetic (avoid uint8 overflow)
img_f = img.astype(np.float64) / 255.0     # MATLAB: double(img)/255

# *** uint8 overflow is a silent bug ***
# uint8 values clip at 255. Adding two uint8 images can overflow.
# MATLAB's Image Toolbox handles this automatically in many functions.
# In Python/NumPy: always convert to float before arithmetic.
#   Bad:  result = img1 + img2          (may overflow if uint8)
#   Good: result = img1.astype(float) + img2.astype(float)

# Flip and rotate
img_flip_h = np.fliplr(img)     # MATLAB: fliplr(img)
img_flip_v = np.flipud(img)     # MATLAB: flipud(img)
img_rot90  = np.rot90(img)      # MATLAB: rot90(img)

# Resize using skimage
from skimage.transform import resize, rescale
img_small = rescale(img_f, 0.5, anti_aliasing=True, channel_axis=2)   # MATLAB: imresize(img,0.5)
img_fixed = resize(img_f, (256, 256), anti_aliasing=True)              # MATLAB: imresize(img,[256,256])


# ============================================================
# 6.3 Color Space Conversion
# ============================================================
from skimage.color import rgb2gray, rgb2hsv, rgb2lab, hsv2rgb

img   = skimage.io.imread('sample.jpg')
img_f = img.astype(np.float64) / 255.0

# RGB → Grayscale
gray = rgb2gray(img_f)              # float64 [0,1]    — MATLAB: rgb2gray(img)

# RGB → HSV
hsv  = rgb2hsv(img_f)              # H,S,V all in [0,1] — MATLAB: rgb2hsv(double(img)/255)

# RGB → LAB
lab  = rgb2lab(img_f)              # MATLAB: rgb2lab(double(img)/255)

# Adjust brightness via HSV
hsv_bright        = hsv.copy()
hsv_bright[:,:,2] = np.clip(hsv_bright[:,:,2] * 1.3, 0, 1)  # increase V
img_bright        = (hsv2rgb(hsv_bright) * 255).astype(np.uint8)
# MATLAB: hsv(:,:,3) = min(hsv(:,:,3)*1.3, 1); img = uint8(hsv2rgb(hsv)*255)


# ============================================================
# 6.4 Filtering and Smoothing
# ============================================================
from skimage import filters
from scipy.ndimage import median_filter, convolve

img  = skimage.io.imread('sample.jpg')
gray = rgb2gray(img)    # float64 [0,1]

# Gaussian blur
sigma    = 2
blur     = filters.gaussian(gray, sigma=sigma)      # MATLAB: imgaussfilt(gray,sigma)

# Median filter (robust to salt-and-pepper noise)
gray_u8  = (gray * 255).astype(np.uint8)
med      = median_filter(gray_u8, size=5)           # MATLAB: medfilt2(gray,[5,5])

# Unsharp masking (sharpening)
sharp    = filters.unsharp_mask(gray, radius=2, amount=1.0)  # MATLAB: imsharpen(...)

# Custom kernel convolution
kernel   = np.ones((5, 5)) / 25.0                  # 5×5 averaging kernel
avg      = convolve(gray, kernel)                   # MATLAB: imfilter(gray,fspecial('average',[5,5]))

# Display comparison
fig, axes = plt.subplots(1, 4, figsize=(14, 4))
for ax, im, title in zip(axes,
                          [gray, blur, med, sharp],
                          ['Original', 'Gaussian Blur', 'Median', 'Sharpened']):
    ax.imshow(im, cmap='gray')
    ax.set_title(title); ax.axis('off')
plt.tight_layout(); plt.savefig('ch6_filters.png', dpi=150); plt.show()


# ============================================================
# 6.5 Edge Detection
# ============================================================
from skimage import feature

img  = skimage.io.imread('sample.jpg')
gray = rgb2gray(img)

# Sobel
edges_sobel = filters.sobel(gray)                   # MATLAB: edge(gray,'Sobel')

# Canny (best general-purpose edge detector)
edges_canny = feature.canny(gray, sigma=1.5,
                             low_threshold=0.1,
                             high_threshold=0.3)    # MATLAB: edge(gray,'Canny',[0.1,0.3])

# Prewitt
edges_prev  = filters.prewitt(gray)                 # MATLAB: edge(gray,'Prewitt')

# Scharr (similar to Sobel but more isotropic — no MATLAB equivalent)
edges_scharr = filters.scharr(gray)

fig, axes = plt.subplots(1, 4, figsize=(14, 4))
for ax, im, title in zip(axes,
                          [edges_sobel, edges_canny, edges_prev, edges_scharr],
                          ['Sobel', 'Canny', 'Prewitt', 'Scharr']):
    ax.imshow(im, cmap='gray')
    ax.set_title(title); ax.axis('off')
plt.tight_layout(); plt.savefig('ch6_edges.png', dpi=150); plt.show()


# ============================================================
# 6.6 Morphological Operations
# ============================================================
from skimage import morphology, filters
from skimage.morphology import disk, binary_erosion, binary_dilation
from skimage.morphology import binary_opening, binary_closing
from scipy.ndimage import binary_fill_holes

img  = skimage.io.imread('sample.jpg')
gray = rgb2gray(img)

# Binarize (threshold)
thresh = filters.threshold_otsu(gray)    # automatic threshold — MATLAB: imbinarize(gray,'adaptive')
bw     = gray < thresh                   # dark objects on light background

# Structuring element
se = disk(5)                             # MATLAB: strel('disk',5)

# Basic operations
eroded  = binary_erosion(bw,  se)        # MATLAB: imerode(bw, se)
dilated = binary_dilation(bw, se)        # MATLAB: imdilate(bw, se)
opened  = binary_opening(bw,  se)        # MATLAB: imopen(bw, se)
closed  = binary_closing(bw,  se)        # MATLAB: imclose(bw, se)

# Fill holes
filled  = binary_fill_holes(bw)          # MATLAB: imfill(bw,'holes')

# Remove small objects (< 100 pixels)
clean   = morphology.remove_small_objects(bw, min_size=100)  # MATLAB: bwareaopen(bw,100)

fig, axes = plt.subplots(2, 3, figsize=(12, 7))
for ax, im, title in zip(axes.ravel(),
    [bw, eroded, dilated, opened, closed, clean],
    ['Binary', 'Eroded', 'Dilated', 'Opened', 'Closed', 'Small objects removed']):
    ax.imshow(im, cmap='gray'); ax.set_title(title); ax.axis('off')
plt.tight_layout(); plt.savefig('ch6_morphology.png', dpi=150); plt.show()


# ============================================================
# 6.7 Histogram and Histogram Equalization
# ============================================================

img  = skimage.io.imread('sample.jpg')
gray = rgb2gray(img)

# Image histogram
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(gray.ravel(), bins=256, range=(0, 1), color='gray')
axes[0].set_title('Grayscale Histogram')        # MATLAB: imhist(gray)
axes[0].set_xlabel('Pixel value'); axes[0].set_ylabel('Count')

# Histogram equalization
eq   = exposure.equalize_hist(gray)             # MATLAB: histeq(gray)
axes[1].hist(eq.ravel(), bins=256, range=(0, 1), color='steelblue')
axes[1].set_title('Equalized Histogram')
plt.tight_layout(); plt.savefig('ch6_histogram.png', dpi=150); plt.show()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].imshow(gray, cmap='gray'); axes[0].set_title('Original');  axes[0].axis('off')
axes[1].imshow(eq,   cmap='gray'); axes[1].set_title('Equalized'); axes[1].axis('off')
plt.tight_layout(); plt.savefig('ch6_equalize.png', dpi=150); plt.show()


# ============================================================
# 6.8 Real Engineering Case: Defect Detection Workflow
# ============================================================
# Industrial inspection pipeline:
# Simulate → Denoise → Threshold → Morphology → Label → Measure
# This mirrors the kind of surface inspection work done in
# manufacturing quality control.

from skimage import measure

rng = np.random.default_rng(seed=42)

# Simulate a uniform surface with circular defects
img_size = (256, 256)
surface  = np.full(img_size, 200, dtype=np.uint8)

defect_params = []
for _ in range(8):
    r  = rng.integers(10, 21)
    cx = rng.integers(r + 1, img_size[1] - r)
    cy = rng.integers(r + 1, img_size[0] - r)
    Y, X = np.ogrid[:img_size[0], :img_size[1]]
    mask = (X - cx)**2 + (Y - cy)**2 <= r**2
    surface[mask] = rng.integers(30, 81)
    defect_params.append((cx, cy, r))

# Add Gaussian noise
noise   = rng.normal(0, 3, img_size).astype(np.int16)
surface = np.clip(surface.astype(np.int16) + noise, 0, 255).astype(np.uint8)

# Step 1: Normalize and smooth
surf_f  = surface.astype(np.float64) / 255.0
smooth  = filters.gaussian(surf_f, sigma=1.5)          # MATLAB: imgaussfilt(surface,1.5)

# Step 2: Threshold to detect dark defects
thresh  = 150 / 255.0
bw_def  = smooth < thresh                              # MATLAB: smooth < thresh

# Step 3: Morphological cleanup
se      = disk(3)
bw_def  = binary_opening(bw_def,  se)                 # MATLAB: imopen(bw_def, se)
bw_def  = binary_fill_holes(bw_def)                   # MATLAB: imfill(bw_def,'holes')
bw_def  = morphology.remove_small_objects(bw_def, min_size=50)

# Step 4: Label connected regions and measure properties
labeled = measure.label(bw_def)                        # MATLAB: bwlabel(bw_def)
props   = measure.regionprops(labeled)                 # MATLAB: regionprops(labeled,...)

print(f"Detected defects: {len(props)}")
for i, p in enumerate(props):
    cy, cx = p.centroid
    print(f"  Defect {i+1}: Area = {p.area} px, "
          f"Center = ({cx:.1f}, {cy:.1f}), "
          f"BBox = {p.bbox}")

# Step 5: Visualize results
fig, axes = plt.subplots(1, 3, figsize=(13, 4))

axes[0].imshow(surface, cmap='gray', vmin=0, vmax=255)
axes[0].set_title('Original Surface'); axes[0].axis('off')

axes[1].imshow(bw_def, cmap='gray')
axes[1].set_title('Detected Defects'); axes[1].axis('off')

axes[2].imshow(surface, cmap='gray', vmin=0, vmax=255)
for p in props:
    min_r, min_c, max_r, max_c = p.bbox
    import matplotlib.patches as patches
    rect = patches.Rectangle(
        (min_c, min_r), max_c - min_c, max_r - min_r,
        linewidth=2, edgecolor='red', facecolor='none'
    )
    axes[2].add_patch(rect)
    cy, cx = p.centroid
    axes[2].plot(cx, cy, 'r+', markersize=8, markeredgewidth=2)
axes[2].set_title('Defects Highlighted'); axes[2].axis('off')

plt.tight_layout()
plt.savefig('ch6_defect_detection.png', dpi=150, bbox_inches='tight')
plt.show()


# ============================================================
# Chapter 6 Summary: Key Differences to Remember
# ============================================================
#
# 1. THREE LIBRARIES, not one toolbox:
#    scikit-image → scientific analysis (use this most)
#    OpenCV       → speed, real-time, video
#    Pillow       → simple file I/O
#
# 2. OpenCV reads BGR not RGB — always convert:
#    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
#
# 3. Convert to float before arithmetic to avoid uint8 overflow:
#    img_f = img.astype(np.float64) / 255.0
#
# 4. rgb2gray returns float [0,1] not uint8 — unlike MATLAB.
#
# 5. imshow needs origin='lower' for scientific data,
#    but for image display use default (origin='upper').
#
# 6. regionprops centroid is (row, col) = (y, x) order.
#    Be careful when plotting: use centroid[1] for x-axis.
