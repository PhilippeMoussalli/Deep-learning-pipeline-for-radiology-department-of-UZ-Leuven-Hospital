import os
import numpy as np
import dicom2nifti
# -- -- -- -- -- -- -- -- -- -- --
import util_dcm
import util_nifti
import util_general as util_gen
import util_visualization as util_vis
#  -------------------------------------------------------------------------------------------------------------------


#  **********************
#  *     Main code      *
#  **********************

# Settings (you might change them)
block = 500
isotropic_resample_size = "2"
resample_size = [2, 2, None]

path_in_dicom = '/staging/leuven/stg_00051/students/brain_rad'
path_in_nifti = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Training'
tags_to_get = ['SeriesInstanceUID', 'SeriesDescription', 'ImageOrientationPatient']  # Has to be list
folder_txt = 'txtDicomInfo'  # Where list files Dicom are saved
folder_nifti = 'niftiConvertedData'  # Where files converted to Nifti are saved

# Init variables (do not change)
bool_exit = False
bool_info_dicom = False
bool_dicom_loaded = False
bool_nifti_loaded = False

#  Main code
while True:
    opt_main_menu = util_gen.menu_main()

    # A. LOAD DICOM
    if opt_main_menu is '0':
        info_dicom, bool_info_dicom, bool_exit = util_dcm.load_dicom(tags_to_get, path_in_dicom, folder_txt, block)

    # B. LOAD NIFTI
    elif opt_main_menu is '1':
        volume2, nifti_obj, bool_nifti_loaded = util_nifti.load_nifti(path_in_nifti)

    # C. CONVERT DICOM TO NIFTI
    elif opt_main_menu is '2':

        # Check if dicom info loaded
        if bool_info_dicom:
            slices_dicom, bool_dicom_loaded = util_dcm.get_dicom_slices(info_dicom)

            # Check if slices where read
            if bool_dicom_loaded:
                # If so, convert and create folders and path where to save it
                output_file = util_dcm.create_filename_from_tags(info_dicom['dict_tags'], '.nii')
                path_out_nifti = util_gen.create_folder_in_dir(folder_nifti)
                path_out_nifti = util_gen.create_folder_in_dir(info_dicom['dict_tags']['SeriesInstanceUID'],
                                                               path_out_nifti)
                output_path = os.path.join(path_out_nifti, output_file)
                dicom2nifti.convert_dicom.dicom_array_to_nifti(slices_dicom, output_path, reorient_nifti=True)
            else:
                print("\n!!! - There are not dicom slices loaded")
        else:
            print("\n!!! -  There are not dicom files information loaded")

    # D. VISUALIZE DICOM:
    elif opt_main_menu is '3':
        if bool_info_dicom:
            slices_dicom, bool_dicom_loaded = util_dcm.get_dicom_slices(info_dicom)
            if bool_dicom_loaded:  # Check
                volume1 = np.stack([s.pixel_array for s in slices_dicom])
                volume1 = volume1.astype(np.int16)
                util_vis.multi_slice_viewer0(volume1)
            else:
                print("\n!!! - There are not dicom slices loaded")
        else:
            print("\n!!! -  There are not dicom files information loaded")

    # E. VISUALIZE NIFTI:
    elif opt_main_menu is '4':
        if bool_nifti_loaded:
            util_vis.multi_slice_viewer2(volume2)
        else:
            print("\n!!! - There are not nifti slices loaded")

    # F. VISUALIZE DICOM AND NIFTI:
    elif opt_main_menu is '5':

        if bool_info_dicom and bool_nifti_loaded:  # TODO check how can this happen

            # Get dicom slices:
            slices_dicom, bool_dicom_loaded = util_dcm.get_dicom_slices(info_dicom)
            if bool_dicom_loaded:
                volume1 = np.stack([s.pixel_array for s in slices_dicom])
                volume1 = volume1.astype(np.int16)

            # Visualize
            util_vis.multi_slice_viewer_double_vis(volume1, volume2,['Dicom','Nifti'])

        if not bool_info_dicom:
                print('\n!!! - There are not dicom files loaded')
        if not bool_dicom_loaded:
                print("\n!!! - There are not dicom slices loaded")
        if not bool_nifti_loaded:
                print("\n!!! - There are not nifti slices loaded")

    elif opt_main_menu is '6':
        #files_folder, path_selected = util_gen.get_files_by_choosing_folder(os.path.join(os.getcwd(),folder_nifti)) # TODO check if exits
        #item_sel, option_sel = util_gen.choose_from_list(files_folder, "Select file:")
        volume3, nifti_obj2, bool_nifti_loaded = util_dcm.load_nifti(os.path.join(os.getcwd(),folder_nifti))
        voxel_size = nifti_obj2.header.get_zooms()
        util_nifti.resample_nifti(nifti_obj2, resample_size, isotropic_resample_size)

    elif opt_main_menu is 'q':
        print("\nBye")
        break

    else:  # Check
        print("\n!!! - The option does not exit")
