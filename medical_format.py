import os
import time
import tempfile
import re
import copy
import numpy as np
import SimpleITK as sitk
from file_structure import remove_file

string_to_pixelType = {"sitkUInt8": sitk.sitkUInt8,
                       "sitkInt8": sitk.sitkInt8,
                       "sitkUInt16": sitk.sitkUInt16,
                       "sitkInt16": sitk.sitkInt16,
                       "sitkUInt32": sitk.sitkUInt32,
                       "sitkInt32": sitk.sitkInt32,
                       "sitkUInt64": sitk.sitkUInt64,
                       "sitkInt64": sitk.sitkInt64,
                       "sitkFloat32": sitk.sitkFloat32,
                       "sitkFloat64": sitk.sitkFloat64}

def read_mhd(mhd_path: str, out_type=None):
    """
    读取mhd/nii文件
    :param mhd_path: 文件路径
    :param out_type: 转换数据类型 None为默认类型
    :return: tuple(array_image, spacing, origin) or None
    !!读取进来的数据array_image遵循C的数据排布规则，三个维度为zyx
    !!spacing 和 origin是列表 对应的顺序为xyz
    !!使用时一定注意！！
    """

    # if not os.path.exists(os.path.abspath(mhd_path)):
    #     print("read mhd file err! path is :{}".format(mhd_path))
    #     return None
    assert os.path.exists(os.path.abspath(mhd_path))

    sitk_image = sitk.ReadImage(mhd_path)
    array_image = sitk.GetArrayFromImage(sitk_image)
    if out_type is not None:
        array_image = array_image.astype(out_type)
    spacing = sitk_image.GetSpacing()
    origin = sitk_image.GetOrigin()
    return array_image, spacing, origin

def write_mhd(mhd_path: str,
              array_image: np.ndarray,
              spacing=(1.0, 1.0, 1.0),
              origin=(0.0, 0.0, 0.0),
              out_type=None,
              compression: bool = False):
    """
    写一个数据为mhd，如果路径不存在则创建
    :param mhd_path:写的 路径+文件名
    :param array_image:图像矩阵，也确定了数据类型
    :param spacing:spacing
    :param origin:origin
    :param out_type: 转换数据类型 None为输入数据的类型
    :param compression: 是否压缩数据
    :return:
    !!写入的时候array_image遵循C的数据排布规则，三个维度为zyx
    !!spacing 和 origin是列表 对应的顺序为xyz
    !!使用时一定注意！！
    """

    if out_type is not None:
        array_image = array_image.astype(out_type)

    sitk_image = sitk.GetImageFromArray(array_image)
    sitk_image.SetSpacing([float(x) for x in spacing])
    sitk_image.SetOrigin([float(x) for x in origin])

    root, name = os.path.split(mhd_path)
    if not os.path.exists(root):
        os.makedirs(root)

    # 其他的都默认就行
    sitk.WriteImage(sitk_image, mhd_path, useCompression=compression)

def mhd_uncompression(file_list, image = True):
    if image:
        for name in file_list:
            print(format(name))
            im = sitk.ReadImage(name)
            sitk.WriteImage(im, name, False)
            remove_file(name.replace('.mhd', '.zraw'))
    else:
        for name in file_list:
            print(format(name))
            name = name.replace('image.mhd','mask.mhd')
            im = sitk.ReadImage(name)
            sitk.WriteImage(im, name, False)
            remove_file(name.replace('.mhd', '.zraw'))

def mhd_compression(file_list, image = True):
    if image:
        for name in file_list:
            print(format(name))

            im = sitk.ReadImage(name)
            sitk.WriteImage(im, name, True)
            remove_file(name.replace('.mhd', '.raw'))
    else:
        for name in file_list:
            print(format(os.path.dirname(name)+ '/mask.mhd'))
            name = name.replace('image.mhd','mask.mhd')
            im = sitk.ReadImage(name)
            sitk.WriteImage(im, name, True)
            remove_file(name.replace('.mhd', '.raw'))

