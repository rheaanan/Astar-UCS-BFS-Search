import collections
import collections
import re
from queue import PriorityQueue
import math


def BFS(matrix_info, start, targets):
    start_col,start_row= [int(i) for i in start.split(" ")]
    cost = 0
    end_node = tuple(int(i) for i in targets.split(" "))
    # visited_nodes = []
    visited_nodes = set()
    open_queue = PriorityQueue()
    end_reached_flag = False

    open_queue.put((cost,(start_col,start_row),[(start_col,start_row)]))

    while  open_queue.qsize():
        cost,curr_node,path_till_now = open_queue.get()
        if curr_node == end_node:
            end_reached_flag =True
            # visited_nodes.append(curr_node)
            break
        if curr_node not in visited_nodes:
            get_neighbours(curr_node, open_queue, matrix_info, visited_nodes, cost, end_node, path_till_now)

            visited_nodes.add(curr_node)
    if end_reached_flag :
        return path_till_now
    else:
        return "FAIL"


def UCS(matrix_info, start,target):

    start_col,start_row= [int(i) for i in start.split(" ")]
    end_node = tuple(int(i) for i in target.split(" "))
    # visited_nodes = []
    visited_nodes = set()
    frontier_queue = PriorityQueue()
    end_reached_flag = False

    cost = 0
    frontier_queue.put((cost,(start_col,start_row),[(start_col,start_row)]))
    while frontier_queue.qsize():
        cost,curr_node,path_till_now = frontier_queue.get()

        if curr_node == end_node:
            # visited_nodes.append(curr_node)
            print(cost)
            end_reached_flag = True
            break

        if curr_node not in visited_nodes:
            get_neighbours(curr_node, frontier_queue, matrix_info, visited_nodes, cost, end_node, path_till_now)

            visited_nodes.add(curr_node)

    if end_reached_flag :
        return path_till_now
    else:
        return "FAIL"


def A_star(matrix_info, start,target):
    start_col,start_row= [int(i) for i in start.split(" ")]
    end_node = tuple(int(i) for i in target.split(" "))

    end_reached_flag = False
    frontier = PriorityQueue()
    visited_nodes = set()
    g =0
    h = get_heuristic([start_col,start_row],end_node)
    f = g+h
    frontier.put((f,(start_col,start_row),[(start_col,start_row)],g))

    while frontier.qsize():
        cost_final,curr_node,path_till_now,prev_g= frontier.get()

        if curr_node == end_node:
            # visited_nodes.append(curr_node)
            print(cost_final)
            end_reached_flag = True
            break

        if curr_node not in visited_nodes:
            get_neighbours(curr_node, frontier, matrix_info, visited_nodes, prev_g, end_node, path_till_now)

            visited_nodes.add(curr_node)

    if end_reached_flag :
        return path_till_now
    else:
        return "FAIL"

def get_neighbours(current,open,matrix,visited,cost,end,path):
    # neighbhour_row = [-1,1,0,0,-1,-1,1,1]
    # neighbhour_col = [0,0,-1,1,-1,1,1,-1]
    neighbhour_row = [-1,-1,-1,0,1,1,1,0]
    neighbhour_col = [-1,0,1,1,1,0,-1,-1]
    curr_parent = " ".join(map(str,current))
    # parent_track_dict[curr_parent] = []

    for i in range(0,len(neighbhour_row)):
        new_r = current[1] + neighbhour_row[i]
        new_c = current[0] + neighbhour_col[i]

        if new_r <0 or new_c <0:
            continue
        if new_r >= h or new_c >= w:
            continue

        if abs(get_stone_height(matrix,current)-get_stone_height(matrix,[new_c,new_r])) > stone_threshold:
            continue
        if (new_c, new_r) in visited:
            continue

        if algo_type == "BFS":
            open.put((cost + 1, (new_c, new_r), path + [(new_c, new_r)]))


        elif algo_type == "UCS":

            if  i%2 :

                open.put((cost+10,(new_c,new_r),path+[(new_c,new_r)]))
            else:
                open.put((cost+14,(new_c,new_r),path+[(new_c,new_r)]))

        elif algo_type == "A*":

            stone_height = abs(get_stone_height(matrix,current)-get_stone_height(matrix,[new_c,new_r]))
            mudd_cost = matrix[new_r][new_c]
            if mudd_cost <0:
                mudd_cost = 0
            dist = get_heuristic([new_c,new_r],end)
            cost_till_now = cost+mudd_cost+stone_height
            total_cost = cost_till_now+dist


            if  i%2 :
                open.put((total_cost+10, (new_c,new_r),path+[(new_c,new_r)],cost_till_now+10))
            else:
                open.put((total_cost+14, (new_c, new_r), path+[(new_c, new_r)], cost_till_now+14))


def get_stone_height(matrix, node):
    if int(matrix[node[1]][node[0]]) >= 0:
        return 0
    else:
        return abs(int(matrix[node[1]][node[0]]))


def get_heuristic(start,end):
    col_dist = abs(start[0]-end[0])
    row_dist = abs(start[1]-end[1])
    diagonal_dist  = 10* (col_dist+row_dist) + (14-2*10)*min(col_dist,row_dist)

    return diagonal_dist


if __name__ == "__main__":
    file_lines = []

    with open("input.txt") as input_file:
        for line in input_file.readlines():
            file_lines.append(line.strip())

    algo_type = file_lines[0].rstrip('\n')
    w, h = [int(i) for i in file_lines[1].rstrip('\n').split()]
    start_state = file_lines[2].rstrip()
    stone_threshold = int(file_lines[3].rstrip('\n'))
    no_of_targets = file_lines[4].rstrip('\n')

    target_list = file_lines[5:5 + int(no_of_targets)]
    matrix_info = (file_lines[5 + int(no_of_targets):])
    matrix_info = [re.sub('\s+', ',', x) for x in matrix_info]
    matrix_info = [[int(y) for y in x.split(",")] for x in matrix_info]
    result = []
    # print(algo_type,w,h,start_state,stone_threshold,no_of_targets,target_list,matrix_info)
    for items in target_list:
        if algo_type == "BFS":
            result.append(BFS(matrix_info, start_state, items))

        elif algo_type == "UCS":
            result.append(UCS(matrix_info, start_state, items))

        elif algo_type == "A*":

            result.append(A_star(matrix_info, start_state, items))
    result_str =''
    for r in result:
        if r != "FAIL":
            print(len(r))
            result_str+=" ".join(map(str,r)).replace("(",'').replace(")",'').replace(", ",',')+'\n'
        else:
            result_str+='FAIL\n'
    # print(result_str.rstrip())

    with open('output.txt','w') as op_file:
        op_file.write(result_str.rstrip())
    op_file.close()

