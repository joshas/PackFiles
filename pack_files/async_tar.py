import os
import tarfile
import threading


class AsyncTar(threading.Thread):
    def __init__(self, selected_files, archive_path, mode, callback):
        threading.Thread.__init__(self)
        self.selected_files = selected_files
        self.archive_path = archive_path
        self.mode = mode
        self.callback = callback

    def run(self):
        tar = tarfile.open(self.archive_path, self.mode)
        for file in self.selected_files:
            tar.add(file, os.path.basename(file))
        tar.close()
        self.callback()
