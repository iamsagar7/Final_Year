import ast
import csv
import math
import os
import random
import itertools
import matplotlib.pyplot as mplpyplot
import numpy as np
from typing import Dict


def load_config(path) -> Dict:
    with open(path, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    return ast.literal_eval(data)


def replace_str_with_float(list_of_list) -> None:
    for l in list_of_list:
        for idx in range(0, len(l)):
            try:
                f = string_to_float(l[idx])
                l[idx] = f
            except ValueError:
                pass


def load_csv_to_header_data(filename) -> Dict:
    fpath = os.path.join(os.getcwd(), filename)
    fs = csv.reader(open(fpath, newline='\n'))
    all_row = []
    for r in fs:
        all_row.append(r)

    headers = all_row[0]
    idx_to_name, name_to_idx = get_header_name_to_idx_maps(headers)

    data = {
        'header': headers,
        'rows': all_row[1:],
        'name_to_idx': name_to_idx,
        'idx_to_name': idx_to_name
    }

    replace_str_with_float(data['rows'])

    return data


def fit(points, bandwidth):

        shift_points = np.array(points)
        shifting = [True] * points.shape[0]

        while True:
            max_dist = 0
            for i in range(0, len(shift_points)):
                if not shifting[i]:
                    continue
                p_shift_init = shift_points[i].copy()
                shift_points[i] = _shift_point(shift_points[i], points, bandwidth)
                dist = distance(shift_points[i], p_shift_init)
                max_dist = max(max_dist, dist)
                shifting[i] = dist < 4

            if(max_dist > 4):
                break
        cluster_ids = _cluster_points(shift_points.tolist())
        return shift_points, cluster_ids

def _shift_point(point, points, kernel_bandwidth):
        shift_x = 0.0
        shift_y = 0.0
        scale = 0.0
        for p in points:
            dist = distance(point, p)
            weight = weight_fun(dist, kernel_bandwidth)
            shift_x += p[0] * weight
            shift_y += p[1] * weight
            scale += weight
        shift_x = shift_x / scale
        shift_y = shift_y / scale
        return [shift_x, shift_y]

def _cluster_points(points):
        cluster_ids = []
        cluster_idx = 0
        cluster_centers = []

        for i, point in enumerate(points):
            if(len(cluster_ids) == 0):
                cluster_ids.append(cluster_idx)
                cluster_centers.append(point)
                cluster_idx += 1
            else:
                for center in cluster_centers:
                    dist = distance(point, center)
                    if(dist < 4):
                        cluster_ids.append(cluster_centers.index(center))
                if(len(cluster_ids) < i + 1):
                    cluster_ids.append(cluster_idx)
                    cluster_centers.append(point)
                    cluster_idx += 1
        return cluster_ids


def get_header_name_to_idx_maps(headers):
    name_to_idx = {}
    idx_to_name = {}
    for i in range(0, len(headers)):
        name_to_idx[headers[i]] = i
        idx_to_name[i] = headers[i]
    return idx_to_name, name_to_idx


def project_columns(data, columns_to_project):
    data_h = list(data['header'])
    data_r = list(data['rows'])

    all_cols = list(range(0, len(data_h)))

    columns_to_project_ix = [data['name_to_idx'][name] for name in columns_to_project]
    columns_to_remove = [cidx for cidx in all_cols if cidx not in columns_to_project_ix]

    for delc in sorted(columns_to_remove, reverse=True):
        del data_h[delc]
        for r in data_r:
            del r[delc]

    idx_to_name, name_to_idx = get_header_name_to_idx_maps(data_h)

    return {'header': data_h, 'rows': data_r,
            'name_to_idx': name_to_idx,
            'idx_to_name': idx_to_name}


def attri_clus(datum, cluster_atts_idxs):
    return [datum[x] for x in cluster_atts_idxs]

sd=3
def nearest_cluster(centroids, cluster_atts_idx, data):
    closest_centroid_idx = None
    closest_centroid_distance = None
    for centroid_idx in range(0, len(centroids)):
        centroid_datum = centroids[centroid_idx]
        if None is centroid_datum:
            continue

        distance = distance_between(data, centroid_datum, cluster_atts_idx)

        if closest_centroid_distance is None or distance < closest_centroid_distance:
            closest_centroid_distance = distance
            closest_centroid_idx = centroid_idx

    return closest_centroid_distance, closest_centroid_idx

def distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def weight_fun(distance, bandwidth):
    return (1 / (bandwidth * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((distance / bandwidth)) ** 2)


def mean_shift(data_rows, k, cluster_atts_idxs):
    centroids = list(itertools.repeat(None, k))

    r = random.randint(0, len(data_rows) - 1)
    centroids[0] = attri_clus(data_rows[r], cluster_atts_idxs)

    for i in range(1, k):
        d = []
        sum_of_squared_distances = 0
        for num in range(0, len(data_rows)):
            datum = data_rows[num]
            closest_distance, closest_idx = nearest_cluster(centroids, cluster_atts_idxs, datum)
            d.append([num, math.pow(closest_distance, 2)])
            sum_of_squared_distances += math.pow(closest_distance, 2)

        ban = random.random()

        accumulator = 0
        s_idx = 1
        while accumulator < ban:
            s_idx = s_idx + 1
            accumulator += d[s_idx][1] / sum_of_squared_distances

        centroids[i] = attri_clus(data_rows[d[s_idx][0]], cluster_atts_idxs)
    return centroids


def rand_init_centroids(data_rows, k, cluster_atts_idxs):
    centroids = list(itertools.repeat(None, k))

    idxs = list(range(0, len(data_rows)))

    for i in range(0, k):
        r = random.randint(0, len(idxs) - 1)
        r_idx = idxs[r]
        del idxs[r]
        datum = data_rows[r_idx]
        centroids[i] = attri_clus(datum, cluster_atts_idxs)

    return centroids


def string_to_float(v):
    return float(v)


def assignment_step(centroids, cluster_atts_idx, data_rows):
    cluster_assignment = {}
    distortion = 0

    for datum_idx in range(0, len(data_rows)):
        datum = data_rows[datum_idx]

        centroid_distance, centroid_idx = nearest_cluster(centroids, cluster_atts_idx, datum)

        if centroid_idx not in cluster_assignment:
            cluster_assignment[centroid_idx] = list()
        cluster_assignment[centroid_idx].append(datum_idx)
        distortion += centroid_distance

    return cluster_assignment, distortion


def distance_between(datum, centroid_datum, cluster_atts_idxs):
    s = 0
    datum_comparable_atts = attri_clus(datum, cluster_atts_idxs)
    for i in range(0, len(datum_comparable_atts)):
        centroid_datum_att_value = datum_comparable_atts[i]
        datum_att_value = centroid_datum[i]

        s += math.pow(abs(centroid_datum_att_value - datum_att_value),2)

    return math.sqrt(s)
    #return distance(centroid_datum_att_value,datum_att_value)


def update_centroids(data_rows, cluster_assignments, cluster_atts_idxs, k):
    centroids = list(itertools.repeat(None, k))

    num_of_atts = len(cluster_atts_idxs)

    for cluster_id in sorted(cluster_assignments):
        data_for_cluster_idxs = cluster_assignments[cluster_id]
        new_centroid = list(itertools.repeat(0.0, num_of_atts))

        num_in_cluster = len(data_for_cluster_idxs)

        for X_in_idx in data_for_cluster_idxs:
            datum = data_rows[X_in_idx]
            datum_comparable_atts = attri_clus(datum, cluster_atts_idxs)
            for cluster_atts_idx_idx in range(0, num_of_atts):
                new_centroid[cluster_atts_idx_idx] += \
                    datum_comparable_atts[cluster_atts_idx_idx]

        for cluster_atts_idx_idx in range(0, num_of_atts):
            new_centroid[cluster_atts_idx_idx] /= num_in_cluster

        centroids[cluster_id] = new_centroid
    return centroids


image_seq = 0


def plot_cluster_assignments(cluster_assignments, centroids, data_rows,
                             cluster_atts, cluster_atts_idxs, distortion, plot_config):
    colors = {0: 'Red', 1: 'Blue', 2: 'Green', 3: 'Purple'}

    plots_configs = plot_config['plots_configs']
    num_of_plots = len(plots_configs)

    fig, subplots = mplpyplot.subplots(1, num_of_plots)
    fig.set_size_inches(4 * num_of_plots, 4, forward=True)

    for idx in range(0, len(plots_configs)):
        plot_atts = plots_configs[idx]['plot_atts']

        try:
            subplot = subplots[idx]
        except TypeError:
            subplot = subplots

        fig.suptitle('Distortion=' + str(round((distortion+3), 3)))

        for cluster_assignment in cluster_assignments:

            cluster_data = [data_rows[x] for x in cluster_assignments[cluster_assignment]]

            x_att = plot_atts[0]
            y_att = plot_atts[1]

            x_att_centroid_idx = cluster_atts.index(x_att)
            y_att_centroid_idx = cluster_atts.index(y_att)

            x_raw_data_idx = cluster_atts_idxs[x_att_centroid_idx]
            y_raw_data_idx = cluster_atts_idxs[y_att_centroid_idx]

            dataum_axis_x_data = [cluster_datum[x_raw_data_idx] for cluster_datum in cluster_data]
            dataum_axis_y_data = [cluster_datum[y_raw_data_idx] for cluster_datum in cluster_data]
            dataum_axis_x_data, dataum_axis_y_data = sort_for_plot(dataum_axis_x_data, dataum_axis_y_data)

            subplot.plot(dataum_axis_x_data, dataum_axis_y_data, marker='o', linestyle='', c=colors[cluster_assignment])
            # centroid
            centroid = centroids[cluster_assignment]
            centroid_axis_x_data = [centroid[x_att_centroid_idx]]
            centroid_axis_y_data = [centroid[y_att_centroid_idx]]

            subplot.plot(centroid_axis_x_data, centroid_axis_y_data, marker='o', linestyle='',
                         c=colors[cluster_assignment],
                         ms=20)

            subplot.set_title(x_att + ' / ' + y_att)
    fig.tight_layout()
    fig.subplots_adjust(top=0.855)

    fig.show()
    global image_seq

    if 'output_file_prefix' in plot_config:
        fig.savefig(plot_config['output_file_prefix'] + " "+str(image_seq) + ".png")
        image_seq += 1
    mplpyplot.close(fig)

#function
def means(data, bandwidth, cluster_atts, cluster_atts_idxs, init_func, plot_config):
    # select initial centroids
    data_rows = data['rows']

    centroids = init_func(data_rows, bandwidth, cluster_atts_idxs)
    cluster_assignments, distortion = assignment_step(centroids, cluster_atts_idxs, data_rows)

    plot_cluster_assignments(cluster_assignments, centroids, data_rows,
                             cluster_atts, cluster_atts_idxs, distortion, plot_config)

    while True:
        centroids = update_centroids(data_rows, cluster_assignments, cluster_atts_idxs, bandwidth)
        next_cluster_assignments, distortion = assignment_step(centroids, cluster_atts_idxs, data_rows)
        if cluster_assignments == next_cluster_assignments:
            break
        cluster_assignments = next_cluster_assignments

        plot_cluster_assignments(cluster_assignments, centroids, data_rows,
                                 cluster_atts, cluster_atts_idxs, distortion, plot_config)

    plot_cluster_assignments(cluster_assignments, centroids, data_rows,
                             cluster_atts, cluster_atts_idxs, distortion, plot_config)

    return cluster_assignments, centroids, distortion


def sort_for_plot(x, y):
    return zip(*sorted(zip(x, y)))


def main(path):
    # argv=sys.argv
    # config = load_config(argv[1])

    config = load_config(path)


    print(config)

    data = load_csv_to_header_data(config['data_file'])
    data = project_columns(data, config['data_project_columns'])

    bandwidth = config['max-no-cluster']
    cluster_atts = config['cluster_atts']
    cluster_atts_idxs = [data['name_to_idx'][x] for x in cluster_atts]

    plot_config = config['plot_config']

    if 'init_cluster_func' in config:
        init_func = globals()[config['init_cluster_func']]
    else:
        init_func = globals()['rand_init_centroids']

    final_cluster_assignments, final_centroids, distortion \
        = means(data, bandwidth, cluster_atts, cluster_atts_idxs, init_func, plot_config)

    data_rows = data['rows']

    plot_cluster_assignments(final_cluster_assignments, final_centroids,
                             data_rows, cluster_atts, cluster_atts_idxs,
                             distortion, plot_config)


if __name__ == "__main__": main()