def read_mhd_attr(mhd_path: str, key: str, dtype: str):
    """
        给定一个mhd文件的路径 提取出key对应的内容
        :param mhd_path: 文件路径
        :param key: key 固定的一些key
        :param dtype: 说明这个key是什么类型的数据，方便进行转换 如"str" "int" "float"
        :return: str or array or None
        """
    assert os.path.exists(mhd_path)

    with open(mhd_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # 正则表达式匹配到目标 并 得到对应的元素
    regex = re.compile(r"^\s*" + key + r"\s*=\s*(.*)\s*$")
    attr = None
    for a_line in lines:
        match_obj = re.match(regex, a_line)
        if match_obj is not None:
            attr = match_obj.group(1)
            break

    # 说明没找到对应的项 返回了
    if attr is None:
        return None

    attr = attr.strip()

    if dtype == "str":
        return attr
    elif dtype == "bool":
        assert attr == "True" or attr == "False"
        return attr == "True"
    else:
        return np.array(attr.split(), dtype)

def mhd_norm(file_list):
    '''
    change the name of all image files to be image.mhd
    the origin name is saved as the directory name
    :param file_list: list of files
    :return: None
    '''
    for name in file_list:
        if name.endswith('/image.mhd'):
            continue
        print(format(name))
        im = sitk.ReadImage(name)
        save_path = os.path.dirname(name) + "/" + os.path.basename(name)[:-4]
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        sitk.WriteImage(im, save_path + '/image.mhd', False)

def mhd_rename(file_list, image = True):
    '''
    rename the name of all image/mask files to be image.mhd
    the origin name is deleted
    :param file_list: list of files
    :param image: image or mask?
    :return: None
    '''
    if image:
        for name in file_list:
            if name.endswith('*.mhd'):
                continue
            print(format(name))
            im = sitk.ReadImage(name)
            sitk.WriteImage(im, os.path.dirname(name) + '\image.mhd', False)
            remove_file(name.replace('.mhd', '.raw'))
    else:
        for name in file_list:
            if name.endswith('image.mhd'):
                continue
            print(format(name))
            im = sitk.ReadImage(name)
            sitk.WriteImage(im, os.path.dirname(name) + '\gold.mhd', False)
            #remove_file(name.replace('mask.mhd', '.zraw'))


def read_raw(binary_file_name, image_size, sitk_pixel_type, image_spacing=None,
             image_origin=None, big_endian=False):
    """
    Read a raw binary scalar image.

    Parameters
    ----------
    binary_file_name (str): Raw, binary image file content.
    image_size (tuple like): Size of image (e.g. [2048,2048])
    sitk_pixel_type (SimpleITK pixel type: Pixel type of data (e.g.
        sitk.sitkUInt16).
    image_spacing (tuple like): Optional image spacing, if none given assumed
        to be [1]*dim.
    image_origin (tuple like): Optional image origin, if none given assumed to
        be [0]*dim.
    big_endian (bool): Optional byte order indicator, if True big endian, else
        little endian.

    Returns
    -------
    SimpleITK image or None if fails.
    """

    pixel_dict = {sitk.sitkUInt8: 'MET_UCHAR',
                  sitk.sitkInt8: 'MET_CHAR',
                  sitk.sitkUInt16: 'MET_USHORT',
                  sitk.sitkInt16: 'MET_SHORT',
                  sitk.sitkUInt32: 'MET_UINT',
                  sitk.sitkInt32: 'MET_INT',
                  sitk.sitkUInt64: 'MET_ULONG_LONG',
                  sitk.sitkInt64: 'MET_LONG_LONG',
                  sitk.sitkFloat32: 'MET_FLOAT',
                  sitk.sitkFloat64: 'MET_DOUBLE'}
    direction_cosine = ['1 0 0 1', '1 0 0 0 1 0 0 0 1',
                        '1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1']
    dim = len(image_size)
    header = ['ObjectType = Image\n'.encode(),
              ('NDims = 3\n').encode(),
              ('DimSize = ' + ' '.join([str(v) for v in image_size]) + '\n')
              .encode(),
              ('ElementSpacing = ' + (' '.join([str(v) for v in image_spacing])
                                      if image_spacing else ' '.join(
                  ['1'] * dim)) + '\n').encode(),
              ('Offset = ' + (
                  ' '.join([str(v) for v in image_origin]) if image_origin
                  else ' '.join(['0'] * dim) + '\n')).encode(),
              ('TransformMatrix = ' + direction_cosine[dim - 2] + '\n')
              .encode(),
              ('ElementType = ' + pixel_dict[sitk_pixel_type] + '\n').encode(),
              'BinaryData = True\n'.encode(),
              ('BinaryDataByteOrderMSB = ' + str(big_endian) + '\n').encode(),
              # ElementDataFile must be the last entry in the header
              ('ElementDataFile = ' + os.path.abspath(
                  binary_file_name) + '\n').encode()]
    fp = tempfile.NamedTemporaryFile(suffix='.mhd', delete=False)

    print(header)

    # Not using the tempfile with a context manager and auto-delete
    # because on windows we can't open the file a second time for ReadImage.
    fp.writelines(header)
    fp.close()
    img = sitk.ReadImage(fp.name)
    os.remove(fp.name)
    return img


def mhd2dicom(input, outDir):
    image = sitk.ReadImage(input)

    writer = sitk.ImageFileWriter()
    writer.KeepOriginalImageUIDOn()
    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")

    # Copy some of the tags and add the relevant tags indicating the change.
    # For the series instance UID (0020|000e), each of the components is a number, cannot start
    # with zero, and separated by a '.' We create a unique series ID using the date and time.
    # tags of interest:
    direction = image.GetDirection()
    series_tag_values = [("0008|0031", modification_time),  # Series Time
                         ("0008|0021", modification_date),  # Series Date
                         ("0008|0008", "DERIVED\\SECONDARY"),  # Image Type
                         ("0020|000e", "1.2.826.0.1.3680043.2.1125." + modification_date + ".1" + modification_time),
                         # Series Instance UID
                         ("0020|0037",
                          '\\'.join(map(str, (direction[0], direction[3], direction[6],  # Image Orientation (Patient)
                                              direction[1], direction[4], direction[7])))),
                         ("0008|103e", "Created-SimpleITK"),  # Series Description
                         ("0020|000D", "1.2.826.0.1.3680043.2.1125." + modification_date),  # Study Instance UID
                         ("0028|1052", "-1024"),  # Rescale Intercept
                         ("0028|1053", "1"),  # Rescale Slope
                         # ("0028|1054","US")#, #Rescale Type
                         # ("0028|0103","0") #Pixel Representation
                         ]

    for i in range(image.GetDepth()):
        image_slice = image[:, :, i]
        # Tags shared by the series.
        for tag, value in series_tag_values:
            image_slice.SetMetaData(tag, value)
        # Slice specific tags.
        image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d"))  # Instance Creation Date
        image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S"))  # Instance Creation Time
        # Setting the type to CT preserves the slice location.
        image_slice.SetMetaData("0008|0060", "CT")  # set the type to CT so the thickness is carried over

        # (0020, 0032) image position patient determines the 3D spacing between slices.
        image_slice.SetMetaData("0020|0032", '\\'.join(
            map(str, image.TransformIndexToPhysicalPoint((0, 0, i)))))  # Image Position (Patient)
        image_slice.SetMetaData("0020,0013", str(i))  # Instance Number

        # Write to the output directory and add the extension dcm, to force writing in DICOM format.
        writer.SetFileName(os.path.join(outDir, str(i) + '.dcm'))
        writer.Execute(image_slice)

def dcm2raw(dcm_files, raw_name):
    """
    Parameters
    ----------
    dcm_files: dcm dir
    raw_name: mhd name

    Returns None
    -------
    """
    reader = sitk.ImageSeriesReader()
    img_names = reader.GetGDCMSeriesFileNames(dcm_files)
    reader.SetFileNames(img_names)
    image = reader.Execute()

    dirname = os.path.dirname(raw_name)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    image = sitk.Cast(image, sitk.sitkInt16)
    sitk.WriteImage(image, raw_name, False)


def read_dicom_series(dicom_dir: str):
    """
    读取一个dicom序列，得到图像基本信息
    :param dicom_dir:文件夹路径
    :return:array_image, spacing, origin
    !!读取进来的数据array_image遵循C的数据排布规则，三个维度为zyx
    !!spacing 和 origin是列表 对应的顺序为xyz
    !!使用时一定注意！！
    """
    if not os.path.exists(os.path.abspath(dicom_dir)):
        print("read dicom series err! dir is :{}".format(dicom_dir))
        return None

    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)
    sitk_image = reader.Execute()

    array_image = sitk.GetArrayFromImage(sitk_image)
    spacing = sitk_image.GetSpacing()
    origin = sitk_image.GetOrigin()

    return array_image, spacing, origin

def read_dicom_file(file_path: str):
    """
    读取以一个文件形式保存的图像（可能是一个slice也可能是一个视频序列）
    得到基本信息
    :param file_path:path
    :return: array_image, spacing, origin
    !!读取进来的数据array_image遵循C的数据排布规则，三个维度为zyx
    !!spacing 和 origin是列表 对应的顺序为xyz
    !!使用时一定注意！！
    """

    if not os.path.exists(os.path.abspath(file_path)):
        print("read dicom file err! path is :{}".format(file_path))
        return None

    res = sitk.ReadImage(file_path)
    array_image = sitk.GetArrayFromImage(res)
    spacing = res.GetSpacing()
    origin = res.GetOrigin()

    return array_image, spacing, origin

def remove_chinese(strs):
    c_list = []
    res = copy.deepcopy(strs)
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            c_list.append(_char)
    for i in c_list:
        res = res.replace(i, '')
    return res
