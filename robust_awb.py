from skimage import color as skcolor
import numpy as np


class AWBManager(object):
    def __init__(self):
        self.threshold = 0.097
        self.u = 0.02
        self.a = 0.1
        self.b = 0.0005
        self.max_steps = 2000

    @staticmethod
    def sign(value):
        if value > 0:
            return 1
        else:
            return -1

    def process_awb(self, rgb_array):
        height = rgb_array.shape[0]
        width = rgb_array.shape[1]
        for step in range(self.max_steps):
            yuv_array = skcolor.rgb2yuv(rgb_array)
            print("yuv array shape : {}".format(yuv_array.shape))
            F = (np.abs(yuv_array[..., 1]) + np.abs(yuv_array[..., 2])) / np.abs(yuv_array[..., 0])
            grays = (F < self.threshold)

            grays = yuv_array[grays]
            print("grays shape : {}".format(grays.shape))
            flattened_grays = np.reshape(grays, (-1, 3))
            mean_values = np.mean(flattened_grays, 0)
            u_bar = mean_values[1]
            v_bar = mean_values[2]
            color_filter = np.eye(3, dtype=np.float32)

            if np.abs(u_bar) > np.abs(v_bar):
                err = u_bar
                ch = 2  # blue channel
            else:
                err = v_bar
                ch = 0  # red channel

            if abs(err) >= self.a:
                delta = 2 * self.sign(err) * self.u
            elif abs(err) < self.b:
                print("Converged in step {}".format(step))
                print("{} / {}".format(u_bar, v_bar))
                break
            else:
                delta = self.sign(err) * self.u

            color_filter[ch][ch] -= delta
            # print(color_filter)
            if step % 10 == 0:
                print("{}".format(abs(err)))
            rgb_array = np.matmul(np.reshape(rgb_array, (-1, 3)), color_filter)
            rgb_array = np.reshape(rgb_array, (height, width, 3))
        rgb_array = np.clip(rgb_array, -1, 1)
        return rgb_array

    def bulk_process_awb(self, rgb_arrays):
        pass
