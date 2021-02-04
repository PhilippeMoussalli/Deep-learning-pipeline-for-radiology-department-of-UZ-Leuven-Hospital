import os
import pydicom as dicom
import numpy as np
import nibabel as nib

# -- -- -- -- -- -- -- -- -- -- --
import util_general as util_gen

# -- -- -- -- -- -- -- -- -- -- --


def load_dicom(tags_to_get, path_in_dicom, folder_txt, block):
    """
    Retrieves the dicom files names, their path and their tags referred in tags_to_get
    A menu guides the user and there are two ways of retrieval:

     A. The user selects the patient folder to work with and the dicom files of interest.
        A menu guides the selection. Files are sorted using the first tag specified in tags_to_get
        (recommended to be SeriesInstanceUID). The retrieved information is also saved in
        an txt file for future loading and avoiding the need of this specific sorting again.

     B. The user chooses between one of the previous generated txt files that contain the
     necessary information to load the dicom files. This process is much faster.

    :param tags_to_get: list of name of tags of interest. The first tag will be used to select the
        dicom files of interest. It is recommended to be "SeriesInstanceUID"
    :param  path_in_dicom: path containing folders with dicom files. Each folder might be a patient or case.
    :param  folder_txt: name of output folder where retrieved info is saved
    :param  block: maximum number of dicom files that can be read at once. Avoids overloading memory.
    :return:
        dicom_info: dictionary containing the list of files selected, their path and their values of the tags referred
            in tags_to_get
        bool_info_dicom: True if the code is executed correctly.
        exit_opt: True if exit is selected in the menu
    """
    # Initialize variables
    dicom_info = {}
    exit_opt = False
    bool_info_dicom = False
    opt_dicom = util_gen.menu_dicom()

    if opt_dicom is "0":

        # A. Select files by UID tag choice input options and save selection
        dicom_info = get_files_from_tag_selection(path_in_dicom, tags_to_get, block)
        path_out_txt = util_gen.create_folder_in_dir(folder_txt)
        save_list_files(path_out_txt, dicom_info)
        bool_info_dicom = True

    elif opt_dicom is "1":

        # B. Get files from folder
        path_file, bool_exits = util_gen.get_file_from_folder_x_in_working_dir(folder_txt)
        if bool_exits:
            dicom_info = read_list_files(path_file)
            bool_info_dicom = True

    elif opt_dicom is "q":

        print("Bye")
        exit_opt = True

    else:  # Check

        print("The option does not exit")

    return dicom_info, bool_info_dicom, exit_opt


def get_files_from_tag_selection(dicom_path, tags2get, block_size=600):
    """
    Allows the user to retrieve the files from the selected folder in the dicom_path directory
    and retrieve only the ones with the chosen tag value. The file names, their path and the
    tags of interest will be saved and returned as info_dicom.

    :param dicom_path: path pointing to directory with folders containing dicom files.
    :param tags2get: list of string with the names of tags of interest. tags2get[0] will be use
        to make the selection of files
    :param block_size: maximum number of dicom files that can be read at once (avoiding memory overload).
    :return:
        info_dicom: dictionary containing files list as 'list_files', path of files as 'path_patient'
            and tags of interest as 'dict_tags'
    """

    # 1. Get PathPatient and files
    files, path_patient = util_gen.get_files_by_choosing_folder(dicom_path)

    # 2. Get all UID tags
    files_aux, tags_obtained = get_tags_per_block_size(files, path_patient, tags2get, block_size)

    # 3. Select UID tag knowing other tag values too (by user input)
    files_sel, tags_selected = get_this_uid_files(files_aux, tags_obtained, tags2get)

    # 4. Save info
    info_dicom = save_info_dicom(path_patient, files_sel, tags_selected)

    return info_dicom


def get_dicom_slices(info_dicom):
    """
    Using the information saved in the dictionary info_dicom (files, path of files and tags of interest),
    his function finds those dicom files, reads them, sorts them by SliceLocation tag and returns them.

    :param info_dicom: dictionary containing files list as 'list_files', path of files as 'path_patient'
        and tags of interest as 'dict_tags'
    :return:
        slices: dicom files read out
        bool_dicom_loaded: True if dicom files where found and read
    """
    bool_dicom_loaded = False

    # Get slices
    path_patient = info_dicom['path_patient']
    slices = [dicom.read_file(path_patient + '/' + s) for s in info_dicom['list_files']]
    slices.sort(key=lambda x: int(x.SliceLocation))

    # Error check
    if not slices:  # Check # TODO check how can this happen
        print("!!! - There are not dicom slices to load")
    else:
        bool_dicom_loaded = True
    return slices, bool_dicom_loaded


