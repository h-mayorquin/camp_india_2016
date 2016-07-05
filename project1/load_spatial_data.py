from __future__ import print_function
import openpyxl
import scipy.io as sio

from functions_extract_database import view_trial

folder = './database/'
filename = 'SummaryDatabase'
format_type = '.xlsx'


wb = openpyxl.load_workbook(folder + filename + format_type)

pre_spatial_set = wb.get_sheet_by_name('Pre_SpatialSet')
post_spatial_set = wb.get_sheet_by_name('Post_SpatialSet')

file_names = []
for file_name, neuron in zip(pre_spatial_set.columns[0], pre_spatial_set.columns[1]):
    open_string = file_name.value + '_' + str(neuron.value)
    file_names.append(open_string)