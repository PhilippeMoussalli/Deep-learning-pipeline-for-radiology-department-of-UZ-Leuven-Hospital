from Functions import *

nifti_path = r"C:\Users\Philippe\Desktop\Design project\test_rtstruct\Testing\case_0"
nifti_file_name = "GT_W_2mm.nii"
output_file_name = "rt_struct_"+nifti_file_name



"""
#Dicom_path = VSC_path --> Location of patient data
#resample_size = [Dicom_path.PixelSpacing[0],Dicom_path.PixelSpacing[0],Dicom_path.	SliceThickness]  [1,1,1]

1) Upsample/ Downsample the obtain mask array to the original size of the Dicom reference (Before downsampling to 2mm 
 for the NN) --> function commented Uncomment this function when referring to the hospital data to resample the 
 segmentation to the proper resolution

isotropic_resample_size =resample_size[0] # 1mm  (original UZ Leuven hospital data resolution, but this can vary)
resample_nifti(nifti_path,nifti_file_name,resample_size, isotropic_resample_size, output_path)
"""


"""
2) Convert the nifti output segmentation of the NN to Dicom files each having a unique SOP reference. The Dicom files are
need to:

    A) Copy tags to the rtstruct file that is to be constructed
    B) Mapping the "SOP Instance UID" reference to the equivalent RT struct slice in order to map from World coordinate to 
    to voxel coordinates ("Image position patient") tag  
 

The output dicom files are saved in "output_dir_dcm". The number of files is equivalent to the number of slices in the
nifti file.

The affine of the nifti file is passed to "convert_nifti_to_rtstruct" to obtain an rtstruct with in RAS World coordinates
"""

affine,output_dir_dcm= convert_nifti_to_dicom(nifti_path,nifti_file_name)

"""
3) RT struct file is created from the nifti output of the NN. The output of this function gives the path "rt_path" of 
the rtstruct file.
Z_start and Z_end are the start and end index of the segmentation with reference to the original dicom file (for example
a dicom slice of 78 slices with only 30 slices of contours can have a z_start=20 and z_end=50). Those indexes will be
used to construct the 2d Binary contour array.
"""
rt_file_path,z_start,z_end= convert_nifti_to_rtstruct(nifti_path,nifti_file_name,affine,output_dir_dcm,output_file_name)

"""
4) Convert the obtained rtstruct to a 2d Binary contour array that will be used for visualization. The output is saved
in " Binary_contour_segmentation_volume" folder 
"""
contour_volume = rtstruct_to_voxel_index(rt_file_path, output_dir_dcm,z_start,z_end)
np.save(os.path.join(os.path.split(rt_file_path)[0],'Binary_surface_'+nifti_file_name.split(".")[0]),contour_volume)


