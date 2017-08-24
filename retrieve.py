import cv2
import urllib.request
import numpy as np
import os

def store_raw_images():
    # Get the image from the URL
    neg_image_link = "http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02782778"
    neg_image_urls = urllib.request.urlopen(neg_image_link).read().decode()

    # Create a new directory for negative picture
    if not os.path.exists('neg'):
        os.makedirs('neg')

    # Number of the picture
    pic_num = 1

    # Read in the picture, resize it and then save it to the new folder
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, 'neg/'+str(pic_num)+'.jpg')
            img = cv2.imread('neg/'+str(pic_num)+'.jpg')
            cv2.imwrite('neg/'+str(pic_num)+'.jpg',img)
            pic_num += 1
        except Exception as e:
            print(str(e))
store_raw_images()

# def find_uglies():
#     for file_type in ['neg']:
#         for img in os.listdir(file_type):
#             for ugly in os.listdir('uglies'):
#                 try:
#                     current_image_path = str(file_type) + '/' + str(img)
#                     ugly = cv2.imread('uglies/'+str(ugly))
#                     question = cv2.imread(current_image_path)
#
#                     if ugly.shape == question.shape and not (np.bitwise_xor(ugly,question).any()):
#                         print("Ugly pic")
#                         print(current_image_path)
#                         os.remove(current_image_path)
#                 except Exception as e:
#                     print(str(e))
#
# def create_pos_n_neg():
#     for file_type in ['neg']:
#         for img in os.listdir(file_type):
#             if file_type == 'neg':
#                 line = file_type + '/' + img + '\n'
#                 with open('bg.txt','a') as f:
#                     f.write(line)
# create_pos_n_neg()
