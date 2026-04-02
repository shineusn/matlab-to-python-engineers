% ============================================================
% Chapter 6: Image Processing
% "From MATLAB to Python for Engineers and Scientists"
% MATLAB Reference Code
% Requires: Image Processing Toolbox
% ============================================================

%% 6.1 Reading, Displaying, and Writing Images
% ------------------------------------------------------------

% Read image
img_rgb  = imread('sample.jpg');        % returns uint8 H×W×3
img_gray = imread('sample_gray.jpg');   % grayscale uint8 H×W

% Display
figure;
imshow(img_rgb)
title('Original RGB Image')

% Convert RGB to grayscale
img_gray2 = rgb2gray(img_rgb);

figure;
imshow(img_gray2)
title('Grayscale')

% Image properties
disp(size(img_rgb))     % [H, W, 3]
disp(class(img_rgb))    % 'uint8'
disp(max(img_rgb(:)))   % 255

% Write image
imwrite(img_gray2, 'output_gray.png')
imwrite(img_rgb,   'output_rgb.jpg',  'Quality', 95)


%% 6.2 Pixel Access and Array Operations
% ------------------------------------------------------------
img = imread('sample.jpg');

% Access single pixel  [row, col, channel]
pixel = img(100, 200, :);       % all 3 channels at (100,200)
red   = img(100, 200, 1);       % red channel only

% Crop region of interest
roi = img(50:200, 80:300, :);   % rows 50-200, cols 80-300

% Convert to double for arithmetic (avoid uint8 overflow)
img_d = double(img) / 255;      % normalize to [0, 1]

% Flip and rotate
img_flip_h = fliplr(img);       % flip horizontal
img_flip_v = flipud(img);       % flip vertical
img_rot90  = rot90(img);        % rotate 90° counterclockwise

% Resize
img_small = imresize(img, 0.5);             % 50% of original size
img_fixed = imresize(img, [256, 256]);      % exact size


%% 6.3 Color Space Conversion
% ------------------------------------------------------------
img = imread('sample.jpg');

% RGB → Grayscale
gray = rgb2gray(img);

% RGB → HSV
hsv = rgb2hsv(double(img)/255);

% RGB → LAB
lab = rgb2lab(double(img)/255);

% Adjust brightness (HSV manipulation)
hsv_bright        = hsv;
hsv_bright(:,:,3) = min(hsv_bright(:,:,3) * 1.3, 1);   % increase V channel
img_bright        = uint8(hsv2rgb(hsv_bright) * 255);


%% 6.4 Filtering and Smoothing
% ------------------------------------------------------------
img  = imread('sample.jpg');
gray = rgb2gray(img);

% Gaussian blur
sigma   = 2;
img_blur = imgaussfilt(gray, sigma);

% Median filter (good for salt-and-pepper noise)
img_med = medfilt2(gray, [5, 5]);

% Sharpen
img_sharp = imsharpen(gray, 'Radius', 2, 'Amount', 1);

% Custom kernel convolution
kernel    = fspecial('average', [5, 5]);    % 5×5 averaging kernel
img_avg   = imfilter(gray, kernel);

% Unsharp masking
kernel_um = fspecial('unsharp', 0.5);
img_um    = imfilter(double(gray)/255, kernel_um);

% Display comparison
figure;
subplot(1,3,1); imshow(gray);     title('Original')
subplot(1,3,2); imshow(img_blur); title('Gaussian Blur')
subplot(1,3,3); imshow(img_med);  title('Median Filter')


%% 6.5 Edge Detection
% ------------------------------------------------------------
gray = rgb2gray(imread('sample.jpg'));

% Sobel edge detection
edges_sobel = edge(gray, 'Sobel');

% Canny edge detection
edges_canny = edge(gray, 'Canny', [0.1, 0.3]);

% Prewitt
edges_prev  = edge(gray, 'Prewitt');

