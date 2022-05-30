import os
from os.path import join
import time
#import win32com.client

import copy
import shutil
import tempfile
import gzip
import json
import re

import numpy as np
import random
import SimpleITK as sitk
from skimage.filters import gaussian

from medical_format import read_mhd_attr
from picture import draw_single
from medical_format import read_raw, string_to_pixelType
from anonymization import Anonymization

if __name__ == '__main__':

    # root=r"F:\VesselDatabaseAnnotation\head_neck\000mcs_spacing=111"
    # subDirList=os.listdir(root)
    # num_subDir=len(subDirList)
    #
    # done=0
    # for subDir in subDirList:
    #     if oldmcsconvertor(os.path.join(root,subDir)):
    #         done=done+1
    # print("sum project:%d,done %d" %(num_subDir,done))

    # ########点定位导出点
    #
    # root_path = [r'G:\head_neck_vessel3\data\test']
    #
    # file_list = search_file_in_directory(root_path, _search_method=search_mcs)
    # # print(file_list)
    # for mcs_name in file_list:
    #     dirname = os.path.dirname(mcs_name)
    #     # dirname = dirname.replace(root_path[0], r'E:/PulmonaryArteryVeinSegmentation_Anonymization_mcs') + '/' + os.path.basename(raw_name).replace('_mask.mhd', '')
    #     # dirname = dirname.replace(root_path[0], r'E:/CatheterData_mcs')
    #     print(mcs_name)
    #     # if not os.path.exists(dirname):
    #         # os.makedirs(dirname)
    #     exportpoint(mcs_name)
    #     # break

    # root_path = [r'G:\Ventricles_aorta\TAVR\data\Pathological_data\QPM_new\5']
    #
    # file_list = search_file_in_directory(root_path, _search_method=search_mcs)
    #
    #
    # for mcs_name in file_list:
    #     dirname = os.path.dirname(mcs_name)
    #
    #     print(mcs_name)
    #     importmask(mcs_name, dirname+'/mask.mhd')

    ###读mhd 相关信息
    # a = np.ones((20, 30, 40), "int")
    # write_mhd("d:/a/b.mhd", a)
    # a
    # a = read_mhd("d:/a/b.mhd")
    # print(read_mhd_attr("d:/a/b.mhd", "BinaryData", "bool"))
    # print(read_mhd_attr("d:/a/b.mhd", "NDims", "int"))
    # print(read_mhd_attr("d:/a/b.mhd", "ElementSpacing", "float"))

    ####raw to mhd
    # path = r'\\dataserver03\hsw\ImageAnalysisData\1-CT\Cardiac test data\raw data'
    # path_out = r'E:\\'
    # # Read the image using both big and little endian
    # for file in os.listdir(path):
    #     if file.endswith('.raw'):
    #         #f = open(os.path.join(path.replace('20171020之前的数据', '20171020'), file.replace('.raw', '.info')))
    #         f = open(r'G:\UnitTest\Tavi_filter\rawdata\x.info', 'r')
    #         info = f.read().splitlines()
    #         size = info[:3]
    #         spacing = info[3:]
    #         image = read_raw(binary_file_name=os.path.join(path, file),
    #                          image_size=size,
    #                          sitk_pixel_type=string_to_pixelType['sitkInt16'],
    #                          image_spacing=spacing)
    #
    #         sitk.WriteImage(image, os.path.join(path_out, file.replace('.raw', '.mhd')))

    ######Dicom 批量匿名
    # dcm_path = [r"F:\Chest_Abdomen_dcm"]
    # dcm_list = search_file_in_directory(dcm_path, _search_method=search_dcm)
    # dcm_list = [os.path.dirname(i) for i in dcm_list]
    # dcm_set = set(dcm_list)
    # print(len(dcm_set))
    # dcm_list = list(dcm_set)
    # dicom_anonymization(dcm_list)

    ####点定位相关， 写点， 写config
    # root_path = r'G:\head_neck_vessel3\data\source_205'
    # for dir in os.listdir(root_path):
    #     # # list.append(os.path.join(root_path,dir,'image.mhd'))
    #     # name = os.path.join(root_path,dir,'location_points.json')
    #     # #读点name = os.path.join(root_path,dir,'location_points')
    #     # with open(name, "r", encoding="utf-8") as f:
    #     #     jsontmp = json.load(f)
    #     # new_name = os.path.join(root_path, dir, dir+'_centerline_keypoints.json')
    #     # # 写点到json
    #     # #location_points_path = os.path.join(project_dir, "location_points.json")
    #     # with open(new_name, "w", encoding="utf-8") as f_new:
    #     #     json.dump(jsontmp, f_new, ensure_ascii=False)
    #     remove_file(os.path.join(root_path, dir, 'location_points.json'))
    #     im = sitk.ReadImage(name)
    #     sitk.WriteImage(im, os.path.join(root_path,dir,dir+'.mhd'), False)
    #     remove_file(name)
    #     remove_file(name.replace('.mhd', '.raw'))
    # write_config()
    # new_config()
    # remove_files()

    #######mhd 批量匿名

    # read_path = r'\\dataserver03\hsw\ImageAnalysisData\1-CT\vessel application\TrainStandard\PulmonaryVessel'
    # txt = '03_Testing'
    # write_path = r'\\dataserver03\Userdata\ying.chen02'
    # f_write = open(os.path.join(write_path, txt+'.txt'), 'w')
    # f_read = open(os.path.join(read_path, txt+'.txt'), 'r')
    # name_list = f_read.readlines()
    # f_read.close()
    # ano = Anonymization()
    # for name in name_list:
    #     ciphertext = name.replace((txt+'/'), '').replace('.mhd\n', '')
    #     plaintext = ano.decrypt(ciphertext)
    #     f_write.write(ciphertext + ',' + plaintext + '\n')
    # f_write.close()

    ano = Anonymization()
    ciphertext = r'R09ORyBIVUkgWkhFTl8yLjAgeCAyLjBfNTAxXzIwMjAwMzEwXzIuMCB4IDIuMA&3d&3d'
    plaintext = ano.decrypt(ciphertext)
    print(plaintext)
