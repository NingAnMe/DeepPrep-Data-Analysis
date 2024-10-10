# DeepPrep-Data-Analysis

## denoise
The code in **denoise** dir is for DeepPrep version >= **24.0.0** result.

## processing steps
Surface space： bandpass -> regression -> smooth(optional)

Volume space：  bandpass -> regression -> smooth(optional)

.

├── sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_bold.nii.gz

├── sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_desc-bandpass_bold.json

├── sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_desc-bandpass_bold.nii.gz

├── sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_desc-fwhm_bold.json

├── sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_desc-fwhm_bold.nii.gz

├── sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_desc-regression_bold.json

├── sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_desc-regression_bold.nii.gz

├── sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-bandpass_bold.json

├── sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-bandpass_bold.nii.gz

├── sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-fwhm_bold.json

├── sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-fwhm_bold.nii.gz

├── sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-regression_bold.json

└── sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-regression_bold.nii.gz

## Install (Docker)

for CN
```shell
docker pull registry.cn-beijing.aliyuncs.com/pbfslab/deepprep:postproc24.0.1
```

Usage:
```shell
$ docker run -it --rm --user $(id -u):$(id -g) \
-v /mnt:/mnt -v $FREESURFER_HOME:/opt/freesurfer \
pbfslab/deepprep:postproc24.0.1 --help

usage: [-h] --bold_preprocess_dir BOLD_PREPROCESS_DIR --bold_preproc_file BOLD_PREPROC_FILE [--repetition_time REPETITION_TIME] [--freesurfer_home FREESURFER_HOME] [--subjects_dir SUBJECTS_DIR]
                       --bold_denoise_dir BOLD_DENOISE_DIR

DeepPrep: denise

options:
  -h, --help            show this help message and exit
  --bold_preprocess_dir BOLD_PREPROCESS_DIR
                        DeepPrep preprocessed BOLD dir
  --bold_preproc_file BOLD_PREPROC_FILE
                        preprocessed BOLD file json
  --repetition_time REPETITION_TIME
                        RepetitionTime of BOLD file (optional)
  --freesurfer_home FREESURFER_HOME
                        freesurfer home path (optional)
  --subjects_dir SUBJECTS_DIR
                        DeepPrep Recon dir is required if the space of BOLD is fsnative (optional)
  --skip_frame SKIP_FRAME
                        how many frames to skip before postprocessing? (optional)
  --fwhm FWHM           (INT) using to smoothing file with fwhm (optional)
  --bold_denoise_dir BOLD_DENOISE_DIR
                        denoised dir path
```

run example:
```shell

# Surface space
# bandpass -> regression -> smooth fwhm-6

$ docker run -it --rm --user $(id -u):$(id -g) \
    -v /mnt:/mnt -v $FREESURFER_HOME:/opt/freesurfer \
    pbfslab/deepprep:postproc24.0.1 \
    --freesurfer_home /opt/freesurfer \
    --bold_preprocess_dir /mnt/ngshare/DeepPrep/FastSurferUpdate/Result/MSC_recon-DP242x_preproc-DP242x/BOLD \
    --bold_preproc_file /mnt/ngshare/DeepPrep/FastSurferUpdate/Result/MSC_recon-DP242x_preproc-DP242x/BOLD/sub-MSC01/ses-func01/func/sub-MSC01_ses-func01_task-rest_hemi-L_space-fsaverage6_bold.func.gii \
    --bold_denoise_dir /mnt/ngshare/DeepPrep/FastSurferUpdate/Result/MSC_recon-DP242x_preproc-DP242x_postproc-pbfslab \
    --skip_frame 2 \
    --fwhm 6

# Volume space
# bandpass -> regression

$ docker run -it --rm --user $(id -u):$(id -g) \
    -v /mnt:/mnt -v $FREESURFER_HOME:/opt/freesurfer \
    pbfslab/deepprep:postproc24.0.1 \
    --freesurfer_home /opt/freesurfer \
    --bold_preprocess_dir /mnt/ngshare/DeepPrep/FastSurferUpdate/Result/MSC_recon-DP242x_preproc-DP242x/BOLD \
    --bold_preproc_file /mnt/ngshare/DeepPrep/FastSurferUpdate/Result/MSC_recon-DP242x_preproc-DP242x/BOLD/sub-MSC01/ses-func01/func/sub-MSC01_ses-func01_task-rest_space-MNI152NLin6Asym_res-02_desc-preproc_bold.nii.gz \
    --bold_denoise_dir /mnt/ngshare/DeepPrep/FastSurferUpdate/Result/MSC_recon-DP242x_preproc-DP242x_postproc-pbfslab \
    --skip_frame 2 \
    --fwhm 6
```
