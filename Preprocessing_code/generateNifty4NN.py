import os
import numpy as np
import dicom2nifti
import nibabel as nib
# -- -- -- -- -- -- -- -- -- -- --
import util_dcm
import util_nifti
import util_general as util_gen
#import util_visualization as util_vis
# -- -- -- -- -- -- -- -- -- -- --

#  **********************
#  *     Main code      *
#  **********************

# Settings (you might change them)
block = 500  # maximum number of dicom files to load at once
resample_size = [2, 2, 2]
isotropic_resample_size = "2"
tags_to_get = ['SeriesInstanceUID', 'SeriesDescription', 'ImageOrientationPatient']  # Has to be list
folder_niftiUZ = 'patientsNifti'  # Where files converted to Nifti are saved
path_in_dicom = '/staging/leuven/stg_00051/students/brain_rad'

# Init variables (do not change)
file_names = ['T1', 'T1_CE', 'FLAIR', 'T2']
cnt = 0

# Create output folder and get input folders
path_out_nifti = util_gen.create_folder_in_dir(folder_niftiUZ, '/data/leuven/335/vsc33557/pyCode/code_Design_v3')
folders_patients = os.listdir(path_in_dicom)

# For each patient
for folder in folders_patients:
    str_case = 'case_' + str(cnt)
    cnt = cnt + 1
    print(str_case+': '+folder)

    # Get files and tags
    path_this_pat = os.path.join(path_in_dicom,folder)
    files_pat = os.listdir(path_this_pat)
    files_aux, tags_obtained = util_dcm.get_tags_per_block_size(files_pat, path_this_pat, tags_to_get, block)

    # Get list unique uid tags
    unique_tags, unique_uid, uids, idxs = util_dcm.get_unique_tags_combination(tags_obtained, tags_to_get)

    # Find the 4 types of needed files looking into the 'series description' tags
    # TODO: change str search when we had better tags
    idx = [-1]*4

    # 1. Find T1
    if 'pre_AX_1mm' in unique_tags[tags_to_get[1]]:
        idx[0] = unique_tags[tags_to_get[1]].index('pre_AX_1mm')
    elif 'PRE_TRA' in unique_tags[tags_to_get[1]]:
        idx[0] = unique_tags[tags_to_get[1]].index('PRE_TRA')
    elif 'preAX_1mm' in unique_tags[tags_to_get[1]]:
        idx[0] = unique_tags[tags_to_get[1]].index('preAX_1mm')

    # 2. Find T1_CE
    if 'post_AX_1mm' in unique_tags[tags_to_get[1]]:
        idx[1] = unique_tags[tags_to_get[1]].index('post_AX_1mm')
    elif 'POST_TRA' in unique_tags[tags_to_get[1]]:
        idx[1] = unique_tags[tags_to_get[1]].index('POST_TRA')
    elif 'postAX_1mm' in unique_tags[tags_to_get[1]]:
        idx[1] = unique_tags[tags_to_get[1]].index('postAX_1mm')

    # 3. Find T2
    if 'T2W_MV_aTSE' in unique_tags[tags_to_get[1]]:
        idx[2] = unique_tags[tags_to_get[1]].index('T2W_MV_aTSE')

    # 4. Find FLAIR
    if 'sb0' in unique_tags[tags_to_get[1]]:
        idx[3] = unique_tags[tags_to_get[1]].index('sb0')

    # For each tag selected based on series description, get the corresponding dicom files and its tags
    cnt2 = 0
    # If the patient had the four types of required images
    if -1 not in idx:
        # For each type of image
        for i in idx:
            # Find the slices with the corresponding tag uid
            print(file_names[cnt2] + ': ' + 'idx = ' + str(i))
            tags_selected = util_dcm.get_tags_selected(unique_tags, i)
            uid_selected = unique_uid[int(i)]
            files_sel = util_dcm.get_files_by_tag(files_aux, uids, uid_selected)
            info_dicom = util_dcm.save_info_dicom(path_this_pat, files_sel, tags_selected)

            # Get slices
            slices_dicom, bool_dicom_loaded = util_dcm.get_dicom_slices(info_dicom)

            # Convert to Nifti
            if bool_dicom_loaded:
                # Create folders and path where to save generated files
                output_file = file_names[cnt2]+'.nii'
                path_out_nifti_pat = util_gen.create_folder_in_dir(str_case, path_out_nifti)
                output_path = os.path.join(path_out_nifti_pat, output_file)
                # Convert files from dicom to nifti
                dicom2nifti.convert_dicom.dicom_array_to_nifti(slices_dicom, output_path, reorient_nifti=True)
                # Get nifti data, resample and save resampled nifti
                nifti_obj = nib.load(output_path)
                # Skull removal
                if file_names[cnt2] is 'T1': # Get the mask: T1 is the first since it is in idx[0]
                    mask = util_nifti.skull_removal_get_mask(nifti_obj)
                print('done')
                new_nifti_obj = util_nifti.do_skull_removal(nifti_obj,mask)
                print('done2')
                util_nifti.resample_nifti(new_nifti_obj, resample_size, isotropic_resample_size, output_path)
                print('done3')

            else:
                print("\n!!! - There are not dicom slices loaded")

            cnt2 = cnt2 + 1
    else:
        print("\n!!! - This case does not contain the 4 image type modalities required")