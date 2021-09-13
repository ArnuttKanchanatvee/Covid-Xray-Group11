#%%

import os
import cv2
import glob
import pydicom
from pydicom.pixel_data_handlers import apply_modality_lut, apply_voi_lut
import numpy as np
import pandas as pd
# %%
"""Helper functions"""
def _extract_data(df_row):
    return df_row['Anon MRN'], df_row['Anon TCIA Study Date'], df_row['Anon Exam Description'], df_row['Anon Study UID']


def load_ricord_metadata(ricord_meta_file):
    df = pd.read_excel(ricord_meta_file, sheet_name='CR Pos - TCIA Submission')
    ricord_metadata = []
    for index, row in df.iterrows():
        ricord_metadata.append(_extract_data(row))
    return ricord_metadata

def make_ricord_dict(ricord_data_set_file):
    """Loads bboxes from the given text file"""
    ricord_dict = {}
    with open(ricord_data_set_file, 'r') as f:
        for line in f.readlines():
            # Values after file name are crop dimensions
            if(len(line.split()) > 1):
                fname, xmin, ymin, xmax, ymax = line.rstrip('\n').split()
                bbox = tuple(int(c) for c in (xmin, ymin, xmax, ymax))
                ricord_dict[fname] = bbox
            else:
                fname = line.rstrip('\n')
                ricord_dict[fname] = None
                
    return ricord_dict
# %%
