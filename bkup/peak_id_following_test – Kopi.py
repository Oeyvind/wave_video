import numpy as np 
def peak_id_following(peak_indices, peak_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right):
    '''
    For a collection of peak indices (x-positions),
    give each peak an ID, and let that ID follow the peak when it moves (within a threshold).
    New peaks get a new ID, and peaks that disappear are deleted.
    Peaks outside the min max range are discarded.
    Output a list of currently active (peak,ID), and a list of deleted peak IDs
    '''    
    #print('\nid following', peak_indices, peak_ids)
    prev_peak_ids = np.copy(peak_ids)
    
    remove_outside_range = []
    for i in range(len(peak_indices)):
        if peak_indices[i] > mask_right:
            remove_outside_range.append(i)
        if peak_indices[i] < mask_left:
            remove_outside_range.append(i)
    remove_outside_range.sort(reverse=True)
    for i in remove_outside_range:
        del peak_indices[i]

    deleted_ids = []
    new_ids = []
    continued_ids = []
    current_peak_id = current_peak_id % max_n_peaks
    if np.min(peak_ids) == empty_id: # if no previous ids, just write new ones
        for p in peak_indices:
            print(p,'peak ids empty, write new')
            peak_ids[current_peak_id] = p
            new_ids.append([current_peak_id,p,0]) # zero movement since previous x as it is new
            current_peak_id = (current_peak_id+1)%max_n_peaks
    else:
        isclose_matrix = np.zeros((len(peak_ids),len(peak_indices)))
        watchlist = []
        print('test', peak_indices, peak_ids)
        for i in range(len(prev_peak_ids)):
            print('is close to', prev_peak_ids[i])
            is_close = np.isclose(peak_indices, prev_peak_ids[i], rtol=0, atol=peak_max_change)
            print(i,is_close)
            if np.sum(is_close) > 1:
                watchlist.append(i)
        print('watchlist',watchlist)
        for w in watchlist:
            print(f'{prev_peak_ids[w]} is close to {np.where}')
            #    print('pid',pid,np.isclose(peak_indices, pid, rtol=0, atol=peak_max_change))
        
        for p in peak_indices:
            index = np.abs(prev_peak_ids - p).argmin() # find closest
            if abs(p-prev_peak_ids[index]) < peak_max_change: 
                print(p, 'update peak id', index, 'prev', prev_peak_ids[index])
                peak_ids[index] = p # if within range, update the old one
                continued_ids.append([int(index),p,int(peak_ids[index]-prev_peak_ids[index])]) #last item is x movement since previous frame (?)
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
        if item not in active_ids:
            active_ids.append(item)
    return current_peak_id, peak_ids, active_ids, deleted_ids
    

empty_id = 9999
max_n_peaks = 9
peak_ids = np.zeros(max_n_peaks)
peak_ids += empty_id
current_peak_id = 0
peak_max_change = 51
mask_left = 0
mask_right = 1000

peak_indices_set = [[20,120,220],
                    [30,130,230],
                    [50,130, 190],
                    [110, 140, 240, 500]]
for peak_indices in peak_indices_set:
    print(f'\npeak indices {peak_indices}')
    current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)    
    print(f'active_ids {active_ids} \n peak_ids \n{peak_ids}')

'''
peak_indices = [250, 700]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print(f'active_ids {active_ids} \n')

peak_indices = [100, 900]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print(f'active_ids {active_ids} \n')

peak_indices = [160, 990]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print(f'active_ids {active_ids} \n')

peak_indices = [170, 1010]
current_peak_id, peak_ids, active_ids, deleted_ids = peak_id_following(peak_indices, peak_ids, peak_prev_ids, current_peak_id, peak_max_change, max_n_peaks, empty_id, mask_left, mask_right)
peak_prev_ids = np.copy(peak_ids)
print(f'active_ids {active_ids} \n')
'''

'''
Notes for peak id following
Basic: 
    - if new peak in range of previous peak: use same ID
    - if not in range: use new ID

Problem:
    - if two peaks in range
    - then we need to decide which continues, and which peak get a new ID
    * Basic: 
        - the peak closest gets to continue
        - the other search for another available ID that is within range
            - if another ID within range, inherit that
            - otherwise, get new ID
    * Peak_max_change adjustment
        - if we always have only new IDs, adjust peak_max_change down

    * discarded strategy with peak move direction:
    * But:
        - if the peak was already moving in one direction:
            - try to continue in that direction
            - which means, perhaps we need to choose the ID in that direction (not closest)
    * Example:
        1. check direction
        2. if within range of 2 IDs
           AND next peak also in range of this ID
           AND next peak has a choice of going to the next ID (it is within range of 2 IDs)
        3. then bump in the direction it was moving

'''