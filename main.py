""" adichtmat_export_blocks_by_tok with file selector"""
import sys
from PySide6.QtWidgets import QApplication,QFileDialog
from adichtmat_export_blocks_by_tok import adichtmat_export_blocks_by_tok

def filepicker()->str:
    # File picker with filters
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select an Image",
        "",
        "ADICHTMAT Mat File (*.mat);;All Files (*)"
    )
    return file_path
    
def main():
    QApplication(sys.argv)
    file_path = filepicker()
    if file_path:
        adichtmat_export_blocks_by_tok(file_path)
        print('adichtmat export done.')
    else:
        print('export aborted.')    

if __name__ == "__main__":
    main()
