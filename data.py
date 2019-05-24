import os, random
import SimpleITK as sitk
import numpy as np
from scipy.ndimage import morphology
from scipy.stats.mstats import winsorize

data_path = 'data'
if 'DEFORM_EVAL_DATA_PATH' in os.environ:
    data_path = os.environ['DEFORM_EVAL_DATA_PATH']

img_path = os.path.join(data_path, 'images')
src_path = os.path.join(data_path, 'src')
processed_img_path = os.path.join(data_path, 'images_processed')
seg_path = os.path.join(data_path, 'segmentations')
affine_path = os.path.join(data_path, 'affine')

subjects = [
    'a01',
    'a02',
    'a03',
    'a04',
    'a05',
    'a06',
    'a07',
    'a08',
    'a09',
    'a10',
    'a11',
    'a12',
    'a13',
    'a14',
    'a15',
    'a16',
    'a17',
    'a18',
    'a19',
    'a20',
    'a21',
    'a22',
    'a23',
    'a24',
    'a25',
    'a26',
    'a27',
    'a28',
    'a29',
    'a30'
]

pairs = [
    ('a05', 'a29'),
    ('a23', 'a18'),
    ('a13', 'a14'),
    ('a03', 'a10'),
    ('a27', 'a11'),
    ('a30', 'a19'),
    ('a06', 'a10'),
    ('a27', 'a03'),
    ('a15', 'a26'),
    ('a09', 'a15'),
    ('a24', 'a21'),
    ('a10', 'a25'),
    ('a27', 'a15'),
    ('a13', 'a03'),
    ('a29', 'a19'),
    ('a26', 'a17'),
    ('a25', 'a21'),
    ('a20', 'a16'),
    ('a16', 'a04'),
    ('a02', 'a05'),
    ('a10', 'a03'),
    ('a16', 'a12'),
    ('a13', 'a02'),
    ('a28', 'a06'),
    ('a24', 'a13')
]

def generate_pairs(n):
    rng = random.Random(60127)

    """ Generates a list of n random pairs """
    pairs = []
    
    def gen_pair():
        p = None
        while True:
            p = (
                subjects[rng.randint(0, len(subjects)-1)],
                subjects[rng.randint(0, len(subjects)-1)]
            )
            if p[0] != p[1] and p not in pairs:
                break
        return p

    for i in range(0, n):
        pairs.append(gen_pair())
    return pairs

def get_pairs():
    """ Returns a list of tuples with all registration pairs """
    return pairs

def image_file(id):
    return os.path.join(img_path, '{}.vtk'.format(id))
    
def processed_image_file(id):
    return os.path.join(processed_img_path, '{}.vtk'.format(id))

def segmentation_file(id):
    return os.path.join(seg_path, '{}_seg.vtk'.format(id))

def affine_file(p):
    return os.path.join(affine_path, 'ants_{}_{}_affine.vtk'.format(p[0],p[1]))

def src_image_file(id):
    return os.path.join(src_path, '{}.nii.gz'.format(id))

def src_segmentation_file(id):
    return os.path.join(src_path, '{}-seg.nii.gz'.format(id))

def get_subjects():
    """ Returns a list of all subject ids """
    return subjects

def preprocess(img):
    """
        Winsorizing
    """
    data = sitk.GetArrayFromImage(img)
    
    n = np.product(data.shape)
    data = winsorize(data, limits=(0.005,0.005))
    
    out = sitk.GetImageFromArray(data)
    out.SetOrigin(img.GetOrigin())
    out.SetSpacing(img.GetSpacing())
    
    return out


def setup(src):
    subjects = get_subjects()

    if not os.path.exists(src):
        raise Exception('Source data missing')

    if not os.path.isdir(data_path):
        os.mkdir(data_path)

    if not os.path.isdir(img_path):
        os.mkdir(img_path)

    if not os.path.isdir(processed_img_path):
        os.mkdir(processed_img_path)

    if not os.path.isdir(seg_path):
        os.mkdir(seg_path)

    if not os.path.isdir(affine_path):
        os.mkdir(affine_path)

    for s in subjects:
        print(s)

        writer = sitk.ImageFileWriter()

        img = sitk.ReadImage(os.path.join(src, '{}.nii.gz'.format(s)), sitk.sitkFloat32)
        writer.SetFileName(image_file(s))
        writer.Execute(img)
        
        img_p = preprocess(img)
        writer.SetFileName(processed_image_file(s))
        writer.Execute(img_p)
        
        seg = sitk.ReadImage(os.path.join(src, '{}-seg.nii.gz'.format(s)), sitk.sitkUInt8)
        seg.SetOrigin(img.GetOrigin())
        seg.SetSpacing(img.GetSpacing())
        writer.SetFileName(segmentation_file(s))
        writer.Execute(seg)