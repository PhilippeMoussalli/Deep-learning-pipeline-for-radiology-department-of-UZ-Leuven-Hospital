import nibabel as nib
import numpy as np
# -- -- -- -- -- -- -- -- -- -- --
import util_visualization as util_vis
import util_nifti
# -- -- -- -- -- -- -- -- -- -- --

# A. Visualize conversion dicom nifti (uncomment to try)
'''
#nifti_obj = nib.load('/data/leuven/335/vsc33557/pyCode/code_Design_v2/patientsNifti/case_4/T1_2mm.nii')
nifti_obj = nib.load('/data/leuven/335/vsc33557/pyCode/code_Design_v2/patientsNifti/case_1/T1_CE.nii')

volume = nifti_obj.get_data()
util_vis.multi_slice_viewer2(volume)
'''

# B. Visualize BRATS testing (uncomment to try)

test_BRATS_T1 = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing_brats/case_0/T1_2mm.nii'
test_BRATS_T1CE = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing_brats/case_0/T1_CE_2mm.nii'
test_BRATS_T2 = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing_brats/case_0/T2_2mm.nii'
test_BRATS_Flair = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing_brats/case_0/FLAIR_2mm.nii'
test_BRATS_GTW = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing_brats/case_0/GT_W_2mm.nii'
test_BRATS_outcome = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing_brats/Runs/run_BRATS_U-Net_2mm/case_0/Testing/experiment_foldAll_20200417_Round_0_Fold_0.nii'

nifti_obj0 = nib.load(test_BRATS_T1)
nifti_obj1 = nib.load(test_BRATS_T1CE)
nifti_obj2 = nib.load(test_BRATS_T2)
nifti_obj3 = nib.load(test_BRATS_Flair)
nifti_obj4 = nib.load(test_BRATS_GTW)
nifti_obj5 = nib.load(test_BRATS_outcome)

volume0 = nifti_obj0.get_data()
volume1 = nifti_obj1.get_data()
volume2 = nifti_obj2.get_data()
volume3 = nifti_obj3.get_data()
volume4 = nifti_obj4.get_data()
volume5 = nifti_obj5.get_data()

volumes = [volume0, volume2, volume4, volume1, volume3, volume5]
titles = ['T1', 'T2', 'NN_outcome', 'T1_CE', 'FLAIR', 'GT_W']
util_vis.multi_slice_viewer_testNN(volumes, 2, 3, titles)


# C. Visualize UZ_data testing (uncomment to try)
'''
test_T1 = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/T1_2mm.nii'
test_T1CE = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/T1_CE_2mm.nii'
test_T2 = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/T2_2mm.nii'
test_Flair = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/FLAIR_2mm.nii'
test_outcome = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/Runs/run_BRATS_U-Net_2mm/case_3/Testing/experiment_foldAll_20200417_Round_0_Fold_0.nii'

nifti_obj0 = nib.load(test_T1)
nifti_obj1 = nib.load(test_T1CE)
nifti_obj2 = nib.load(test_T2)
nifti_obj3 = nib.load(test_Flair)
nifti_obj4 = nib.load(test_outcome)


volume0 = nifti_obj0.get_data()
volume1 = nifti_obj1.get_data()
volume2 = nifti_obj2.get_data()
volume3 = nifti_obj3.get_data()
volume4 = nifti_obj4.get_data()
volume5 = np.zeros(volume4.shape) # Since we do not have ground truth

volumes = [volume0, volume2, volume4, volume1, volume3, volume5]
titles = ['T1', 'T2', 'NN_outcome', 'T1_CE', 'FLAIR', 'GT (missing)']
util_vis.multi_slice_viewer_testNN(volumes, 2, 3, titles)
'''


# D. Do and visualize skull removal
'''
test_T1 = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/T1_2mm.nii'
test_T1CE = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/T1_CE_2mm.nii'
test_T2 = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/T2_2mm.nii'
test_Flair = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/case_3/FLAIR_2mm.nii'
test_outcome = '/data/leuven/335/vsc33557/deepvoxnet_core/demo/BRATS_2018_complete/Testing/Runs/run_BRATS_U-Net_2mm/case_3/Testing/experiment_foldAll_20200417_Round_0_Fold_0.nii'

nifti_obj0 = nib.load(test_T1)
nifti_obj1 = nib.load(test_T1CE)
nifti_obj2 = nib.load(test_T2)
nifti_obj3 = nib.load(test_Flair)
nifti_obj4 = nib.load(test_outcome)

mask = util_nifti.skull_removal_get_mask(nifti_obj0)
nifti_obj0 = util_nifti.do_skull_removal(nifti_obj0, mask)
nifti_obj1 = util_nifti.do_skull_removal(nifti_obj1, mask)
nifti_obj2 = util_nifti.do_skull_removal(nifti_obj2, mask)
nifti_obj3 = util_nifti.do_skull_removal(nifti_obj3, mask)
nifti_obj4 = util_nifti.do_skull_removal(nifti_obj4, mask)

volume0 = nifti_obj0.get_data()
volume1 = nifti_obj1.get_data()
volume2 = nifti_obj2.get_data()
volume3 = nifti_obj3.get_data()
volume4 = nifti_obj4.get_data()
volume5 = np.zeros(volume4.shape) # Since we do not have ground truth

volumes = [volume0, volume2, volume4, volume1, volume3, volume5]
titles = ['T1', 'T2', 'NN_outcome', 'T1_CE', 'FLAIR', 'GT (missing)']
util_vis.multi_slice_viewer_testNN(volumes, 2, 3, titles)

'''