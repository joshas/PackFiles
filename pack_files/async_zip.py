import os
import zipfile
import threading


class AsyncZip(threading.Thread):
    def __init__(self, selected_files, archive_path, callback):
        threading.Thread.__init__(self)
        self.selected_files = selected_files
        self.archive_path = archive_path
        self.callback = callback

    def run(self):
        zip_file = zipfile.ZipFile(self.archive_path, 'w', zipfile.ZIP_DEFLATED)

        for single_file in self.selected_files:
            # pack single file
            if os.path.isfile(single_file):
                zip_file.write(single_file,
                               os.path.basename(single_file))  # single file is written to top dir without path
            # pack directory and its contents recursively
            else:
                base_dir = os.path.dirname(single_file)  # base directory that should not be in zipped files paths
                for root, dirs, files in os.walk(single_file):
                    # pack files
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, base_dir))
                    # pack directories
                    for directory in dirs:
                        dir_path = os.path.join(root, directory)
                        zip_file.write(dir_path, os.path.relpath(dir_path, base_dir))
                    # pack empty root directory
                    zip_file.write(root, os.path.relpath(root, base_dir))

        zip_file.close()
        self.callback()
