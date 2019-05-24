import os, shutil, subprocess, platform

bin_dir = '/home/simon/proj/ANTs/build/bin/'
if 'ANTS_BIN_PATH' in os.environ:
    bin_dir = os.environ['ANTS_BIN_PATH']

# New build of LabelOverlapMeasures does not work for some reason
label_overlap_measures = os.path.join(bin_dir, 'LabelOverlapMeasures')

def measure_overlap(src, tgt, csv_out):
    args = [label_overlap_measures, '3', src, tgt, '1']
    with open(csv_out, 'w') as f:
        proc = subprocess.Popen(args, stdout=f)
        proc.wait()
