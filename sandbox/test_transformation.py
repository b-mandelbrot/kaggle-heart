import matplotlib
# matplotlib.use('Qt4Agg')

import glob
import re
from matplotlib import animation
import matplotlib.pyplot as plt
# import data_test
import utils
import data as data_test
# import data_test
from configuration import set_configuration

set_configuration('test_config')

patch_size = (128, 128)
train_transformation_params = {
    'patch_size': patch_size,
    'rotation_range': (-90, 90),
    'translation_range': (-10, 10),
    'shear_range': (0, 0),
    'roi_scale_range': (0.9, 1.3),
    'do_flip': False,
    'sequence_shift': False
}

valid_transformation_params = {
    'patch_size': patch_size
}

data_path = '/mnt/sda3/data/kaggle-heart/pkl_validate'
slice2roi = utils.load_pkl('../pkl_train_slice2roi.pkl')
slice2roi_valid = utils.load_pkl('../pkl_validate_slice2roi.pkl')
slice2roi.update(slice2roi_valid)

patient_path = sorted(glob.glob(data_path + '/1/study'))
for p in patient_path:
    print p
    spaths = sorted(glob.glob(p + '/sax_*.pkl'), key=lambda x: int(re.search(r'/\w*_(\d+)*\.pkl$', x).group(1)))
    for s in spaths:
        d = data_test.read_slice(s)
        metadata = data_test.read_metadata(s)
        pid = utils.get_patient_id(s)
        sid = utils.get_slice_id(s)
        roi = slice2roi[pid][sid]


        def init():
            im.set_data(d[0])


        def animate(i):
            im.set_data(d[i])
            return im


        fig = plt.figure(1)
        fig.canvas.set_window_title(s)
        plt.subplot(121)
        im = plt.gca().imshow(d[0], cmap='gist_gray_r', vmin=0, vmax=255)
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=30, interval=50)

        # ---------------------------------

        out_data = data_test.transform_norm_rescale(d, metadata, train_transformation_params, roi=roi)


        def init_out():
            im2.set_data(out_data[0])


        def animate_out(i):
            im2.set_data(out_data[i])
            return im2


        plt.subplot(122)
        im2 = fig.gca().imshow(out_data[0], cmap='gist_gray_r', vmin=0., vmax=1.)
        anim2 = animation.FuncAnimation(fig, animate_out, init_func=init_out, frames=30, interval=50)

        plt.show()
