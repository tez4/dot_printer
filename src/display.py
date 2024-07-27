import numpy as np
from PIL import Image


class ImageTransformer:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        # numpy array from image
        self.image_array = np.array(self.image)
        self.new_image = np.zeros((2 * self.image_array.shape[0], 2 * self.image_array.shape[1], 3), dtype=np.uint8)

    def transform_two_by_two(self, i, j):
        image_cutout = self.image_array[i:i + 2, j:j + 2]

        average_color = np.mean(image_cutout, axis=(0, 1))
        red_count = 0
        green_count = 0
        blue_count = 0

        for m in range(2):
            for n in range(2):
                # if average color of channel is less 32 + ((k + l) * 64) then assign 0 else 255
                channel_binary = np.where(average_color < 32 + ((2 * m + n) * 64), 0, 255)
                self.new_image[2 * i + 2 * m, 2 * j + 2 * n] = [channel_binary[0], 0, 0]
                self.new_image[2 * i + 2 * m, 2 * j + 2 * n + 1] = [0, channel_binary[1], 0]
                self.new_image[2 * i + 2 * m + 1, 2 * j + 2 * n] = [0, 0, channel_binary[2]]

                red_count += int(channel_binary[0] / 255)
                green_count += int(channel_binary[1] / 255)
                blue_count += int(channel_binary[2] / 255)

        created_color = np.array([red_count * 64, green_count * 64, blue_count * 64])

        for m in range(2):
            for n in range(2):
                real_color = image_cutout[m, n]
                created_with_black = (created_color * 3 + np.array([0, 0, 0])) / 4
                created_with_white = (created_color * 3 + np.array([255, 255, 255])) / 4

                black_diff_to_real = np.abs(np.mean(created_with_black - real_color))
                white_diff_to_real = np.abs(np.mean(created_with_white - real_color))

                if white_diff_to_real < black_diff_to_real:
                    self.new_image[2 * i + 2 * m + 1, 2 * j + 2 * n + 1] = [255, 255, 255]

    def transform_image(self):
        for i in range(0, self.image_array.shape[0], 2):
            for j in range(0, self.image_array.shape[1], 2):
                self.transform_two_by_two(i, j)

    def save_image(self):
        new_image = Image.fromarray(self.new_image)
        new_image.save("output/transformed_image_1.png")


def main():
    transformer = ImageTransformer("assets/test_image_06.jpg")
    transformer.transform_image()
    transformer.save_image()


if __name__ == "__main__":
    main()
