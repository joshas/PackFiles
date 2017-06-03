from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class PackDialog(QDialog):
    def __init__(self, file_count, target_file, parent=None):
        super().__init__()
        self.file_count = file_count
        self.target_file = target_file
        self.packer_types = [".zip", ".tar", ".tar.gz", ".tar.bz2", ".tar.xz"]
        self.packer_type = self.packer_types[0]

        self.resize(440, 120)
        self.setFixedSize(self.size())
        self.setWindowTitle('Pack files')
        self.setModal(True)
        # hide question mark icon in titlebar on Windows
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # setup GUI elements
        self.label = QLabel("Pack {} file(s) to archive".format(self.file_count))
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum))

        self.line_edit = QLineEdit()
        self.line_edit.setText(self.target_file + self.packer_type)
        self.line_edit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

        self.combo_box = QComboBox()
        self.combo_box.setEnabled(True)
        self.combo_box.addItems(self.packer_types)
        self.combo_box.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.combo_box.activated[str].connect(self.on_combo_box_change)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)
        h_layout.addWidget(self.line_edit)
        h_layout.addWidget(self.combo_box)

        v_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.label)
        v_layout.addItem(h_layout)
        v_layout.addItem(v_spacer)
        v_layout.addWidget(self.button_box)
        self.setLayout(v_layout)

        self.show()

    # replace archive extension on combobox selection change
    def on_combo_box_change(self, text):
        # need to start with longest file extensions first, to prevent leaving .tar suffix
        packer_types_sorted = self.packer_types
        packer_types_sorted.sort(key=len, reverse=True)  # sort strings to begin with longest
        path = self.line_edit.text()
        for packer_type in packer_types_sorted:
            if path.endswith(packer_type):
                path = path[:-len(packer_type)]
        # display new value, store packer_type selection
        self.line_edit.setText(path + text)
        self.packer_type = text

    def get_archive_path(self):
        return self.line_edit.text()

    def get_packer_type(self):
        return self.packer_type

    @staticmethod
    def get_packer_options(file_count, target_file, parent=None):
        dialog = PackDialog(file_count, target_file, parent)
        result = dialog.exec_()
        return dialog.get_archive_path(), dialog.get_packer_type(), result == QDialog.Accepted
