# PackFiles
[fman](https://fman.io) plugin for packing (archiving) files. Supported formats: zip, tar, tar.gz, tar.bz2 and tar.xz.

## Installation
Download and extract it to fman Plugins directory, restart fman. Or use fman [plugin installer](https://fman.io/docs/installing-plugins).

## Usage
* <kbd>Alt+F5</kbd> - add selected files (or file under cursor) to archive, archive will be stored in target pane directory.

## TODO
- [ ] Add path input validation, exception catching and error display, prevent file overwriting and permissions issues
- [ ] Visual packing progress display
- [ ] Add options: compression level selection, encryption, recursive packing, splitting archives
- [ ] Custom archives support using command line programs: use config json to store entries, add GUI later
- [ ] Do not display taskbar icon for dialog window (set mainWindow as parent for dialog)
