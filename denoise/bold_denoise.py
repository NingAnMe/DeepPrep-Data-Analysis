#! /usr/bin/env python3
import os
import argparse
from bids import BIDSLayout
from pathlib import Path

from filters.filters import bandpass_nifti
from regressors.regressors import glm_nifti


def set_environ(freesurfer_home, subjects_dir):
    # FreeSurfer recon-all env
    os.environ['FREESURFER_HOME'] = freesurfer_home
    if subjects_dir:
        os.environ['SUBJECTS_DIR'] = subjects_dir
    else:
        os.environ['SUBJECTS_DIR'] = f'{freesurfer_home}/subjects'
    os.environ['PATH'] = f'{freesurfer_home}/bin:{freesurfer_home}/mni/bin:{freesurfer_home}/tktools:' + \
                         f'{freesurfer_home}/fsfast/bin:' + os.environ['PATH']
    os.environ['MINC_BIN_DIR'] = f'{freesurfer_home}/mni/bin'
    os.environ['MINC_LIB_DIR'] = f'{freesurfer_home}/mni/lib'
    os.environ['PERL5LIB'] = f'{freesurfer_home}/mni/share/perl5'
    os.environ['MNI_PERL5LIB'] = f'{freesurfer_home}/mni/share/perl5'
    # FreeSurfer fsfast env
    os.environ['FSF_OUTPUT_FORMAT'] = 'nii.gz'
    os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ'


def fsaverage6_sm6(input_path, output_path, hemi):
    cmd = ' '.join([
                    'mri_surf2surf',
                    '--hemi', hemi,
                    '--s', 'fsaverage6',
                    '--sval', input_path,
                    '--label-src', hemi + '.cortex.label',
                    '--fwhm-trg', '6',
                    '--tval', output_path,
                    '--reshape'
                    ])
    print(f'run: {cmd}')
    os.system(cmd)
    assert os.path.exists(output_path)
    print(f'>>> {output_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="DeepPrep: denise"
    )

    # input
    parser.add_argument("--bold_preprocess_dir", required=True, help="DeepPrep BOLD result dir")
    parser.add_argument("--bold_preproc_file", required=True, help="DeepPrep preprocessed BOLD file path")
    # output
    parser.add_argument("--bold_denoise_dir", required=True, help="denoised BOLD file path")
    parser.add_argument("--freesurfer_home", required=False, help="freesurfer home path (optional)")
    parser.add_argument("--subjects_dir", required=False, help="DeepPrep Recon dir is required if space of BOLD is fsnative (optional)")
    args = parser.parse_args()

    assert os.environ.get('FREESURFER_HOME', None), "FREESURFER_HOME environment variable not set, please add --freesurfer_home /path/to/freesurfer"
    if args.freesurfer_home:
        set_environ(os.path.join(args.freesurfer_home), args.subjects_dir)

    assert os.path.isdir(args.bold_preprocess_dir)
    assert os.path.isfile(args.bold_preproc_file)
    assert args.bold_preproc_file.startswith(args.bold_preprocess_dir)

    layout_pre = BIDSLayout(args.bold_preprocess_dir, validate=False)
    TR = layout_pre.get_metadata(args.bold_preproc_file)['RepetitionTime']
    entities = layout_pre.parse_file_entities(args.bold_preproc_file)

    bold_preprocess_entities = {'extension': entities.get('extension'),
                                'space': entities.get('space')}
    for entity in ['subject', 'session', 'run', 'task', 'preproc', 'res', 'hemi']:
        if entities.get(entity, None):
            bold_preprocess_entities[entity] = entities.get(entity)
    bold_preprocess_file = layout_pre.get(**bold_preprocess_entities)[0]

    confounds_entities = {'desc': 'confounds'}
    for entity in ['subject', 'session', 'run', 'task']:
        if entities.get(entity, None):
            confounds_entities[entity] = entities.get(entity)
    confounds_file = layout_pre.get(**confounds_entities)[0]

    # output
    output_dir = os.path.join(args.bold_denoise_dir, os.path.dirname(bold_preprocess_file.relpath))
    os.makedirs(output_dir, exist_ok=True)

    if entities['extension'] == '.func.gii':
        # output
        nii_file = os.path.join(output_dir, bold_preprocess_file.filename.replace('func.gii', 'nii.gz'))
        nii_file_name = os.path.basename(nii_file)
        bandpass_file = os.path.join(output_dir, nii_file_name.replace(f'_bold', f'_desc-bandpass_bold'))
        regression_file = os.path.join(output_dir, nii_file_name.replace(f'_bold', f'_desc-regression_bold'))
        sm6_file = os.path.join(output_dir, nii_file_name.replace(f'_bold', f'_desc-postproc_bold'))

        def to_nii(_in_file, _output_file):
            _cmd = f'mri_convert {_in_file} {_output_file}'
            os.system(_cmd)

        to_nii(bold_preprocess_file.path, nii_file)
        assert os.path.exists(nii_file)
        bandpass_nifti(nii_file, bandpass_file, TR)
        assert os.path.exists(bandpass_file)
        glm_nifti(bandpass_file, regression_file, Path(confounds_file))
        assert os.path.exists(regression_file)

        print(f'>>> {regression_file}')
        if 'L' in os.path.basename(sm6_file):
            hemi = 'lh'
        elif 'R' in os.path.basename(sm6_file):
            hemi = 'rh'
        else:
            raise ValueError(os.path.basename(sm6_file))
        fsaverage6_sm6(regression_file, sm6_file, hemi)

    elif entities['extension'] == '.nii.gz':
        bandpass_file = os.path.join(output_dir, bold_preprocess_file.filename.replace('desc-preproc', 'desc-bandpass'))
        regression_file = os.path.join(output_dir, bold_preprocess_file.filename.replace('desc-preproc', 'desc-postproc'))

        bandpass_nifti(bold_preprocess_file.path, bandpass_file, TR)
        assert os.path.exists(bandpass_file)
        print(f'>>> {bandpass_file}')

        glm_nifti(bandpass_file, regression_file, Path(confounds_file))
        assert os.path.exists(regression_file)
        print(f'>>> {regression_file}')
    else:
        raise KeyError
