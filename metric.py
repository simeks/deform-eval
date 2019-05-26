import os, shutil, subprocess, platform

import numpy as np, SimpleITK as sitk

bin_dir = '/home/simon/proj/ANTs/build/bin/'
if 'ANTS_BIN_PATH' in os.environ:
    bin_dir = os.environ['ANTS_BIN_PATH']

label_overlap_measures = os.path.join(bin_dir, 'LabelOverlapMeasures')

def measure_overlap_itk(src, tgt, csv_out):
    # New build of LabelOverlapMeasures does not seem work (crashes)
    args = [label_overlap_measures, '3', src, tgt, '1']
    with open(csv_out, 'w') as f:
        proc = subprocess.Popen(args, stdout=f)
        proc.wait()

def dsc(src, tgt):
    return 2*np.logical_and(src, tgt).sum()/(src.sum() + tgt.sum())

def measure_overlap(src, tgt, csv_out):
    src = sitk.GetArrayFromImage(sitk.ReadImage(src))
    tgt = sitk.GetArrayFromImage(sitk.ReadImage(tgt))
    
    with open(csv_out, 'w') as f:
        f.write('Label,Dice\n')

        src_all = src != 0
        tgt_all = tgt != 0
        dsc_all = dsc(src_all, tgt_all)

        f.write('All,{}\n'.format(dsc_all))

        for i in range(1, 96):
            src_i = src == i
            tgt_i = tgt == i
            dsc_i = dsc(src_i, tgt_i)

            f.write('{},{}\n'.format(i, dsc_i))

def njac(df):
    img = sitk.ReadImage(df)
    jac = sitk.DisplacementFieldJacobianDeterminant(img)
    jd = sitk.GetArrayFromImage(jac)
    jd = jd < 0
    return jd.sum()

