import os
import numpy as np
import SimpleITK as sitk
import shutil
import json
from search_recursive import SearchFile
from medical_format import mhd2dicom


def oldmcsconvertor(projectDir):
    print("start:%s" % projectDir)

    mhdfileDict = SearchFile(projectDir, "mhd")
    if len(mhdfileDict) != 1:
        print("%s has %d mhd file" % (projectDir, len(mhdfileDict)))
        return False

    mhd_name, mhd_path = list(mhdfileDict.items())[0]

    mcsfileDict = SearchFile(projectDir, "mcs")
    if len(mcsfileDict) != 1:
        print("%s has %d mcs file" % (projectDir, len(mcsfileDict)))
        return False

    _, old_mcs_path = list(mcsfileDict.items())[0]

    Dir = os.path.dirname(mhd_path)
    name = os.path.basename(Dir)
    if mhd_name != name:
        print("not find %d.mhd" % name)

    project_path = os.path.join(Dir, name + ".mcs")
    createMcsProject_mhd(mhd_path, project_path)

    #
    mask_names = ["skull__wj", "cervical_vertebra__wj", "carotid_artery__wj", "vertebral_artery__wj"]

    mimics.file.open_project(old_mcs_path)
    mask_list = []
    for i, mask_name in enumerate(mask_names):
        mask = mimics.data.masks.find(mask_name)
        if mask == None:
            print("can not find %s mask" % mask_name)
        maskbuffer = mask.get_voxel_buffer()
        mask_list.append((mask_name, maskbuffer))
    mimics.file.close_project()

    #
    mimics.file.open_project(project_path)

    for i, mask in enumerate(mask_list):
        mask_a = mimics.segment.create_mask()
        mask_a.name = mask[0]
        mask_a.set_voxel_buffer(mask[1])
    mimics.view.set_contrast(lower_point=(-200 + 1024, 0), upper_point=(1000 + 1024, 1))
    mimics.file.save_project()

    os.remove(old_mcs_path)

    print("end")

    return True

def importmask(mcs_proj, mask_name):
    mask = sitk.ReadImage(mask_name)
    mask = sitk.GetArrayFromImage(mask).transpose()

    mimics.file.open_project(mcs_proj)

    mask_a = mimics.segment.create_mask()
    mask_a.name = "left_ventricle_new"
    mask_a.set_voxel_buffer(mask == 2)

    mask_a = mimics.segment.create_mask()
    mask_a.name = "aorta_new"
    mask_a.set_voxel_buffer(mask == 1)

    # mimics.view.set_contrast(lower_point=(-200+1024,0),upper_point=(1200+1024,1))
    if mimics.file.is_project_loaded():
        if mimics.file.is_project_modified():
            mimics.file.save_project()
        mimics.file.close_project()
    #

def createMcsProject_mhd(mhd_path, project_path):
    """
    Parameters
    ----------
    mhd_path: path of image.mhd
    project_path: path of .mcs

    Returns None
    -------

    """
    if mimics.file.is_project_loaded():
        if mimics.file.is_project_modified():
            mimics.file.save_project()
        mimics.file.close_project()

    tempDir = r"F:\Temp\dicom"

    if not os.path.exists(r"F:\Temp"):
        os.mkdir(r"F:\Temp")

    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)
    os.mkdir(tempDir)

    mhd2dicom(mhd_path, tempDir)
    input_dir = tempDir

    input_path = []
    for root, _, files in os.walk(input_dir):
        input_path.extend(os.path.join(root, f) for f in files)

    image_objs = mimics.file.test_images(filenames=input_path, force_raw_import=False)
    print(len(image_objs))

    conf_images = mimics.file.configure_dicom_images(imagefiles=image_objs)
    print(len(conf_images))

    studies = mimics.file.split_images_into_studies(configured_imagefiles=conf_images,
                                                    patient_name_grouping=True,
                                                    series_description_grouping=True,
                                                    study_description_grouping=True)
    if (len(studies) != 1):
        print(len(studies))
        print("!!!error!!!" + mhd_path)
        return

    image_data = mimics.file.load_series_into_memory(studies=[studies[0]])
    mimics.file.open_images_as_project(imagedata=image_data)
    mimics.file.save_project(filename=project_path + '/n_a.mcs')
    ##mimics.file.save_project(filename=project_path)
    mimics.file.close_project()


def createMcsProject_DCM(dcm_path, project_path):
    if mimics.file.is_project_loaded():
        if mimics.file.is_project_modified():
            mimics.file.save_project()
        mimics.file.close_project()

    input_path = []
    for root, _, files in os.walk(dcm_path):
        input_path.extend(os.path.join(root, f) for f in files)

    image_objs = mimics.file.test_images(filenames=input_path, force_raw_import=False)
    print(len(image_objs))

    conf_images = mimics.file.configure_dicom_images(imagefiles=image_objs)
    print(len(conf_images))

    studies = mimics.file.split_images_into_studies(configured_imagefiles=conf_images,
                                                    patient_name_grouping=True,
                                                    series_description_grouping=True,
                                                    study_description_grouping=True)
    if (len(studies) != 1):
        print(len(studies))
        print("!!!error!!!" + dcm_path)
        return

    image_data = mimics.file.load_series_into_memory(studies=[studies[0]])
    mimics.file.open_images_as_project(imagedata=image_data)
    mimics.file.save_project(filename=project_path + '/n_a.mcs')
    mimics.file.close_project()


