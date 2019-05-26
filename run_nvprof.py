import subprocess
import data

deform_exe = 'bin/deform_profile'

fixed = data.image_file('a16')
moving = data.image_file('a12')

def run_nvprof(gpu):
    subprocess.check_call([
        'nvprof',
        '--log-file', 'nvprof_{}.txt'.format('gpu' if gpu else 'cpu'),
        '--csv',
        deform_exe, 'registration',
        '-p', 'config_df_{}.yml'.format('gpu' if gpu else 'cpu'),
        '-f0', fixed,
        '-m0', moving,
        '--gpu' if gpu else ''
    ])

run_nvprof(True)
run_nvprof(False)

