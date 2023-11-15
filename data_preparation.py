import torch
from IPython.display import Image
import os
import random
import shutil
from sklearn.model_selection import train_test_split
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

'''Получаем путь до директории, где запущена программа
   и список всех подкаталогов / файлов в ней'''
current_dir = os.getcwd()
folders = os.listdir(current_dir)
print(current_dir)
print(folders)


def pick_all_img_names() -> None:
    file_names = []
    for name in folders:
        if "TC_by_Classes_jpg" in name:
            file_names += os.listdir(current_dir + "/" + name)

    with open("data/TC-Satellite-DataSet-main/filenames_img.txt", "w") as file:
        for name in file_names:
            file.write(name + "\n")
    print("Успешно записано", len(file_names), "элементов")


def pick_all_txt_names() -> None:
    file_names = []
    for name in folders:
        if "TC_by_Classes_txt" in name:
            file_names += os.listdir(current_dir + "/" + name)

    with open("data/TC-Satellite-DataSet-main/filenames_txt.txt", "x") as file:
        for name in file_names:
            file.write(name + "\n")
    print("Успешно записано", len(file_names), "элементов")


def pick_data_from_files():
    with open("data/TC-Satellite-DataSet-main/filenames_img.txt") as img_file:
        images = img_file.readlines()
    with open("data/TC-Satellite-DataSet-main/filenames_txt.txt") as txt_file:
        annotations = txt_file.readlines()
    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size=0.2,
                                                                                    random_state=1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations,
                                                                                  test_size=0.5, random_state=1)

    return test_images, val_images, train_images, test_annotations, val_annotations, train_annotations


# Utility function to move images
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        for tries in ['TC_by_Classes_jpg_1', 'TC_by_Classes_jpg_2', 'TC_by_Classes_jpg_3', 'TC_by_Classes_jpg_4', 'TC_by_Classes_jpg_5', 'TC_by_Classes_txt_1', 'TC_by_Classes_txt_2']:
            try:
                shutil.move(tries + "/" + f[:-1], destination_folder)
            except Exception as e:
                print(f, e)


def know_more_about_data():
    datalist = []
    for ttv in ["train", "test", "val"]:
        for filename in os.listdir(current_dir + "/labels/" + ttv):
            with open("labels/" + ttv + "/" + filename, "r") as file:
                datalist.append(file.readline().split(", "))
    return datalist


def fix_class_2():
    flag = False
    for folder in ["train", "test", "val"]:
        ppath = current_dir + "/labels/" + folder
        for file in os.listdir(ppath):
            with open(ppath + "/" + file, 'r') as file_txt:
                a = file_txt.readline()
                if a.split(', ')[0] == '':
                    flag = True
            if flag:
                with open(ppath + "/" + file, 'w') as file_txt_wr:
                    file_txt_wr.write("Class_2, 1, 1, 1, 1")
                flag = False


def data_fix_yolo():
    for ttv in ["train", "test", "val"]:
        for filename in os.listdir(current_dir + "/labels/" + ttv):
            ppath = "labels/" + ttv + "/" + filename
            with open(ppath, "r") as file:
                lst = file.readline().replace("\n", "").replace(", ", " ").split(" ")
            lst[0] = lst[0][-1]
            with open(ppath, "w") as file:
                file.write(' '.join(lst))


def fix_names():
    for ttv in ["train", "test", "val"]:
        for filename in os.listdir(current_dir + "/images/" + ttv):
            ppath = "images/" + ttv + "/" + filename
            os.rename(ppath, ppath.replace('_pro', ''))



#pick_all_img_names()
#pick_all_txt_names()

# Move the splits into their folders
#test_images, val_images, train_images, test_annotations, val_annotations, train_annotations = pick_data_from_files()
#move_files_to_folder(train_images, 'images/train/')
#move_files_to_folder(val_images, 'images/val/')
#move_files_to_folder(test_images, 'images/test/')
#move_files_to_folder(train_annotations, 'labels/train/')
#move_files_to_folder(val_annotations, 'labels/val/')
#move_files_to_folder(test_annotations, 'labels/test/')

#fix_class_2()
#data_fix_yolo()

#data_list = know_more_about_data()
#classes = [i[0] for i in data_list]
#print(classes)
#for i in set(classes):
#    print(i + ":", classes.count(i))

#fix_names()


