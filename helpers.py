import os
from consts import ROOT_DIR, DIRECTORY_TO_SAVE_CSV
from datetime import datetime

def getFileName(officeName):
    return os.path.join(ROOT_DIR,DIRECTORY_TO_SAVE_CSV,officeName,
                        os.path.basename(officeName + '_' + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + '.csv'))
