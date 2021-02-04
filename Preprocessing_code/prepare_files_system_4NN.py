import os
import nibabel as nib
import util_visualization as util_vis
import numpy as np

import util_general as util_gen

def zero_padding(volume, desired_shape):
    """
    Zero pads the images so they can have the desired size, by adding zeros in both sides of each
    dimension, keeping the image centered.

    Inputs:
        volume: original image data
        desired_shape: array containing the 3D shape of the new volume

    Outputs:
        new_vol: the zero-pad volume
    """

    x_side1 = np.floor((desired_shape[0] - volume.shape[0]) / 2).astype(np.int)
    x_side2 = np.ceil((desired_shape[0] - volume.shape[0]) / 2).astype(np.int)
    y_side1 = np.ceil((desired_shape[1] - volume.shape[1]) / 2).astype(np.int)
    y_side2 = np.floor((desired_shape[1] - volume.shape[1]) / 2).astype(np.int)
    z_side1 = np.ceil((desired_shape[2] - volume.shape[2]) / 2).astype(np.int)
    z_side2 = np.floor((desired_shape[2] - volume.shape[2]) / 2).astype(np.int)
    new_vol = np.pad(volume, ((x_side1, x_side2), (y_side1, y_side2), (z_side1, z_side2)), mode='constant', constant_values=0)
    return new_vol


# --------------------------------------------------------------------------------------------------------------------
#  **********************
#  *   Main code        *
#  **********************

# Settings
path_in_cases = '/data/leuven/335/vsc33557/pyCode/code_Design_v2/patientsNifti'
path_out_cases = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing'

# Read each case/patient folder in the directory to retrieve the image files
cases = os.listdir(path_in_cases)
for case in cases:

    nifti_objs = []
    volumes = []
    name_files = []
    path_this_case = os.path.join(path_in_cases, case)
    files = os.listdir(path_this_case)

    # Read volume or each modality image
    for file in files:
        if '2mm' in file:
            name_files.append(file)
            nii_obj = nib.load(os.path.join(path_this_case, file))
            nifti_objs.append(nii_obj)
            volumes.append(nii_obj.get_data())

    # Get max shape of volumes
    shapes = [vol.shape for vol in volumes]
    coord = np.vstack(shapes)
    max_coord = coord.max(0)

    # For each image modality
    new_objs_nii = []
    new_volumes = []
    cnt = 0
    for vol in volumes:

        # Zero pad volumes to max shape
        new_vol = zero_padding(vol, max_coord)

        # Create new nii image
        empty_header = nib.Nifti1Header()
        new_nii = nib.Nifti1Image(new_vol, nifti_objs[cnt].affine, empty_header)

        # Save image in the output directory (creates it if it does not exit)
        path_pat = util_gen.create_folder_in_dir(case, path_out_cases)
        #nib.save(new_nii, os.path.join(path_pat, name_files[cnt]))
        cnt = cnt + 1

        # Append for debugging  and visualization purposes
        new_volumes.append(new_vol)
        new_objs_nii.append(new_nii)

    # Visualize all modalities together
    util_vis.multi_slice_viewer_testNN(new_volumes, 2, 2, name_files)

