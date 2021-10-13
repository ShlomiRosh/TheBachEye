import cv2
import time
import os


class SuperResolution:

    def __init__(self, img, quality, debug=False):
        """
        initialize params for this class.
        :param: img: the image to improve
        :param: quality: in which quality the result pic should be
        """
        self.__org_image = img
        self.__super_image = None
        self.__quality = quality if quality in [0, 1, 2, 3] else 0
        self.__models = {1: 'FSRCNN_x3.pb', 2: 'ESPCN_x4.pb', 'MediumGPU': 'EDSR_x4.pb',
                         3: 'LapSRN_x8.pb'}
        self.__model_scale = {1: 3, 2: 4, 3: 8}
        self.__debug = debug
        self.__to_bicubic() if self.__quality == 0 else self.__to_super_resolution()

    def get_image(self):
        return self.__super_image

    def __to_bicubic(self):
        """
        a minor improvement to a picture, take a very sort time.
        :return: bicubic: a bicubic improvement image
        """
        start = time.time()
        bicubic = cv2.resize(self.__org_image, (self.__org_image.shape[1]*2, self.__org_image.shape[0]*2),
                             interpolation=cv2.INTER_CUBIC)
        end = time.time()
        if self.__debug:
            self.__show_interpolation_results(bicubic, end - start)
        self.__super_image = bicubic

    def __show_interpolation_results(self, interpolation_img, took_time):
        """
        show the img before and after the interpolation
        :param interpolation_img: the img after interpolation
        :param took_time: the time for the interpolation
        """
        print('Interpolation took {:.2f} seconds'.format(took_time))
        cv2.imshow("Original", self.__org_image)
        cv2.imshow("Interpolation", interpolation_img)
        cv2.imwrite('.\SavedImages\\interpolation_img.png', interpolation_img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        cv2.waitKey(0)

    def __to_super_resolution(self):
        """
        use the heavy tools to improve image by the expropriate models.
        :return: scaled_image: depend on what the quality that the user
        ask for
        """
        model = self.init_model()
        start = time.time()
        scaled_image = model.upsample(self.__org_image)
        # scaled_image = cv2.resize(scaled_image, (self.__org_image.shape[1], self.__org_image.shape[0]))
        end = time.time()
        if self.__debug:
            self.__show_interpolation_results(scaled_image, end - start)
        self.__super_image = scaled_image

    def init_model(self):
        """
        this func will init model by the asked quality
        """
        model_file = self.__models[self.__quality]
        model_name = model_file.split('_')[0].lower()
        scale = self.__model_scale[self.__quality]
        super_resolution = cv2.dnn_superres.DnnSuperResImpl_create()
        script_dir = os.path.dirname(__file__)
        super_resolution.readModel(os.path.join(script_dir, "Models/" + model_file))
        super_resolution.setModel(model_name, scale)
        return super_resolution


def for_tests_only():
    """
    A test func to this page only..
    """
    image = cv2.imread('.\SavedImages\\4.png')
    # SuperResolution(image, 0)
    SuperResolution(image, 2, True)


if __name__ == '__main__':
    for_tests_only()


