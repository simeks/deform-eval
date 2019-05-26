# Prerequisites

* [deform v0.2](https://github.com/simeks/deform/releases/tag/v0.2)
* [ANTs v2.3.1](https://github.com/ANTsX/ANTs/releases/tag/v2.3.1)
* SimpleITK (e.g. `pip install SimpleITK`)
* Adult atlas (30 subjects, 95 regions) (https://brain-development.org/brain-atlases/adult-brain-atlases/)

# Setup

First configure the environment by setting necessary environment variables. 
```
export DEFORM_EVAL_DATA_PATH <path>
export DEFORM_EVAL_RESULTS_PATH <path>
export ANTS_BIN_PATH <path>
export DEFORM_BIN_PATH <path>
```

| Variable                   | Description                                  |
|----------------------------|----------------------------------------------|
| `DEFORM_EVAL_DATA_PATH`    | Path for storing intermediate imaging data.  |
| `DEFORM_EVAL_RESULTS_PATH` | Path for the outputted results               |
| `ANTS_BIN_PATH`            | Path to the ANTs binaries.                   |
| `DEFORM_BIN_PATH`          | Path to the deform binaries.                 |

Generate intermediate imaging data by first extracting atlas retrieved from https://brain-development.org. Then run the setup script, providing the full path to the extracted `Hammers_mith-n30r95` path: 

```
python run.py setup <Hammers_mith-n30r95/>
```

# Run

To run all labeling experiments simply run
```
python run.py 
```

## nvprof

[nvprof](https://docs.nvidia.com/cuda/profiler-users-guide/index.html) can further assess the performance of deform. This requires deform to be compiled with profiling enabled. See scripts `run_nvprof.py` and `parse_nvprof.py`.

# Results

Results are stored in `DEFORM_EVAL_RESULTS_PATH` (`results/` by default). Provided notebooks can be used to generate figures and tables.

