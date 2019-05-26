import os, random, shutil, sys, time
import ants, data, deform, metric 

results_path = 'results'

if not os.path.isdir(results_path):
    os.mkdir(results_path)

deform_config = {
    'pyramid_levels': 3,
    'pyramid_stop_level': 0,

    'block_size': [16, 16, 16],
    'block_energy_epsilon': 0.00000001,
    'max_iteration_count': 200,

    'step_size': 0.1,
    'regularization_weight': 0.3,
    'regularization_scale': 7,
    'regularization_exponent': 7,

    'levels': {
        '0': {'max_iteration_count':20},
        '1': {'max_iteration_count':40}
    },

    'image_slots': [
        {
            'resampler': 'gaussian',
            'normalize': False,
            'cost_function': [
                {
                    'function': 'ncc',
                    'radius': 2
                }
            ]
        }
    ]
}

def measure_njac(result_path):
    with open(os.path.join(result_path, 'njac.csv'), 'w') as f:
        f.write('fixed,moving,njac\n')
        for p in data.get_pairs():
            df = os.path.join(result_path, '{}_{}_result_def.vtk'.format(*p))
            if not os.path.isfile(df):
                df = os.path.join(result_path, '{}_{}_result_1Warp.nii.gz'.format(*p))

            njac = metric.njac(df)
            f.write('{},{},{}\n'.format(p[0], p[1], njac))

def run_deform(test_name, cfg, use_gpu):
    test_results_path = os.path.join(results_path, test_name)
    if not os.path.isdir(test_results_path):
        os.mkdir(test_results_path)

    cfg_file = 'config_'+test_name+'.yml'
    deform.write_config(cfg_file, cfg)

    pairs = data.get_pairs()

    for p in pairs:
        print(p)

        f = data.image_file(p[0])
        m = data.image_file(p[1])
        d0 = data.affine_file(p)

        log_file = os.path.join(test_results_path, '{}_{}_log.txt'.format(p[0], p[1]))
        with open(log_file, 'w') as lf:
            start = time.time()
            deform.register(f, m, cfg_file, d0=d0, stdout=lf, use_gpu=use_gpu)
            stop = time.time()
            lf.write('\nTime elapsed: {}\n'.format(stop-start))

        deform.transform(data.segmentation_file(p[1]), 'result_def.vtk', 
            os.path.join(test_results_path, '{}_{}_segm.vtk'.format(p[0], p[1])), True)
        
        shutil.move('result_def.vtk', os.path.join(test_results_path, '{}_{}_result_def.vtk'.format(p[0], p[1])))
        shutil.move('result.vtk', os.path.join(test_results_path, '{}_{}_t1.vtk'.format(p[0], p[1])))

        metric_file = os.path.join(test_results_path, '{}_{}.csv'.format(p[0], p[1]))
        metric.measure_overlap(
            data.segmentation_file(p[0]),
            os.path.join(test_results_path, '{}_{}_segm.vtk'.format(p[0], p[1])),
            metric_file)

    measure_njac(test_results_path)


def run_ants():
    ants_results_path = os.path.join(results_path, 'ants')
    if not os.path.isdir(ants_results_path):
        os.mkdir(ants_results_path)
        
    pairs = data.get_pairs()

    for p in pairs:
        print(p)

        f = data.image_file(p[0])
        m = data.image_file(p[1])

        log_file = os.path.join(ants_results_path, '{}_{}_log.txt'.format(p[0], p[1]))
        with open(log_file, 'w') as lf:
            start = time.time()
            ants.register(f, m, 'ants_result_', stdout=lf)
            stop = time.time()
            lf.write('\nTime elapsed: {}\n'.format(stop-start))
        
        t = [
            'ants_result_1Warp.nii.gz',
            'ants_result_0GenericAffine.mat'
        ]

        ants.transform(data.image_file(p[0]), data.segmentation_file(p[1]), 
            os.path.join(ants_results_path, '{}_{}_segm.vtk'.format(p[0], p[1])), t)

        shutil.move('ants_result_0GenericAffine.mat', os.path.join(ants_results_path, '{}_{}_result_0GenericAffine.mat'.format(p[0], p[1])))
        shutil.move('ants_result_1Warp.nii.gz', os.path.join(ants_results_path, '{}_{}_result_1Warp.nii.gz'.format(p[0], p[1])))
        shutil.move('ants_result_Warped.nii.gz', os.path.join(ants_results_path, '{}_{}_t1.nii.gz'.format(p[0], p[1])))

        metric_file = os.path.join(ants_results_path, '{}_{}.csv'.format(p[0], p[1]))
        metric.measure_overlap(
            data.segmentation_file(p[0]),
            os.path.join(ants_results_path, '{}_{}_segm.vtk'.format(p[0], p[1])),
            metric_file)

        # Convert affine transformation to displacement field

        ants.convert_affine(
            data.image_file(p[0]),
            os.path.join(ants_results_path, '{}_{}_result_0GenericAffine.mat'.format(p[0], p[1])),
            data.affine_file(p)
        )

    measure_njac(ants_results_path)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'setup':
            data.setup(sys.argv[2])
        elif sys.argv[1] == 'ants':
            run_ants()
        elif sys.argv[1] == 'df_gpu':
            run_deform('df_gpu', deform_config, True)
        elif sys.argv[1] == 'df_cpu':
            run_deform('df_cpu', deform_config, False)
    else:
        # Run everything
        print('ANTs')
        run_ants()
        print('df_gpu') 
        run_deform('df_gpu', deform_config, True)
        print('df_cpu')
        run_deform('df_cpu', deform_config, False)




