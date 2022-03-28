import cv2
from imgaug import augmenters as iaa

img_path = "/home/daton/PycharmProjects/pythonProject/ByteTrack/datasets/crowdhuman/CrowdHuman_val/273271,2b3eb0002dbca786.jpg"
img = cv2.imread(img_path)

resize = (640, 360)
img = cv2.resize(img, dsize=resize)

# 모션각도, 블러강도 필요
motion_blur = iaa.MotionBlur()
# img = motion_blur(image=img)

muladd = iaa.MultiplyAndAddToBrightness(mul=(0.9, 1.1), add=(-15, 15))

snow = iaa.imgcorruptlike.Snow(severity=(1, 4))
#snow = iaa.Snowflakes()

fog = iaa.Fog()

weather = iaa.OneOf([
            iaa.Snowflakes(),
            iaa.Clouds()
        ])

gray = iaa.Grayscale()
noise = iaa.AdditiveGaussianNoise(scale=(0, 20))

for _ in range(10):
    tmp = snow(image=img)

    print(tmp.shape)
    cv2.imshow("img", tmp)
    cv2.waitKey(0)