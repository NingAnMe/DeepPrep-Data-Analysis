
process bold_get_preproc_bold_file {
    tag "${task_id}"

    cpus 1
    memory '2 GB'

    input:
    val(preprocess_bids_dir)
    val(task_id)
    val(space)
    val(subject_id)
    
    val(output_dir)
    val(work_dir)
    output:
    path "sub-*"  // file_path & bids_cache_database_path
    script:
    script_py = "bold_get_preproc_bold_file.py"
    if (subject_id.toString() != '') {
        subject_id = "--subject_id ${subject_id}"
    }
    """
    ${script_py} \
    --bids_dir ${preprocess_bids_dir} \
    --task_id ${task_id} \
    --space ${space} \
    ${subject_id} \
    --output_dir ${output_dir} \
    --work_dir ${work_dir}
    """
}


process bold_postprocess {
    tag "${bold_id}"

    cpus 1
    memory '8 GB'
    label 'maxForks_10'

    input:
    val(preprocess_bids_dir)
    tuple(val(subject_id), val(bold_id), val(bold_preproc_file))
    val(confounds_index_file)

    val(repetition_time)
    val(freesurfer_home)
    val(subjects_dir)
    val(skip_frame)
    val(fwhm)

    val(output_dir)
    val(work_dir)
    output:
    tuple(val(subject_id), val(bold_id), val("anything"))
    script:
    script_py = "bold_denoise.py"
    if (repetition_time.toString() != '') {
        repetition_time = "--repetition_time ${repetition_time}"
    }
    if (freesurfer_home.toString() != '') {
        freesurfer_home = "--freesurfer_home ${freesurfer_home}"
    }
    if (subjects_dir.toString() != '') {
        subjects_dir = "--subjects_dir ${subjects_dir}"
    }
    """
    ${script_py} \
    --bold_preprocess_dir ${preprocess_bids_dir} \
    --bold_preproc_file ${bold_preproc_file} \
    --confounds_index_file ${confounds_index_file} \
    ${repetition_time} \
    ${freesurfer_home} \
    ${subjects_dir} \
    --skip_frame ${skip_frame} \
    --fwhm ${fwhm} \
    --output_dir ${output_dir} \
    --work_dir ${work_dir}
    """
}


workflow {

    preprocess_bids_dir = params.preprocess_bids_dir

    subjects_dir = params.subjects_dir  // optional
    freesurfer_home = params.freesurfer_home  // optional

    repetition_time = params.repetition_time  // optional
    confounds_index_file = params.confounds_index_file
    task_id = params.task_id
    space = params.space
    subject_id = params.subject_id  // optional

    skip_frame = params.skip_frame  // optional
    surface_fwhm = params.fwhm  // optional

    output_dir = params.output_dir

    postprocess_bids_dir = "${output_dir}/BOLD"
    work_dir = "${output_dir}/WorkDir"
    if (confounds_dir.toString() == '') {
        confounds_dir = params.preprocess_bids_dir
    }

    bold_orig_entities_file = bold_get_preproc_bold_file(preprocess_bids_dir, task_id, space, subject_id, postprocess_bids_dir, work_dir)
    bold_orig_entities_file = bold_orig_entities_file.flatten().multiMap { it ->
                                                                        a: [it.name.split('_')[0], it.name, it] }
    bold_postprocess_output = bold_postprocess(preprocess_bids_dir, bold_orig_entities_file,
                                               confounds_index_file, repetition_time, freesurfer_home, subjects_dir,
                                               skip_frame, fwhm, postprocess_bids_dir, work_dir)
}
