import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
# -- -- -- -- -- -- -- -- -- -- --


def multi_slice_viewer0(volume, title=''):
    """
    Shows the different slices of the given volume. Iterates over the first dimension ([0]).
    Press j and k to go down and up.
    """
    remove_keymap_conflicts({'j', 'k'})
    final_index = volume.shape[0]
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[0] // 2
    ax.final_index = final_index
    ax.imshow(volume[ax.index, :, :], cmap='Greys_r')  # Plot z axis and transpose to show correct orientation
    ax.set_title(title)
    fig.suptitle("Slice " + str(ax.index) + "/" + str(final_index))
    fig.canvas.mpl_connect('key_press_event', process_key0)
    plt.show()


def multi_slice_viewer2(volume, title=''):
    """
    Shows the different slices of the given volume. Iterates over the last dimension ([2]).
    Press j and k to go down and up.
    """
    remove_keymap_conflicts({'j', 'k'})
    final_index = volume.shape[2]
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = volume.shape[2] // 2
    ax.final_index = final_index
    ax.imshow(volume[:, :, ax.index].T, cmap='Greys_r')  # Plot z axis and transpose to show correct orientation
    ax.set_title(title)
    fig.suptitle("Slice " + str(ax.index) + "/" + str(final_index))
    fig.canvas.mpl_connect('key_press_event', process_key2)
    plt.show()


def multi_slice_viewer_testNN(volumes, subplot_dim_1, subplot_dim_2, titles):
    """
    Shows the different slices of the given volumes. Iterates over the last dimension ([2]) for all the volumes.
    You need to specify subplots dimensions in order to tell the program the subplot layout to use, and the name
    you want to show as title of each image.
    Press j and k to go down and up.
    """
    remove_keymap_conflicts({'j', 'k'})
    final_index = []
    for volume in volumes:
        final_index.append(volume.shape[2])

    fig, ax = plt.subplots(subplot_dim_1, subplot_dim_2)
    ax = fig.axes
    cnt = 0
    for volume_x in volumes:
        ax[cnt].volume = volume_x
        ax[cnt].index = volume_x.shape[2] // 2
        ax[cnt].final_index = final_index[cnt]
        ax[cnt].imshow(volume_x[:, :, ax[cnt].index].T,
                       cmap='Greys_r')  # Plot z axis and transpose to show correct orientation
        ax[cnt].set_title(titles[cnt])
        cnt = cnt + 1

    fig.suptitle("Slice " + str(ax[cnt - 1].index) + "/" + str(final_index[cnt - 1]))
    fig.canvas.mpl_connect('key_press_event', process_key_multiple_vis)
    plt.show()


def multi_slice_viewer_double_vis(volume1, volume2, titles=['', '']):
    """
    Shows the different slices of the two given volumes. The first volume iterates over the first dimension ([0])
    and the second over the last dimension ([2])
    Press j and k to go down and up.
    """
    remove_keymap_conflicts({'j', 'k'})
    final_index1 = volume1.shape[0]
    final_index2 = volume2.shape[2]
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.volume = volume1
    ax1.index = volume1.shape[0] // 2
    ax1.final_index = final_index1
    ax1.imshow(volume1[ax1.index, :, :], cmap='Greys_r')  # Plot z axis and transpose to show correct orientation
    ax1.set_title('Slice ' + str(ax1.index) + '/' + str(final_index1))

    ax2.volume = volume2
    ax2.index = volume2.shape[2] // 2
    ax2.final_index = final_index2
    ax2.imshow(volume2[:, :, ax2.index].T, cmap='Greys_r')  # Plot z axis and transpose to show correct orientation
    ax2.set_title('Slice ' + str(ax2.index) + '/' + str(final_index2))

    if titles[0] is not '' and titles[1] is not '':
        fig.suptitle(titles[0] + " vs " + titles[1])
    fig.canvas.mpl_connect('key_press_event', process_key_double_vis)
    plt.show()


def process_key0(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice0(ax)
        fig.suptitle("Slice " + str(ax.index) + "/" + str(ax.final_index))
    elif event.key == 'k':
        next_slice0(ax)
        fig.suptitle("Slice " + str(ax.index) + "/" + str(ax.final_index))
    fig.canvas.draw()


def process_key2(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == 'j':
        previous_slice2(ax)
        fig.suptitle("Slice " + str(ax.index) + "/" + str(ax.final_index))
    elif event.key == 'k':
        next_slice2(ax)
        fig.suptitle("Slice " + str(ax.index) + "/" + str(ax.final_index))
    fig.canvas.draw()


def process_key_multiple_vis(event):
    fig = event.canvas.figure
    ax = fig.axes
    if event.key == 'j':
        for this_ax in ax:
            previous_slice2(this_ax)
            fig.suptitle("Slice " + str(ax[0].index) + "/" + str(ax[0].final_index))
    elif event.key == 'k':
        for this_ax in ax:
            next_slice2(this_ax)
            fig.suptitle("Slice " + str(ax[0].index) + "/" + str(ax[0].final_index))
    fig.canvas.draw()


def process_key_double_vis(event):
    fig = event.canvas.figure
    ax1 = fig.axes[0]
    ax2 = fig.axes[1]
    if event.key == 'j':
        previous_slice0(ax1)
        previous_slice2(ax2)
        ax1.set_title("Slice " + str(ax1.index) + "/" + str(ax1.final_index))
        ax2.set_title("Slice " + str(ax2.index) + "/" + str(ax2.final_index))
    elif event.key == 'k':
        next_slice0(ax1)
        next_slice2(ax2)
        ax1.set_title("Slice " + str(ax1.index) + "/" + str(ax1.final_index))
        ax2.set_title("Slice " + str(ax2.index) + "/" + str(ax2.final_index))

    fig.canvas.draw()


def previous_slice0(ax):
    """Go to the previous slice."""
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[0]  # wrap around using %
    ax.images[0].set_array(volume[ax.index, :, :])
    # ax.set_title('Slice ' + str(ax.index) + '/' + str(ax.final_index))


def next_slice0(ax):
    """Go to the next slice."""
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[0]
    ax.images[0].set_array(volume[ax.index, :, :])
    # ax.set_title('Slice ' + str(ax.index) + '/' + str(ax.final_index))


def previous_slice2(ax):
    """Go to the previous slice."""
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[2]  # wrap around using %
    ax.images[0].set_array(volume[:, :, ax.index].T)
    # ax.set_title('Slice ' + str(ax.index) + '/' + str(ax.final_index))


def next_slice2(ax):
    """Go to the next slice."""
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[2]
    ax.images[0].set_array(volume[:, :, ax.index].T)
    # ax.set_title('Slice ' + str(ax.index) + '/' + str(ax.final_index))


def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)