def get_tags_per_block_size(files, path_files, tags_to_get, block_size):
    """
    Reads the provided list of files from the indicated path and extracts the tags specified in tags_to_get.
    To avoid overloading memory, the files are loaded in blocks of files smaller than block_size.

    :param files: list of files names to read
    :param path_files: path where the indicated files are located
    :param tags_to_get: tags that will be retrieved from each dicom file read
    :param block_size: maximum number of dicom files that can be read at once (avoiding memory overload).
    :return:
        files_with_tag: list of files that contained the mentioned tags in tags_to_get
        tags_obtained: dictionary with the tags belonging to each file in file_with_tags
    """
    # Initialize variables
    files_with_tag = []
    tags_obtained = {k: [] for k in tags_to_get}

    # Get the specified tags from all files (files without those tags are discarded)
    num_blocks = int(np.ceil(len(files) / block_size))
    files_blocks = np.array_split(files, num_blocks)
    for block in files_blocks:
        # Get files and tags per block
        this_files, this_tags = get_tags_values(list(block), path_files, tags_to_get)
        # Add files and tags to the ones we already have
        files_with_tag = files_with_tag + this_files
        for k, v in this_tags.items():
            tags_obtained[k] = tags_obtained.get(k) + v
    return files_with_tag, tags_obtained


def get_tags_values(files, path_dicom_patient, tags_str):
    """
    Gets the indicated tag values from the dicom files in the specified path
    :param files: list of files names to read
    :param path_dicom_patient: path where the indicated files are located
    :param tags_str: tags that will be retrieved from each dicom file read
    :return:
        files: list of files that contained the mentioned tags in tags_to_get
        info_tags: dictionary with the tags belonging to each file in file_with_tags
    """
    # Read DICOM files
    if len(files) > 1:
        slices = [dicom.read_file(path_dicom_patient + '/' + s) for s in files]
    else:
        slices = [dicom.read_file(path_dicom_patient + '/' + files)]

    info_tags = {}

    # Check if Tag exits in the slices and returns only the ones where it does
    for tag in tags_str:
        files, slices = check_tag(files, slices, tag)
    # Get tags of interest
    for tag in tags_str:
        aux = [getattr(x, tag) for x in slices]
        if tag == "ImageOrientationPatient":
            aux = [np.array2string(np.abs(np.round(getattr(x, tag)))) for x in slices]
        info_tags[tag] = aux
    return files, info_tags


def check_tag(files, slices, tag):
    """
    Checks if the dicom files contains the tags and returns only the ones that has them.
    :param files: list of name of files corresponding to the slices in slices
    :param slices: list of read dicom slices
    :param tag: tag name to check
    :return:
        files: list of file names where the tag to check exited.
        slices: list of corresponding slices where tag to check exited.
    """
    bool_tag = [True if hasattr(this_slice, tag) else False for this_slice in slices]
    idx2pop = [idx for idx, element in enumerate(bool_tag) if element is False]
    cnt = 0
    for idx in idx2pop:
        slices.pop(idx - cnt)
        files.pop(idx - cnt)
        cnt = cnt + 1
    if cnt > 0:
        print('[checkTag]: Tag ' + tag + ' is missing in ' + str(cnt) + ' items')
    return files, slices


def get_unique_tags_combination(tags, tags_keys):
    """
    Gets the unique tags values from the first element of tags_keys (expected to be 'SeriesDescriptionUID')
    and returns a reduced dictionary of tags values, where the first tag values are unique and are saved
    along with the corresponding values of the other tags specified in tags_keys.

    :param tags: dictionary with values under the keys specified in tags_keys
    :param tags_keys: key string to retrieve values from the dictionary tags
    :returns:
        unique_tags: dictionary with unique values in the first element of the dictionary
        unique_uids: the values saved in the first element of the new dictionary
        uids: the original values saved in the first element of the old dictionary
        idx: position of the elements of unique_uids in uids.
    """
    # Initialize
    unique_tags = {k: [] for k in tags_keys}  # empty initialize
    uids = tags[tags_keys[0]] # get uids in tags

    # Get for each unique UID the other tags_str values
    unique_uid, idxs = np.unique(uids, return_index=True)
    for k, v in tags.items():
        unique_tags[k] = [v[idx] for idx in idxs]

    return unique_tags, unique_uid, uids, idxs


