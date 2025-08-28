import numpy as np 

def peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right):
    '''
    For a collection of peak indices (x-positions),
    give each peak an ID, and let that ID follow the peak when it moves (within a threshold).
    New peaks get a new ID, and peaks that disappear are deleted.
    Peaks outside the min max range are discarded.
    Output a list of currently active (peak,ID), and a list of deleted peak IDs
    '''    
    print('\npeak_indices', peak_indices)
    
    remove_outside_range = []
    for i in range(len(peak_indices)):
        if peak_indices[i] > mask_right:
            remove_outside_range.append(i)
        if peak_indices[i] < mask_left:
            remove_outside_range.append(i)
    for i in remove_outside_range:
        del peak_indices[i]

    deleted_ids = []
    new_ids = []
    continued_ids = []
    for p in peak_indices:
        current_peak_id = current_peak_id % max_n_peaks
        if np.min(peak_prev_ids) == empty_id: # if no previous ids, just write new ones
            print(p,'peak ids empty, write new')
            peak_ids[current_peak_id] = p
            new_ids.append((current_peak_id,p))
            current_peak_id += 1
        else:
            index = np.abs(peak_prev_ids - p).argmin() # find closest
            if abs(peak_ids[index]-p) < peak_max_change:
                print(p, 'update peak id', index, 'at', peak_prev_ids[index])
                peak_ids[index] = p # if within range, update the old one
                continued_ids.append((int(index),p))
            else:
                print(p, 'make new peak')
                peak_ids[current_peak_id] = p # otherwise, make a new id
                new_ids.append((current_peak_id,p))
                current_peak_id += 1
    for i in range(len(peak_ids)):
        peak_ndx = peak_ids[i]
        if peak_ndx not in peak_indices: # when a peak disappears (or moves out of range), delete it
            peak_ids[i] = empty_id
            if peak_ndx < empty_id:
                print(peak_ndx, 'deleted peak')
                deleted_ids.append(i)
    print('new', new_ids, 'continued', continued_ids, 'deleted', deleted_ids)
    active_ids = new_ids
    for item in continued_ids:
        active_ids.append(item)
    return current_peak_id, peak_ids, active_ids, deleted_ids
    

empty_id = 9999
max_n_peaks = 99
peak_ids = np.zeros(max_n_peaks)
peak_ids += empty_id
peak_prev_ids = np.zeros(max_n_peaks)
peak_prev_ids += empty_id
current_peak_id = 0
peak_max_change = 50
mask_left = 0
mask_right = 1000

peak_indices = [20,120,220]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print('active_ids', active_ids)

peak_indices = [30,130,230]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)

peak_indices = [50,130]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print('active_ids', active_ids)

peak_indices = [110, 140, 250, 500]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print('active_ids', active_ids)

peak_indices = [250, 700]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print('active_ids', active_ids)

peak_indices = [100, 900]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print('active_ids', active_ids)

peak_indices = [160, 990]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print('active_ids', active_ids)

peak_indices = [170, 1010]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print('active_ids', active_ids)