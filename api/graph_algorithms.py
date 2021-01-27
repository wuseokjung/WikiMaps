from timeout import timeout

def get_paths(page_ids, visited):
  paths = []

  for page_id in page_ids:
    if page_id is None:
      return [[]]
    else: 
      current_paths = get_paths(visited[page_id], visited)
      for current_path in current_paths:
        new_path = list(current_path)
        new_path.append(page_id)
        paths.append(new_path)

  return paths


# Returns list(list(int)), a list of id paths
@timeout(10)
def breadth_first_search_bidirectional(src_id, dest_id, db):
  # If the src and dest are identical, no search needed
  if src_id == dest_id:
    return [[src_id]]

  paths = []

  unvisited_forward = { src_id: [None] }
  unvisited_backward = { dest_id: [None] }

  visited_forward = {}
  visited_backward = {}

  forward_depth = 0
  backward_depth = 0

  while (len(paths) == 0 and ((len(unvisited_forward) != 0)) and (len(unvisited_backward) != 0)):
    forward_link_count = db.get_outgoing_link_count(unvisited_forward.keys())
    backward_link_count = db.get_incoming_link_count(unvisited_backward.keys())

    if forward_link_count < backward_link_count:
      # Forward BFS
      forward_depth += 1

      outgoing_links = db.get_outgoing_links(unvisited_forward.keys())

      for page_id in unvisited_forward:
        visited_forward[page_id] = unvisited_forward[page_id]

      unvisited_forward.clear()

      for src_page_id, dest_page_ids in outgoing_links:
        for dest_page_id in dest_page_ids.split('|'):
          if dest_page_id:
            dest_page_id = int(dest_page_id)

            if (dest_page_id not in visited_forward) and (dest_page_id not in unvisited_forward):
              unvisited_forward[dest_page_id] = [src_page_id]
            elif dest_page_id in unvisited_forward:
              unvisited_forward[dest_page_id].append(src_page_id)

    else:
      # Backward BFS
      backward_depth += 1

      incoming_links = db.get_incoming_links(unvisited_backward.keys())

      for page_id in unvisited_backward:
        visited_backward[page_id] = unvisited_backward[page_id]

      unvisited_backward.clear()

      for dest_page_id, src_page_ids in incoming_links:
        for src_page_id in src_page_ids.split('|'):
          if src_page_id:
            src_page_id = int(src_page_id)

            if (src_page_id not in visited_forward) and (src_page_id not in unvisited_backward):
              unvisited_backward[src_page_id] = [dest_page_id]
            elif src_page_id in unvisited_backward:
              unvisited_backward[src_page_id].append(dest_page_id)

    # Check path completion
    try:
      for page_id in unvisited_forward:
        if page_id in unvisited_backward:
          paths_from_src = get_paths(unvisited_forward[page_id], visited_forward)
          paths_from_dest = get_paths(unvisited_backward[page_id], visited_backward)

          for path_from_src in paths_from_src:
            for path_from_dest in paths_from_dest:
              current_path = list(path_from_src) + [page_id] + list(reversed(path_from_dest))

              if current_path not in paths:
                paths.append(current_path)
    except RecursionError:
      paths = []

  return paths


# Returns list(list(int)), a list of id paths
@timeout(10)
def breadth_first_search(src_id, dest_id, db):
  # If the src and dest are identical, no search needed
  if src_id == dest_id:
    return [[src_id]]

  paths = []

  # Initialize the src vertex to be unvisited
  unvisited = { src_id: [None] }

  visited = {}

  depth = 0

  while (len(paths) == 0) and (len(unvisited) != 0):
    depth += 1

    outgoing_links = db.get_outgoing_links(unvisited.keys())

    # Set all currently unvisited vertices as now visited
    for page_id in unvisited:
      visited[page_id] = unvisited[page_id]

    unvisited.clear()

    for src_page_id, dest_page_ids in outgoing_links:
      for dest_page_id in dest_page_ids.split('|'):
        if dest_page_id:
          dest_page_id = int(dest_page_id)

          if (dest_page_id not in visited) and (dest_page_id not in unvisited):
            unvisited[dest_page_id] = [src_page_id]
          elif dest_page_id in unvisited:
            unvisited[dest_page_id].append(src_page_id)

    # Check path completion
    try:
      for page_id in unvisited:
        paths_from_src = get_paths(unvisited[page_id], visited)
        for path in paths_from_src:
          current_path = list(path) + [page_id]
          if page_id == dest_id:
            paths.append(current_path)
    except RecursionError:
      paths = []

  return paths
