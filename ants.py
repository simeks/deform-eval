import os, shutil, subprocess


bin_dir = '/home/simon/proj/ANTs/build/bin/'
if 'ANTS_BIN_PATH' in os.environ:
    bin_dir = os.environ['ANTS_BIN_PATH']

ants_exe = os.path.join(bin_dir, 'antsRegistrationSyN.sh')
transform_exe = os.path.join(bin_dir, 'antsApplyTransforms')



# Compulsory arguments:
#     -d:  ImageDimension: 2 or 3 (for 2 or 3 dimensional registration of single volume)
#     -f:  Fixed image or source image or reference image
#     -m:  Moving image or target image
#     -o:  OutputPrefix: A prefix that is prepended to all output files.

# Optional arguments:
#     -n:  Number of threads (default = 1)



def ants_registration_syn(fixed_file, moving_file, output, stdout):
    os.environ['ANTSPATH']=bin_dir

    args = [
        ants_exe,
        '-d', '3',
        '-f', fixed_file,
        '-m', moving_file,
        '-o', output,
        '-n', '12'
    ]
    
    proc = subprocess.Popen(args, stdout=stdout)
    proc.wait()

    if proc.returncode != 0:
        raise RuntimeError('Subprocess returned {}, something went wrong?'.format(proc.returncode))

def transform(fixed_file, src_file, output, transforms):
    args = [
        transform_exe,
        '-d', '3',
        '-i', src_file,
        '-o', output,
        '-r', fixed_file,
        '-n', 'NearestNeighbor' 
    ]

    for t in transforms:
        args.extend(['-t', t])

    proc = subprocess.Popen(args)
    proc.wait()
    
    if proc.returncode != 0:
        raise RuntimeError('Subprocess returned {}, something went wrong?'.format(proc.returncode))

def register(fixed_file, moving_file, output, stdout):
    ants_registration_syn(fixed_file, moving_file, output, stdout)

def convert_affine(ref, t, out):
    """ Converts an affine matrix to a displacement field """
    args = [
        transform_exe,
        '-d', '3',
        '-r', ref,
        '-t', '[{},0]'.format(t),
        '-o', '[{},1]'.format(out),
        '--float'
    ]
    subprocess.check_call(args)