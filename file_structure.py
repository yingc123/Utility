import os
import shutil
from search_recursive import search_file_in_directory, search_dcm

def search_walk(root, file_extension):
    """
    Parameters
    ----------
    root: search all files in the root
    file_extension: files are restricted with specific extension

    Returns: sorted list of all files with extension in root
    dicom will return its dir
    -------
    """
    print('search directory recursive path: ', + root)
    all_path_list = []
    ##if dcm, return its dir
    if file_extension == '.dcm':
        for root, dirs, files in os.walk(root):
            num = 0
            for file in files:
                if file.endswith('.dcm'):
                    num += 1
            if num > 100:
                all_path_list.append(root)
                #print(num)
    ## otherwise return files
    else:
        for root, dirs, files in os.walk(root):
            for file in files:
                if file.endswith(file_extension):
                    all_path_list.append(os.path.join(root, file))

    print('find {} {} files'.format(len(all_path_list), file_extension))
    return all_path_list

def remove_file(_src_file):
    if not os.path.exists(_src_file):
        return
    os.remove(_src_file)
    print("remove %s"%( _src_file))

def remove_image(_src_file):
    if _src_file.endswith(".mhd"):
        remove_file(_src_file)
        remove_file(_src_file.replace('.mhd', '.raw'))
        remove_file(_src_file.replace('.mhd', '.zraw'))
        remove_file(_src_file.replace('.mhd', '.dat'))
    elif _src_file.endswith(".nii.gz"):
        remove_file(_src_file)
    else:
        print('Unknown file type!!!')

def move_file(_src_file, _dst_file):
    if not os.path.exists(_src_file):
        return
    if not os.path.isfile(_src_file):
        shutil.move(_src_file, _dst_file)               # 移动文件夹
    else:
        dirname = os.path.dirname(_dst_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)                        # 创建路径
        while True:
            try:
                shutil.move(_src_file, _dst_file)               # 移动文件
                break
            except:
                pass
    print("move %s -> %s"%( _src_file, _dst_file))

def move_image(_src_file, _dst_file):
    # print("move %s -> %s"%( _src_file, _dst_file))
    if _src_file.endswith(".mhd"):
        move_file(_src_file, _dst_file)
        move_file(_src_file.replace('.mhd', '.raw'), _dst_file.replace('.mhd', '.raw'))
        move_file(_src_file.replace('.mhd', '.zraw'), _dst_file.replace('.mhd', '.zraw'))
        move_file(_src_file.replace('.mhd', '.dat'), _dst_file.replace('.mhd', '.dat'))
    elif _src_file.endswith(".nii.gz"):
        move_file(_src_file, _dst_file)
    else:
        print('Unknown file type!!!')



def copy_file_all(_src_file, _dst_file):
    if not os.path.exists(_src_file):
        return
    if os.path.exists(_dst_file):
        return
    if not os.path.isfile(_src_file):
        shutil.copytree(_src_file, _dst_file)  #复制文件夹
    else:
        dirname = os.path.dirname(_dst_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)                        # 创建路径
        while True:
            try:
                shutil.copyfile(_src_file, _dst_file)           # 复制文件
                break
            except:
                pass

def copy_file(_src_file, _dst_file):
    if not os.path.exists(_src_file):
        return
    if os.path.exists(_dst_file):
        return
    if not os.path.isfile(_src_file):
        print(_src_file + " not exist!")
    else:
        dirname = os.path.dirname(_dst_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)                        # 创建路径
        while True:
            try:
                shutil.copyfile(_src_file, _dst_file)           # 复制文件
                break
            except:
                pass
        # print("copy %s -> %s"%( _src_file, _dst_file))

def copy_image(_src_file, _dst_file):
    # print("copy %s -> %s"%( _src_file, _dst_file))
    if _src_file.endswith(".mhd"):
        copy_file(_src_file, _dst_file)
        copy_file(_src_file.replace('.mhd', '.raw'), _dst_file.replace('.mhd', '.raw'))
        copy_file(_src_file.replace('.mhd', '.zraw'), _dst_file.replace('.mhd', '.zraw'))
        copy_file(_src_file.replace('.mhd', '.dat'), _dst_file.replace('.mhd', '.dat'))
    elif _src_file.endswith(".nii.gz"):
        copy_file(_src_file, _dst_file)
    else:
        print('Unknown file type!!!')


def robocopy_file(src_dir, dst_dir, file_name):
    '''
    如果路径带space做不了
    :param src_dir:
    :param dst_dir:
    :param file_name:
    :return:
    '''
    command = 'robocopy {} {} {} /copyall'.format(src_dir, dst_dir, file_name)
    os.system(command)

def robocopy_dcm(src, dst):
    root = [src]
    file_list = search_file_in_directory(root, _search_method=search_dcm)
    for file in file_list:
        src_dir = os.path.dirname(file)
        dst_dir = src_dir.replace(src, dst)
        robocopy_file(src_dir, dst_dir, os.path.basename(file))