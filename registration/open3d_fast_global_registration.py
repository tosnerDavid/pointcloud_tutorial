# Open3D: www.open3d.org
# The MIT License (MIT)
# See license file or visit www.open3d.org for details

from open3d import *
from registration.open3d_global_registration import *
# from open3d_global_registration import *
import numpy as np
import copy

import time


def execute_fast_global_registration(source_down,
                                     target_down,
                                     source_fpfh,
                                     target_fpfh,
                                     voxel_size):
    distance_threshold = voxel_size * 0.5
    print(":: Apply fast global registration with distance threshold %.3f" % distance_threshold)
    result = open3d.pipelines.registration.registration_fast_based_on_feature_matching(source_down,
                                                         target_down,
                                                         source_fpfh,
                                                         target_fpfh,
                                                         open3d.pipelines.registration.FastGlobalRegistrationOption(maximum_correspondence_distance=distance_threshold))
    return result


if __name__ == "__main__":
    voxel_size = 0.05 # means 5cm for the dataset

    # Load data
    source = open3d.io.read_point_cloud("../data/1.ply")
    target = open3d.io.read_point_cloud("../data/2.ply")

    trans_init = np.asarray([[0.0, 0.0, 1.0, 0.0],
                            [1.0, 0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0, 1.0]])
    source.transform(trans_init)
    draw_registration_result(source, target, np.identity(4))

    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)

    # Ransac global registration
    start = time.time()
    result_ransac = execute_global_registration(source_down,
                                                target_down,
                                                source_fpfh,
                                                target_fpfh,
                                                voxel_size)
    print(result_ransac)
    print("Global registration took %.3f sec.\n" % (time.time() - start))
    draw_registration_result(source_down,
                             target_down,
                             result_ransac.transformation)

    # Fast Ransac Zhou 2016
    start = time.time()
    result_fast = execute_fast_global_registration(source_down,
                                                   target_down,
                                                   source_fpfh,
                                                   target_fpfh,
                                                   voxel_size)
    print("Fast global registration took %.3f sec.\n" % (time.time() - start))
    draw_registration_result(source_down,
                             target_down,
                             result_fast.transformation)


    # Secondary alignment
    source.transform(result_fast.transformation)
    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)

    start = time.time()
    result_fast = execute_fast_global_registration(source_down,
                                                   target_down,
                                                   source_fpfh,
                                                   target_fpfh,
                                                   voxel_size)
    print("Fast global registration took %.3f sec.\n" % (time.time() - start))
    draw_registration_result(source_down,
                             target_down,
                             result_fast.transformation)