% Display
figure;
subplot(1,3,1); imshow(edges_sobel); title('Sobel')
subplot(1,3,2); imshow(edges_canny); title('Canny')
subplot(1,3,3); imshow(edges_prev);  title('Prewitt')


%% 6.6 Morphological Operations
% ------------------------------------------------------------
% Work on binary images
gray   = rgb2gray(imread('sample.jpg'));
bw     = imbinarize(gray, 'adaptive');     % adaptive thresholding

% Structuring element
se_disk = strel('disk', 5);
se_rect = strel('rectangle', [3, 7]);

% Erosion and dilation
eroded  = imerode(bw,  se_disk);
dilated = imdilate(bw, se_disk);

% Opening (erode then dilate — removes small objects)
opened  = imopen(bw, se_disk);

% Closing (dilate then erode — fills small holes)
closed  = imclose(bw, se_disk);

% Fill holes
filled  = imfill(bw, 'holes');

% Remove small objects
clean   = bwareaopen(bw, 100);    % remove objects smaller than 100 px

figure;
subplot(2,3,1); imshow(bw);      title('Binary')
subplot(2,3,2); imshow(eroded);  title('Eroded')
subplot(2,3,3); imshow(dilated); title('Dilated')
subplot(2,3,4); imshow(opened);  title('Opened')
subplot(2,3,5); imshow(closed);  title('Closed')
subplot(2,3,6); imshow(clean);   title('Small objects removed')


%% 6.7 Histogram and Histogram Equalization
% ------------------------------------------------------------
gray = rgb2gray(imread('sample.jpg'));

% Image histogram
figure;
imhist(gray)
title('Grayscale Histogram')

% Histogram equalization (enhance contrast)
eq   = histeq(gray);

figure;
subplot(1,2,1); imshow(gray); title('Original')
subplot(1,2,2); imshow(eq);   title('Histogram Equalized')


%% 6.8 Real Engineering Case: Defect Detection Workflow
% ------------------------------------------------------------
% Typical industrial inspection pipeline:
% Load → Grayscale → Filter → Threshold → Morphology → Measure

% Simulate a surface with defects
img_size  = [256, 256];
surface   = uint8(200 * ones(img_size));        % uniform background
rng(42);

% Add random dark defects (circular blobs)
for i = 1:8
    r  = randi([10, 20]);
    cx = randi([r+1, img_size(2)-r]);
    cy = randi([r+1, img_size(1)-r]);
    [X, Y] = meshgrid(1:img_size(2), 1:img_size(1));
    mask   = (X-cx).^2 + (Y-cy).^2 <= r^2;
    surface(mask) = uint8(randi([30, 80]));
end

% Add noise
surface = imnoise(surface, 'gaussian', 0, 0.005);

% Step 1: Gaussian smoothing
smooth = imgaussfilt(surface, 1.5);

% Step 2: Threshold to detect dark defects
thresh  = 150;
bw_def  = smooth < thresh;

% Step 3: Morphological cleanup
se      = strel('disk', 3);
bw_def  = imopen(bw_def, se);
bw_def  = imfill(bw_def, 'holes');

% Step 4: Label and measure
labeled = bwlabel(bw_def);
props   = regionprops(labeled, 'Area', 'Centroid', 'BoundingBox');

fprintf('Detected defects: %d\n', length(props))
for i = 1:length(props)
    fprintf('  Defect %d: Area = %d px, Center = (%.1f, %.1f)\n', ...
        i, props(i).Area, props(i).Centroid(1), props(i).Centroid(2))
end

% Visualize
figure;
subplot(1,3,1); imshow(surface);        title('Original Surface')
subplot(1,3,2); imshow(bw_def);         title('Detected Defects')
subplot(1,3,3); imshow(surface); hold on
for i = 1:length(props)
    bb = props(i).BoundingBox;
    rectangle('Position', bb, 'EdgeColor', 'r', 'LineWidth', 2)
end
hold off
title('Defects Highlighted')
