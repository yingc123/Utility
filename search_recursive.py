import os

def Temp():
    root_path = r"E:\data\mhd"
    #txt_read = r"Z:\ImageAnalysisData\1-CT\Cardiac test data\AlgorithmTestBaseline\list20210422all.txt"
    file_list = search_file_in_directory([root_path], _search_method=search_mhd)
    base_list = [os.path.basename(i.replace('/image.mhd', '')) for i in file_list]
    file_set = set(base_list)
    print(len(file_list))
    print(len(file_set))

def _file_method(abs_file_name):
    if os.path.isfile(abs_file_name):
        return True, abs_file_name
    else:
        return False, ''

def _dir_method(abs_file_name):
    if os.path.isdir(abs_file_name):
        return True, abs_file_name
    else:
        return False, ''

def _default_method(abs_file_name):
    return True, abs_file_name

def _search_directory(_root_path, _search_method):
    _path_list = []
    if not os.path.exists(_root_path):
        return _path_list
    _sub_dir_files = os.listdir(_root_path)
    for _file_name in _sub_dir_files:
        _abs_file_name = _root_path + '/' + _file_name
        _is_searched, _search_file = _search_method(_abs_file_name)
        if _is_searched:
            _path_list.append(_search_file)
    return _path_list

def _search_directory_recursive(_root_path, _all_path_list, _search_method):
    if _root_path.endswith('.lnk'):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(_root_path)
        _root_path = shortcut.Targetpath
    # print('search directory recursive path: ' + _root_path)
    _is_searched, _search_file = _search_method(_root_path)
    if _is_searched:
        _all_path_list.append(_search_file)
    # ���ж��Ƿ���Ŀ¼
    if os.path.isdir(_root_path):
        _path_list = _search_directory(_root_path, _default_method)
        _path_list = _search_directory(_root_path, _default_method)
        for _sub_path in _path_list:
            if not _search_directory_recursive(_sub_path, _all_path_list, _search_method):
                ValueError(_sub_path + ' search failed.')
    return True

def _save_file_list(_file_name, _path_list):
    fp = open(_file_name, 'w')
    for index in range(len(_path_list)):
        fp.write(_path_list[index] + "\n")
    fp.close()

def search_file_in_directory(_root_paths, _file_name = None, _recursive = True, _search_method = _default_method):
    all_path_list = []
    if _recursive:
        for search_root in _root_paths:
            print('search directory recursive path: ' + search_root)
            path_list = []
            _search_directory_recursive(search_root, path_list, _search_method)
            all_path_list.extend(sorted(path_list))
    else:
        for search_root in _root_paths:
            print('search directory path: ' + search_root)
            all_path_list.extend(sorted(_search_directory(search_root, _search_method)))

    if _file_name is not None:
        _save_file_list(_file_name, all_path_list)
        print("Save search result from " + _root_paths  + " to " + _file_name)

    return all_path_list

def search_image(abs_file_name):
    if -1 != abs_file_name.find('image.mhd') and -1 == abs_file_name.find('mask.mhd'):
        return True, abs_file_name
    else:
        return False, ''

def search_dcm(abs_file_name):
    if -1 != abs_file_name.find('.dcm'):
        return True, abs_file_name
    else:
        return False, ''

def search_mhd(abs_file_name):
    if -1 != abs_file_name.find('.mhd'):
        return True, abs_file_name
    else:
        return False, ''

def search_txt(abs_file_name):
    if -1 != abs_file_name.find('.txt'):
        return True, abs_file_name
    else:
        return False, ''

def search_DSA(abs_file_name):
    if -1 != abs_file_name.find('image_Post.mhd') and -1 != abs_file_name.find('image_Post.mhd'):
        return True, abs_file_name
    else:
        return False, ''

def search_dcm_dir(abs_file_name):
    list = ['IM', 'I', '.dcm', 'DICOM']
    if -1 != abs_file_name.find('I') or -1 != abs_file_name.find('.dcm') or -1 != abs_file_name.find('DICOM'):
        return True, os.path.dirname(abs_file_name)
    else:
        return False, ''

def search_dcm_file(abs_file_name):
    if -1 != abs_file_name.find('.dcm') or -1 != abs_file_name.find('IM'):
        return True, abs_file_name
    else:
        return False, ''

def search_mcs(abs_file_name):
    if -1 != abs_file_name.find('.mcs'):
        return True, abs_file_name
    else:
        return False, ''

def search_nii(abs_file_name):
    if -1 != abs_file_name.find('.nii'):
        return True, abs_file_name
    else:
        return False, ''

def search_mask(abs_file_name):
    if -1 != abs_file_name.find('.mhd') and -1 != abs_file_name.find('mask'):
        return True, abs_file_name
    else:
        return False, ''

def search_Mask_MLabel(abs_file_name):
    if -1 != abs_file_name.find('Mask_MLabel.mhd'):
        return True, abs_file_name
    else:
        return False, ''

def SearchFile(path, fileFormat):
    files=os.listdir(path)
    findfileName={}
    for f in files:
        filepath= os.path.join(path,f)
        if os.path.isfile(filepath):
            fileName=os.path.split(f)[1]
            ext = fileName.split(".",1)[1].lower()
            if (ext==fileFormat) &(("mask" not in fileName)):
                findfileName[fileName.split(".",1)[0]]=filepath
        else:
            findfileName.update(SearchFile(filepath,fileFormat))
    return findfileName
