import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from Functions import *
from glob import glob
from matplotlib.lines import Line2D

# Path of NN output
nifti_pred_vol_path = r"C:\Users\Philippe\Desktop\Design project\test_rtstruct\Testing\Runs\run_BRATS_U-Net_2mm\case_0\Testing"
# Path of modalities and GT
nifti_mod_vol_path = r"C:\Users\Philippe\Desktop\Design project\test_rtstruct\Testing\case_0"

# Load modalities and GT
Flair = load_nifti_lps(os.path.join(nifti_mod_vol_path, "Flair_2mm.nii"))
T1= load_nifti_lps(os.path.join(nifti_mod_vol_path, "T1_2mm.nii"))
T1_CE = load_nifti_lps(os.path.join(nifti_mod_vol_path, "T1_CE_2mm.nii"))
T2= load_nifti_lps(os.path.join(nifti_mod_vol_path, "T2_2mm.nii"))

#Load prediction (Binary segmentation)
Binary_pred = np.load(glob(os.path.join(os.path.join(nifti_pred_vol_path, "rt_struct"), "*.npy"))[0])

#Load Ground truth (Binary segmentation)
Binary_GT = np.load(glob(os.path.join(os.path.join(nifti_mod_vol_path, "rt_struct"), "*.npy"))[0])
"""
Visualize RT struct either with respect to the original nifti segmentation volume or with the dicom reference files
generated from the nifti
"""

# Option 1: Visualize RTstruct (contour) with respect to predicted volume in nii format
nifti_file_name = "experiment_foldAll_20200417_Round_0_Fold_0.nii"
nifti_file_dir = load_nifti_lps(os.path.join(nifti_pred_vol_path,nifti_file_name))

final_index = Binary_pred.shape[2]

def multi_slice_viewer_contour(Flair,T1,T1_CE,T2,pred,GT):
 # Visualization of 4 modalities with predicted and GT segmentation overlaid
    remove_keymap_conflicts({'j', 'k'})
    fig,ax = plt.subplots(2, 2, sharex=True, sharey=True)
    ax = fig.axes
    volumes = [Flair, T1, T1_CE, T2]
    titles = ["Flair", "T1", "T1_CE", "T2"]

    for i in range(len(ax)):
        ax[i].volume1 = volumes[i]
        ax[i].pred = np.ma.masked_where(pred == 0, pred)
        ax[i].GT = np.ma.masked_where(GT == 0, GT)
        ax[i].index = volumes[i].shape[2] // 2
        ax[i].imshow(volumes[i][:, :, ax[i].index], cmap='Greys_r', interpolation='none')
        ax[i].imshow(np.ma.masked_where(pred[:, :, ax[i].index] == 0, pred[:, :, ax[i].index]), cmap='autumn',
                    interpolation='none', alpha=1)
        ax[i].imshow(np.ma.masked_where(GT[:, :, ax[i].index] == 0, GT[:, :, ax[i].index]), cmap='summer',
                    interpolation='none', alpha=1)
        ax[i].set_title(titles[i])

    legend_elements = [Line2D([0], [0], color='g', lw=4, label='Ground Truth'),
                       Line2D([0], [0], color='r', lw=4, label='Prediction')]
    fig.suptitle("Slice " + str(ax[1].index) + "/" + str(final_index))
    fig.legend(handles=legend_elements, loc='upper right')
    """Create thread."""
    fig.canvas.mpl_connect('key_press_event', process_key_contour)
    plt.show()

def process_key_contour(event):

    fig = event.canvas.figure
    ax = fig.axes

    if event.key == 'j':
        for this_ax in ax:
            previous_slice_contour(this_ax)

    elif event.key == 'k':
        for this_ax in ax:
            next_slice_contour(this_ax)

    fig.suptitle("Slice " + str(ax[0].index) + "/" + str(final_index))
    fig.canvas.draw()

def previous_slice_contour(ax):
    """Go to the previous slice."""
    volume1 = ax.volume1
    pred = ax.pred
    GT = ax.GT
    ax.index = (ax.index - 1) % volume1.shape[2]  # wrap around using %
    ax.images[0].set_array(volume1[:, :, ax.index])
    ax.images[1].set_array(pred[:, :, ax.index])
    ax.images[2].set_array(GT[:, :, ax.index])

def next_slice_contour(ax):
    """Go to the next slice."""
    volume1 = ax.volume1
    pred = ax.pred
    GT = ax.GT
    ax.index = (ax.index + 1) % volume1.shape[2]
    ax.images[0].set_array(volume1[:, :, ax.index])
    ax.images[1].set_array(pred[:, :, ax.index])
    ax.images[2].set_array(GT[:, :, ax.index])

def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)

multi_slice_viewer_contour(Flair, T1, T1_CE, T2, Binary_pred, Binary_GT)
