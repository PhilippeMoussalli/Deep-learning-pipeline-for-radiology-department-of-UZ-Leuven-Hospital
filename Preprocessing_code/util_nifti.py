import nibabel as nib
import numpy as np
import os
from scipy.ndimage import zoom
from deepbrain import Extractor

# -- -- -- -- -- -- -- -- -- -- --
import util_general as util_gen
# -- -- -- -- -- -- -- -- -- -- --


def load_nifti(path):
    """
    Loads the nifti selected by the user. The user first selects the folder of interest and then the file to read
    inside it.

    Inputs:
    -------
    path: path pointing to a directory that contains folders which contain nifti files.

    Outputs:
    --------
    volume: pixels data of the nifti file

    obj: the nifti object

    bool_info_nifti: True if the nifti file was successfully read
    """
    bool_info_nifti = False

    files, path_selected = util_gen.get_files_by_choosing_folder(path)
    file, option_sel = util_gen.choose_from_list(files, 'Choose the nifti file to use')
    # Check
    if '.nii' in file:
        obj = nib.load(os.path.join(path_selected, file))
        volume = obj.get_data()
        bool_info_nifti = True
    else:
        print('The selected file is not a nifti file\n')
        volume = []
        obj = []
    return volume, obj, bool_info_nifti


def resample_nifti(ni_image, resample_size, isotropic_resample_size, path):
    """
    Resamples the nifti image to fit the resample_size and saves the resampled image in the indicated path
    adding to the name of the file the string "_xmm" where x is the value specified in isotropic_resample_size
    """

    # Get original nifti attribute values
    zooms = ni_image.header.get_zooms()
    affine = ni_image.affine
    data = ni_image.get_data()

    print("\t", zooms)
    assert np.allclose(zooms, np.linalg.norm(affine[:3, :3], 2, axis=0), atol=0.01)

    # Modify to get new attribute values
    zooms_ = [z / (r_s or z) for z, r_s in zip(zooms, resample_size[:len(zooms)])]
    affine_ = affine.copy()
    affine_[:3, :3] /= np.array(zooms_)
    assert data.ndim < 5
    data_ = zoom(data, zooms_, order=1, mode='nearest')

    # Create nifti image and save it
    img_ = nib.Nifti1Image(data_, affine=affine_)
    nib.save(img_, path[:-4] + "_{}mm.nii".format(isotropic_resample_size))


def skull_removal_get_mask(nib_T1_obj):
    volume = nib_T1_obj.get_fdata()
    ext = Extractor()

    # `prob` will be a 3d numpy image containing probability
    # of being brain tissue for each of the voxels in `img`
    prob = ext.run(volume)

    # mask can be obtained as:
    mask = prob > 0.5

    return mask


def do_skull_removal(nib_obj, mask):
    volume = nib_obj.get_fdata()
    volume2 = np.array(volume)
    volume2[mask == False] = 0
    new_nib_obj = nib.Nifti1Image(volume2, nib_obj.affine, nib_obj.header)

    return new_nib_obj