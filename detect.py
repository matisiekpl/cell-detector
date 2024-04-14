import cv2
import matplotlib.pyplot as plt
import os

if not os.path.exists('cells'):
    os.makedirs('cells')


def extract_cells(filename):
    print(f'analyzing {filename}')

    # Preprocess image
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_contours = img.copy()
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

    # Find centroids
    centroids = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            try:
                if thresh[cY-10, cX-10] > 0 and thresh[cY+10, cX+10] > 0 and thresh[cY-10, cX+10] > 0 and thresh[cY+10, cX-10] > 0:
                    centroids.append((cX, cY))
                    cv2.circle(img_contours, (cX, cY), 10, (255, 0, 0), -1)
                    print(f'found cell at ({cX}, {cY})')
            except Exception as e:
                continue
    plt.imsave(f'{filename.replace(".jpg","")}_contours.png', img_contours)

    # Extract squares
    if not os.path.exists(f'cells/{filename.replace(".jpg","")}'):
        os.makedirs(f'cells/{filename.replace(".jpg","")}')

    size = 120
    for i, (cX, cY) in enumerate(centroids):
        if cX-size < 0 or cX+size > img.shape[1] or cY-size < 0 or cY+size > img.shape[0]:
            print(f'cell {i} is too close to the border')
            continue
        # Crop square
        square = img[cY-size:cY+size, cX-size:cX+size]
        plt.imsave(
            f'cells/{filename.replace(".jpg", "")}/cell_{i}.png', square)


extract_cells('Im060_1.jpg')
