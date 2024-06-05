# DeepPrep-Data-Analysis

## denoise
The code in **denoise** dir is for DeepPrep **23.1.0** result.

Software dependence:
1. FreeSurfer >= 6.0.0
2. Python >= 3.10

Install Python dependence:
$ pip install bids numpy nibabel

```shell
usage: bold_denoise.py [-h] --bold_preprocess_dir BOLD_PREPROCESS_DIR --bold_preproc_file BOLD_PREPROC_FILE --bold_denoise_dir BOLD_DENOISE_DIR [--freesurfer_home FREESURFER_HOME] [--subjects_dir SUBJECTS_DIR]

DeepPrep: denise

options:
  -h, --help            show this help message and exit
  --bold_preprocess_dir BOLD_PREPROCESS_DIR
                        DeepPrep BOLD result dir
  --bold_preproc_file BOLD_PREPROC_FILE
                        DeepPrep preprocessed BOLD file path
  --bold_denoise_dir BOLD_DENOISE_DIR
                        denoised BOLD file path
  --freesurfer_home FREESURFER_HOME
                        freesurfer home path (optional)
  --subjects_dir SUBJECTS_DIR
                        DeepPrep Recon dir is required if space of BOLD is fsnative (optional)
```

run example:
```python
$ cd denoise

$ python3 bold_denoise.py --bold_preprocess_dir /DeepPrep_2310_Result/BOLD \
    --bold_preproc_file /DeepPrep_2310_Result/BOLD/sub-MSC01/ses-func01/func/sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-preproc_bold.nii.gz \
    --bold_denoise_dir /mnt/ngshare2/anning/workspace/DeepPrep-Data-Analysis/tmp/bold_denised_dir

$ python3 bold_denoise.py --bold_preprocess_dir /DeepPrep_2310_Result/BOLD \
    --bold_preproc_file /DeepPrep_2310_Result/BOLD/sub-MSC01/ses-func01/func/sub-MSC01_ses-func01_task-rest_space-T1w_desc-preproc_bold.nii.gz \
    --bold_denoise_dir /mnt/ngshare2/anning/workspace/DeepPrep-Data-Analysis/tmp/bold_denised_dir
```
