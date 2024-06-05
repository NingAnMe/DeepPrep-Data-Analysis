import numpy as np
import nibabel as nib


def glm_nifti(bpss_path, regression_path, regressor_path):
    '''
    Compute the residuals of the voxel information in a NIFTI file.

    bpss_path - path. Path of bold after bpass process.
    regressor_path - Path object.

    Creates a file with the same name as :nifti_path:, but ending with
    '_resid.nii.gz'.
    return:
        resid_path - path. Path of bold after regression process.
    '''

    # Read the regressors.
    regressors = []
    with regressor_path.open('r') as f:
        for line in f:
            if 'WB' in line:
                continue
            regressors.append(list(map(float, line.split())))
    regressors = np.array(regressors)

    # Read NIFTI values.
    nifti_img = nib.load(bpss_path)
    nifti_data = nifti_img.get_fdata()
    nx, ny, nz, nv = nifti_data.shape
    nifti_data = np.reshape(nifti_data, (nx * ny * nz, nv)).T

    # Assemble linear system and solve it.
    A = np.hstack((regressors, np.ones((regressors.shape[0], 1))))
    x = np.linalg.lstsq(A, nifti_data, rcond=-1)[0]

    # Compute residuals.
    residuals = nifti_data - np.matmul(A, x)
    residuals = np.reshape(residuals.T, (nx, ny, nz, nv))

    # Save result.
    hdr = nifti_img.header
    aff = nifti_img.affine
    new_img = nib.Nifti1Image(
        residuals.astype(np.float32), affine=aff, header=hdr)
    new_img.header['pixdim'] = nifti_img.header['pixdim']
    nib.save(new_img, regression_path)
    return regression_path
