from robust_awb import AWBManager
from skimage import io
from scipy import misc

if __name__ == '__main__':
    manager = AWBManager()
    image = io.imread('./assets/test_image2.jpg')
    float_image = image / 255.
    float_image -= 0.5
    float_image *= 2
    print('image array : {}'.format(float_image))
    processed_image = manager.process_awb(float_image)
    # processed_image = float_image
    # print(processed_image)
    # io.imsave('./assets/processed_test_image2.jpg', processed_image)
    misc.imsave('./assets/processed_test_image2.jpg', processed_image)
