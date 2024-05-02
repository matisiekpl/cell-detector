import cv2
import matplotlib.pyplot as plt

I1 = cv2.imread('cells/Im060_1/cell_0.png')
I2 = cv2.imread('cells/Im060_1/cell_1.png')
I3 = cv2.imread('cells/Im060_1/cell_7.png')

fig, ax = plt.subplots(1, 3)
ax[0].imshow(I1)
ax[0].axis('off')
ax[1].imshow(I2)
ax[1].axis('off')
ax[2].imshow(I3)
ax[2].axis('off')

plt.savefig('cells.png', bbox_inches='tight', transparent="True", pad_inches=0)
