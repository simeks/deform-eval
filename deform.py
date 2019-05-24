import os, shutil, subprocess, platform, yaml

bin_dir = 'bin'
if 'DEFORM_BIN_PATH' in os.environ:
    bin_dir = os.environ['DEFORM_BIN_PATH']

deform_exe = os.path.join(bin_dir, 'deform')

def write_config(out_file, params):
    with open(out_file, 'w') as f:
        yaml.dump(params, f)
        
def register(fixed_file, moving_file, param_file, silent=False, d0=None, num_threads=None, stdout=subprocess.DEVNULL, exe=None, use_gpu=False):
    if exe is None:
        args = [deform_exe]
    else:
        args = [exe]

    args.extend(['registration', '-t', '-j', '-p', param_file, '-f0', fixed_file, '-m0', moving_file])
    if d0 is not None:
        args.extend(['-d0', d0])
    if num_threads is not None:
        args.extend(['--num-threads', str(num_threads)])
    if use_gpu:
        args.extend(['--gpu'])

    proc = subprocess.Popen(args, stderr=stdout)
    proc.wait()
    
    if proc.returncode != 0:
        raise RuntimeError('Subprocess returned {}, something went wrong?'.format(proc.returncode))

def transform(src_file, def_file, out_file, nn = False, silent=False, exe=None):
    if exe is None:
        args = [deform_exe]
    else:
        args = [exe]

    args.extend(['transform', src_file, def_file, out_file])
    
    if nn:
        args.extend(['-i', 'nn'])
        
    if silent:
        proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc = subprocess.Popen(args)

    proc.wait()
    
    if proc.returncode != 0:
        raise RuntimeError('Subprocess returned {}, something went wrong?'.format(proc.returncode))

