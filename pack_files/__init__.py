import os
# noinspection PyUnresolvedReferences
from fman import DirectoryPaneCommand, show_status_message, clear_status_message
# noinspection PyUnresolvedReferences
from fman.util.qt import run_in_main_thread
from pack_files.pack_dialog import PackDialog
from pack_files.async_zip import AsyncZip
from pack_files.async_tar import AsyncTar


class PackFiles(DirectoryPaneCommand):
    # on success clear selection and reset message in status bar
    def success(self):
        self.pane.clear_selection()
        clear_status_message()

    # create name for archive from file name
    @staticmethod
    def get_file_name(selected_file):
        basename = os.path.basename(selected_file)
        if os.path.isfile(selected_file):
            return os.path.splitext(basename)[0]
        else:
            return basename

    @run_in_main_thread
    def __call__(self):

        # check if multiple files were selected
        selected_files = self.pane.get_selected_files()

        if not selected_files:
            # if no files were selected, get the one under cursor
            selected_file = self.pane.get_file_under_cursor()
            selected_files = [selected_file]
            # select file
            self.pane.toggle_selection(selected_file)
            # get archive filename - selected file name without extension or directory name
            archive_name = self.get_file_name(selected_file)
        else:
            first_file = selected_files[0]
            if len(selected_files) > 1:
                # get archive filename - parent directory name
                archive_name = os.path.basename(os.path.dirname(first_file))
            else:
                # if only one file selected - archive name is its name
                archive_name = self.get_file_name(first_file)

        # if somehow no files were selected - return
        if not selected_files:
            return

        if not archive_name:
            archive_name = "pack"

        # get target path
        panes = self.pane.window.get_panes()
        target_pane = panes[(panes.index(self.pane) + 1) % len(panes)]
        target_path = target_pane.get_path()

        # display options dialog, wait for results
        archive_path, packer_type, result = PackDialog.get_packer_options(len(selected_files),
                                                                          os.path.join(target_path, archive_name))

        if result:
            show_status_message("Packing files...")

            # call function with options for packing
            if packer_type == ".tar":
                background_thread = AsyncTar(selected_files, archive_path, 'x', self.success)
            elif packer_type == ".tar.gz":
                background_thread = AsyncTar(selected_files, archive_path, 'x:gz', self.success)
            elif packer_type == ".tar.bz2":
                background_thread = AsyncTar(selected_files, archive_path, 'x:bz2', self.success)
            elif packer_type == ".tar.xz":
                background_thread = AsyncTar(selected_files, archive_path, 'x:xz', self.success)
            else:
                background_thread = AsyncZip(selected_files, archive_path, self.success)

            # pack in background thread
            background_thread.start()
