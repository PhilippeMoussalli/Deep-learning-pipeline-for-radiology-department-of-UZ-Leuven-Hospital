import os


def create_folder_in_dir(folder_name, working_dir = os.getcwd()):
    """
    Creates a folder with the provided name in the provided directory if it does not exist yet
    and returns the path of the folder directory either way.
    If no directory is specified, chooses the python working directory.
    """
    # Create path folder
    path_folder = os.path.join(working_dir, folder_name)

    # Create folder if it does not exit
    if os.path.isdir(path_folder) is False:
        os.mkdir(path_folder)

    return path_folder


def get_file_from_folder_x_in_working_dir(folder_name):
    """
    If the folder exit in the working directory, retrieves files inside folder, lets user
    choose a file and returns its path. If not, returns book_ok as False.
    """
    # Initialization and create path folder
    bool_ok = True
    working_dir = os.getcwd()
    # If exits, get files list inside and let user choose one
    path_folder = os.path.join(working_dir, folder_name)
    if os.path.isdir(path_folder) is True:
        files = os.listdir(path_folder)
        file, option_sel = choose_from_list(files, 'Choose the info txt file to use')
        path_file = os.path.join(path_folder, file)
    else:
        path_file = ""
        bool_ok = False
        print("\n!!! - There is not a folder with txt information")
    return path_file, bool_ok


def get_files_by_choosing_folder(path_dir):
    """
    Returns all the files inside the folder the user choose and their path. This folder will be inside
    the specified path_dir.
    """
    # Choose folder
    folders_dir = os.listdir(path_dir)
    dir_selected, idxsel = choose_from_list(folders_dir, "Choose the folder to work with")

    # Get files
    path_selected = os.path.join(path_dir, dir_selected)  # TODO select patient
    files_folder = os.listdir(path_selected)

    return files_folder, path_selected


def choose_from_list(list_str, text):
    """
    Generates a menu so the user can choose one of the elements in the list list_str. Returns the selected
    element and its index.
    """
    print()
    print(text)
    idx = 0
    # Print menu
    for item in list_str:
        print("[" + str(idx) + "] " + item)
        idx = idx + 1
    # Get selection input and retrieve element
    option_sel = input("Number selected: ")
    item_sel = list_str[int(option_sel)]
    return item_sel, int(option_sel)


def menu_main():
    print()
    print("What do you want to do?")
    print("[0] Load Dicom files")
    print("[1] Load Nifti files")
    print("[2] Convert Dicom to Nifti")
    print("[3] Visualize Dicom files")
    print("[4] Visualize Nifti files")
    print("[5] Visualize and compare Dicom and Nifti files")
    print("[6] Resample nifti file")
    opt_main = input("Choose (q to quit): ")
    return opt_main


def menu_dicom():
    print()
    print("What do you want to do?")
    print("[0] Read all Dicom files from a directory")
    print("[1] Select the txt with the Dicom files to read")
    opt_dicom = input("Choose (b to go back and q to quit): ")
    return opt_dicom

