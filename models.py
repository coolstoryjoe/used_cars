import csv
import pickle
import os
cwd = os.getcwd()

# Write a txt file
def dump_file(obj, file_name):
    with open(str(os.path.join(cwd, 'soup_kitchen', file_name)), 'w') as f:
        f.write(obj)
    return

# write a csv file by row - with first row creating csv file
def dump_csv(myCsvRow, file_name, row_index):
    if row_index == 0:
        with open(str(os.path.join(cwd, 'soup_kitchen', file_name)), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(myCsvRow)
    else:
        with open(str(os.path.join(cwd, 'soup_kitchen', file_name)), 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(myCsvRow)
    return

# write a csv file with a single column
def dump_csv_single_col(myCsvRow, file_name, row_index):
    if row_index == 0:
        with open(str(os.path.join(cwd, 'soup_kitchen', file_name)), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([myCsvRow])
    else:
        with open(str(os.path.join(cwd, 'soup_kitchen', file_name)), 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([myCsvRow])
    return

def save_obj(obj, name):
    with open(str(os.path.join(os.getcwd(), 'pickle_jar', str(name + '.pkl'))), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(str(os.path.join(os.getcwd(), 'pickle_jar', str(name + '.pkl'))), 'rb') as f:
        return pickle.load(f)
