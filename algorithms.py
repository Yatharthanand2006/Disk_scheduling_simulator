# ---------------- FCFS (First Come First Serve) ----------------
def fcfs(request_list, start_head):
    # sequence will store movement of disk head
    movement_sequence = [start_head]

    # total distance travelled by head
    total_seek_time = 0

    current_position = start_head

    # process requests in same order as given
    for request in request_list:
        distance = abs(current_position - request)
        total_seek_time += distance

        current_position = request
        movement_sequence.append(request)

    return movement_sequence, total_seek_time


# ---------------- SSTF (Shortest Seek Time First) ----------------
def sstf(request_list, start_head):
    # copy list so original data is not modified
    remaining_requests = request_list.copy()

    movement_sequence = [start_head]
    total_seek_time = 0
    current_position = start_head

    # keep selecting closest request
    while remaining_requests:
        # find request with minimum distance from current head
        nearest_request = min(
            remaining_requests,
            key=lambda x: abs(x - current_position)
        )

        distance = abs(current_position - nearest_request)
        total_seek_time += distance

        current_position = nearest_request
        movement_sequence.append(nearest_request)

        # remove serviced request
        remaining_requests.remove(nearest_request)

    return movement_sequence, total_seek_time


# ---------------- SCAN (Elevator Algorithm) ----------------
def scan(request_list, start_head, disk_size):
    # sort requests for directional movement
    sorted_requests = sorted(request_list)

    movement_sequence = [start_head]
    total_seek_time = 0
    current_position = start_head

    # divide into left and right side of head
    left_side = [r for r in sorted_requests if r < current_position]
    right_side = [r for r in sorted_requests if r >= current_position]

    # move towards right end first
    for request in right_side:
        distance = abs(current_position - request)
        total_seek_time += distance

        current_position = request
        movement_sequence.append(request)

    # go till end of disk
    end = disk_size - 1
    total_seek_time += abs(current_position - end)
    current_position = end
    movement_sequence.append(end)

    # then reverse direction (like elevator)
    for request in reversed(left_side):
        distance = abs(current_position - request)
        total_seek_time += distance

        current_position = request
        movement_sequence.append(request)

    return movement_sequence, total_seek_time


# ---------------- C-SCAN (Circular SCAN) ----------------
def cscan(request_list, start_head, disk_size):
    sorted_requests = sorted(request_list)

    movement_sequence = [start_head]
    total_seek_time = 0
    current_position = start_head

    # split requests
    left_side = [r for r in sorted_requests if r < current_position]
    right_side = [r for r in sorted_requests if r >= current_position]

    # move right only
    for request in right_side:
        distance = abs(current_position - request)
        total_seek_time += distance

        current_position = request
        movement_sequence.append(request)

    # go till end
    end = disk_size - 1
    total_seek_time += abs(current_position - end)
    current_position = end
    movement_sequence.append(end)

    # jump to beginning (circular)
    total_seek_time += abs(current_position - 0)
    current_position = 0
    movement_sequence.append(0)

    # continue from start
    for request in left_side:
        distance = abs(current_position - request)
        total_seek_time += distance

        current_position = request
        movement_sequence.append(request)

    return movement_sequence, total_seek_time