def exportmask(mcs_proj, mask_name):
    # if os.path.exists(mask_name):
    # return
    dirname = os.path.dirname(mask_name)
    im = sitk.ReadImage(dirname + '/image.mhd')
    im_data = sitk.GetArrayFromImage(im)

    mimics.file.open_project(mcs_proj)

    # mask_a = mimics.segment.create_mask()
    # mask_a.name  = "PV"
    # mask_a.set_voxel_buffer(mask==1)

    # mask_a = mimics.segment.create_mask()
    # mask_a.name  = "PA"
    # mask_a.set_voxel_buffer(mask==2)

    # mimics.view.set_contrast(lower_point=(-200+1024,0),upper_point=(1200+1024,1))

    #

    mask_aorta = mimics.data.masks.find("aorta")
    mask_left_ventricle = mimics.data.masks.find("left_ventricle")
    maskarray_aorta = np.asarray(mask_aorta.get_voxel_buffer(), dtype=np.ubyte)
    maskarray_left_ventricle = np.asarray(mask_left_ventricle.get_voxel_buffer(), dtype=np.ubyte)

    maskarray_aorta = maskarray_aorta.transpose()
    maskarray_aorta[im_data < 80] = 0
    maskarray_left_ventricle = maskarray_left_ventricle.transpose()

    maskarray = maskarray_aorta.copy()
    maskarray[maskarray_left_ventricle == 1] = 2
    outImg = sitk.GetImageFromArray(maskarray)
    outImg.CopyInformation(im)
    sitk.WriteImage(outImg, mask_name, True)

    if mimics.file.is_project_loaded():
        if mimics.file.is_project_modified():
            mimics.file.save_project()
        mimics.file.close_project()


def exportmask1(mcs_proj, mask_name):
    # if os.path.exists(mask_name):
    # return
    mimics.file.open_project(mcs_proj)

    mask_skull__lz = mimics.data.masks.find("skull__lz")
    maskarray_skull__lz = np.asarray(mask_skull__lz.get_voxel_buffer(), dtype=np.ubyte)

    maskarray_skull__lz = maskarray_skull__lz.transpose()

    maskarray = maskarray_skull__lz.copy()
    outImg = sitk.GetImageFromArray(maskarray)
    spacing = (0.58593799999999996, 0.58593799999999996, 0.80000000000000004)
    outImg.SetSpacing(spacing)
    sitk.WriteImage(outImg, mask_name, True)

    if mimics.file.is_project_loaded():
        if mimics.file.is_project_modified():
            mimics.file.save_project()
        mimics.file.close_project()


def exportpoint(mcs_proj):
    names = [
        "ica_mca_end_right",
        "ica_mca_bifurcation_right",
        "ica_hypophysial_fossa_turning_1_right",
        "ica_hypophysial_fossa_turning_2_right",
        "ica_into_skull_right",
        "cca_ica_bifurcation_right",
        "va_sa_bifurcation_right",
        "cca_sa_bifurcation_right",
        "sa_arc_right",
        "ica_mca_end_left",
        "ica_mca_bifurcation_left",
        "ica_hypophysial_fossa_turning_1_left",
        "ica_hypophysial_fossa_turning_2_left",
        "ica_into_skull_left",
        "cca_ica_bifurcation_left",
        "lcca_arc_mid",
        "ba_pca_end_right",
        "ba_pca_bifurcation_right",
        "va_ba_bifurcation_right",
        "va_into_skull_right",
        "va_turning_1_right",
        "va_turning_2_right",
        "va_turning_3_right",
        "va_vertebra_3rd_right",
        "va_vertebra_6rd_right",
        "ba_pca_end_left",
        "ba_pca_bifurcation_left",
        "va_ba_bifurcation_left",
        "va_into_skull_left",
        "va_turning_1_left",
        "va_turning_2_left",
        "va_turning_3_left",
        "va_vertebra_3rd_left",
        "va_vertebra_6rd_left",
        "va_left_end",
        "sa_arc_left"
    ]
    mimics.file.open_project(mcs_proj)
    file_name = mcs_proj.replace('.mcs', '_centerline_keypoints.json')
    point_dict = {}
    for i in range(36):
        point_name = 'centerline_keypoint_' + names[i] + '__tj'
        point = mimics.data.points.find(point_name)
        point_dict[names[i]] = [point.x, point.y, point.z]
    print(point_dict)

    with open(file_name, 'w') as f:
        json.dump(point_dict, f)

    if mimics.file.is_project_loaded():
        if mimics.file.is_project_modified():
            mimics.file.save_project()
        mimics.file.close_project()