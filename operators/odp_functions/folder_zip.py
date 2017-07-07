import os
import ntpath
import zipfile

def folder_zip(output_path, folder_paths=[], file_paths=[]):
    """
    Zip files and folders into a zip folder
    """
    
    zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
    
    if len(folder_paths) > 0:
        for folder in folder_paths:
            
            parent_folder = ntpath.basename(folder)
            garbage = folder.replace(parent_folder, '')
        
            contents = os.walk(folder)
            
            for root, fs, files in contents:
                for file_name in files:
                    absolute_path = os.path.join(root, file_name)
                    relative_path = absolute_path.replace(garbage, '')
                    zip_file.write(absolute_path, relative_path)
    
    for f in file_paths:
        zip_file.write(f, ntpath.basename(f))
    
    zip_file.close()