def get_this_uid_files(files, tags, tags_keys):
    """
    Returns the files corresponding to the Series Instance UID selected by the user and values of the tags
    tags_to_get of the selection.

    First, all dicom files in the directory are read to get the Series Instance UIDs.
    Then some other tags (specified in tags_to_get) are retrieved to have more information regarding each S.I.UID
    Finally, one S.I.UID is selected by the user.

    :param files list of files names that have the corresponding tags values in tags
    :param tags: dictionary with the tags belonging to each file in file_with_tags
    :param tags_keys: key names to retrieve information from the dictionary tags

    """
    # Get unique tags
    unique_tags, unique_uid, uids, idxs = get_unique_tags_combination(tags, tags_keys)

    # Ask user which UID is wanted
    options = create_choose_uid_menu_list(unique_tags, len(idxs))
    text_selected, idx_tag_opt = util_gen.choose_from_list(options, 'Choose the UID to use')
    tags_selected = get_tags_selected(unique_tags, idx_tag_opt)
    uid_selected = unique_uid[int(idx_tag_opt)]

    # Get files with that UID
    files_sel = get_files_by_tag(files, uids, uid_selected)
    return files_sel, tags_selected


def replace_iop(str_info, tag):
    """
    If the tag is 'ImageOrientationPatient', it replaces the values by others easier to read.
    """
    if tag is 'ImageOrientationPatient':
        str_info = str_info.replace('[1. 0. 0. 0. 1. 0.]', 'TRA')
        str_info = str_info.replace('[1. 0. 0. 0. 0. 1.]', 'COR')
        str_info = str_info.replace('[0. 1. 0. 0. 0. 1.]', 'SAG')
    return str_info


def get_tags_selected(tags, idx):
    """
    Selects from the dictionary tags the values in the position idx and generates a new dictionary
    only with those values after making some changes to them (see replace_iop)
    """
    tags_selection = {}
    # Get the value and make an string
    for k, v in tags.items():
        val = replace_iop(str(v[idx]), k)
        tags_selection[k] = val
    return tags_selection


def create_choose_uid_menu_list(unique_tags, num_val):
    """
    Create UID option string to show in menu
    """
    options = list()
    # For each different option
    for opt in range(num_val):
        aux = ''
        # Get the tag-value pair and make an string
        for k, v in unique_tags.items():
            value = replace_iop(str(v[opt]), k)
            aux = aux + '[' + str(k) + ' = ' + value + '] '
        options.append(aux)
    return options


def get_files_by_tag(files, values_list, tag_selected):
    """
    Retrieves from files the files with the tag_selected value, that is, the ones located in
    the idx position where values_list is equal to tag_selected.
    values
    """
    bool_opt = [True if uid == tag_selected else False for uid in values_list]
    idx2get = [idx for idx, element in enumerate(bool_opt) if element is True]
    files_selected = [file for idx, file in enumerate(files) if idx in idx2get]
    return files_selected


def save_info_dicom(path_files, files_list, tags):
    info_dicom = dict()
    info_dicom['path_patient'] = path_files
    info_dicom['list_files'] = files_list
    info_dicom['dict_tags'] = tags
    return info_dicom


def read_list_files(path_file):
    """
    Reads the file created in save_list_files
    """
    tags = {}
    f = open(path_file, "r")
    text = f.read()
    aux = text.split('***')
    path_patient = aux[1].replace('\n', '')
    aux_tags = aux[3].replace(' = ', '\n')
    aux_tags = aux_tags.split('\n')
    aux_tags = [tag for tag in aux_tags if tag is not '']
    for i in range(0, len(aux_tags), 2):
        tags[aux_tags[i]] = aux_tags[i+1]
    file_list = aux[5].replace('\n', '')
    file_list = file_list.split('**')
    info_dicom = save_info_dicom(path_patient, file_list, tags)
    return info_dicom


def save_list_files(path, info):
    """
    Saves in the specified path the information inside the dictionary info. The name of the
    file will be determined by the tags values in 'dict_tags' of info.

    :param path: where to save the file
    :param info: dictionary with the dictionary with tags as 'dict_tags', the list of files as
        'list_files' and the path those files as 'path_patient'.
    """
    tags = info['dict_tags']
    files = info['list_files']

    # Create patient path text
    text1 = 'Path patient: \n***\n' + info['path_patient'] + '\n'

    # Create tags text
    text2 = '***\nTags: \n***\n'
    for k, v in tags.items():
        text2 = text2 + k + ' = ' + v + '\n'

    # Create files text
    text3 = '***\nFiles: \n***\n'
    text4 = '**'.join(map(str, files))

    # Create filename and write txt
    filename = create_filename_from_tags(tags, '.txt')
    f = open(os.path.join(path, filename), "w")
    f.write(text1 + text2 + text3 + text4)


def create_filename_from_tags(tags, extension):
    """
    Generates a name from the concatenation of the values in the dictionary tags and the extension.
    Note: add extension with the dot. Ex.: '.txt'
    """
    filename = ''
    cnt = 0
    for k, v in tags.items():
        if cnt == 0:
            filename = str(v)
        else:
            filename = filename + '-' + str(v)
        cnt = cnt + 1
    filename = filename + extension
    return filename