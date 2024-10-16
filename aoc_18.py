# AoC 2019 Day 18
# Part 1:
# Part 2:
from collections import defaultdict

part1_correct = 4042
part2_correct = 2014

CURRENT_FILE = 'aoc_18_input.txt'

# def print_map(m):
#     for y in range(0, len(m[0])):
#         for x in range(0, len(m)):
#             print(m[x][y], end='')
#         print()
#

'''
Node
  key = (x,y) coordinate
  contains (nothing, key, door)
  connects to [(x,y)..... 
'''


class Node:
    def __str__(self):
        return "<N: {} @ {} neigh: {}>".format(self.value, self.coord, self.edges)

    def __init__(self, coord, value, edges):
        if value == '#':
            print(f'error Node created with value {value} (WALL) at {coord} with edges {edges}')
        self.coord = coord
        self.value = value
        self.edges = edges
        self.edge_weight = [1] * len(edges)

    def get_weighted_edge_list(self):
        result = []
        for i in range(0, len(self.edges)):
            w = self.edge_weight[i]
            e = self.edges[i]
            result.append((e, w))
        return result


def neighbors(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


GRID_SIZE = 80

WALL = '#'
EMPTY = '.'
KEYS = set(map(chr, range(ord('a'), ord('z') + 1)))
DOORS = set(map(chr, range(ord('A'), ord('Z') + 1)))


def part1(all_file):
    print()

    grid = all_file.split('\n')

    door_list = []
    key_list = []

    coord_to_node = dict()
    poi_to_node = dict()
    node_list = []
    start_node = None
    poi_node_list = []
    path_count = 0
    path_list = []
    for y in range(0, GRID_SIZE + 1):
        for x in range(0, GRID_SIZE + 1):
            ch = grid[y][x]
            if ch == '#':
                pass
            else:
                edges = []
                for (x1, y1) in neighbors(x, y):
                    n_ch = grid[y1][x1]
                    if n_ch is not WALL:
                        edges.append((x1, y1))
                n = Node((x, y), ch, edges)
                coord_to_node[(x, y)] = n
                node_list.append(n)
                if ch == '@':
                    start_node = n
                    poi_node_list.append(n)
                    poi_to_node[(x, y)] = n
                elif ch in KEYS:
                    key_list.append(n)
                    poi_node_list.append(n)
                    poi_to_node[ch] = n
                elif ch in DOORS:
                    door_list.append(n)
                    poi_node_list.append(n)
                    poi_to_node[ch] = n
                else:
                    assert (ch == '.')
                    path_list.append(n)
                    path_count += 1
    print(f'{len(node_list)} nodes with {len(poi_to_node)} POI nodes')
    print(f'entrace node: {start_node}')
    for n in node_list:
        if n.value == 'Y':
            print(f'Y Door is at {n.coord}  (for reference')
            break
    print("\n shrinking graph")
    merge_or_discard = True

    while merge_or_discard:
        merge_or_discard = False
        merge_count = None
        while merge_count is None or merge_count > 0:
            merge_count = 0
            merged_nodes = []
            for n in node_list:
                assert (n.value != WALL)
                if n.value == EMPTY and len(n.edges) == 2:
                    assert (n not in poi_node_list)
                    (x1, y1) = n.edges[0]
                    (x2, y2) = n.edges[1]


                    n1 = coord_to_node[(x1, y1)]

                    n2 = coord_to_node[(x2, y2)]

                    i1 = n1.edges.index(n.coord)
                    i2 = n2.edges.index(n.coord)
                    (w1, w2) = (n1.edge_weight[i1], n2.edge_weight[i2])
                    n1.edges.pop(i1)
                    n2.edges.pop(i2)
                    new_weight = w1 + w2
                    n1.edge_weight.pop(i1)
                    n2.edge_weight.pop(i2)
                    n1.edges.append(n2.coord)
                    n1.edge_weight.append(new_weight)
                    n2.edges.append(n1.coord)
                    n2.edge_weight.append(new_weight)

                    merge_count += 1
                    merged_nodes.append(n)

            else:
                pass  # print('f {len(n.edges)} is too many for me ')

            assert (merge_count == len(merged_nodes))
            if merge_count > 0: merge_or_discard = True
            #        print(f'merged_nodes ({len(merged_nodes)}): {list(map(lambda n: (n.value, n.coord), merged_nodes))}')
            path_count -= merge_count
            for m in merged_nodes:
                node_list.remove(m)
                path_list.remove(m)
                coord_to_node.pop(m.coord)
        #         print(
        #            f'merge {merge_count} nodes, leaving {len(path_list)} path nodes, {len(poi_node_list)} poi nodes {len(node_list)} total')

        #    print("\nlooking for dandling nodes")

        discard_count = None
        while discard_count == None or discard_count > 0:
            discard_nodes = []
            discard_count = 0
            for n in node_list:
                if n not in poi_node_list:
                    edge_count = len(n.edges)
                    if edge_count == 1:
                        # print(f'\tnode has 1 edge: {n}')
                        n1_coord = n.edges[0]
                        n1 = coord_to_node[n1_coord]
                        # print(f'\t\tneighbor node: {n1}')
                        i = n1.edges.index(n.coord)

                        n1.edges.pop(i)
                        n1.edge_weight.pop(i)
                        discard_nodes.append(n)
                        discard_count += 1
            if discard_count > 0: merge_or_discard
            for m in discard_nodes:
                node_list.remove(m)
                path_list.remove(m)
                path_count -= 1
                coord_to_node.pop(m.coord)
    #           print(f'found {discard_count} dangling nodes, leaving {len(path_list)} path nodes, {len(poi_node_list)} poi nodes {len(node_list)} total')
    edges_nums = defaultdict(lambda: 0)
    for n in node_list:
        e_count = len(n.edges)
        edges_nums[e_count] += 1
    print(edges_nums)
    print(f'leaving {len(path_list)} path nodes, {len(poi_node_list)} poi nodes {len(node_list)} total')
    print(len(node_list))
    print(f'there are {len(path_list)} or {path_count} non-POI nodes remaining')

    # we want to eliminate all p_nodes
    for p_node in path_list:
        neigh_value_list = list(map(lambda c: coord_to_node[c].value, p_node.edges))
        print(f'working p_node: {p_node}  {neigh_value_list} ')
        print(f' edges: {edges_nums[p_node]}')  # B-(66,1) t-(79,1) n-(65,5)
        print(f'\t edge weights: {p_node.edge_weight}') # 1   12  30
        p_coords = p_node.coord

        for left_coord_i  in range(len(p_node.edges)):
                left_coords = p_node.edges[left_coord_i]
                left_node = coord_to_node[left_coords]
                left_weight = p_node.edge_weight[left_coord_i]
                print(f'\t left node {left_node.value} @ {left_coords} distance: {left_weight}')
                for right_coord_i in range(len(p_node.edges)):
                    right_coords = p_node.edges[right_coord_i]
                    if left_coords == right_coords: continue
                    right_node = coord_to_node[right_coords]
                    right_weight = p_node.edge_weight[right_coord_i]
                    print(f'adding new links from {left_node.value} <-> {right_node.value}')
                    print(f'\t right node {right_node.value} @ {right_coords} distance: {right_weight}')



                    print()
                    print(f'\t\t left_node {left_node} {list(map(lambda c: coord_to_node[c].value, left_node.edges))}')
                    print(f'\t\t\t edges: {left_node.edges}')
                    print(f'\t\t\t weights {left_node.edge_weight}')

                    print()
                    print(f'\t\t right_node {right_node} {list(map(lambda c: coord_to_node[c].value, right_node.edges))}')
                    print(f'\t\t\t edges: {right_node.edges}')
                    print(f'\t\t\t weights {right_node.edge_weight}')


                    #add new edge left->right
                    left_node.edges.append(right_coords)
                    left_node.edge_weight.append(left_weight+right_weight)
                    #add new edge right->left
                    right_node.edges.append(left_coords)
                    right_node.edge_weight.append(right_weight+left_weight)

                    left_p_idx = left_node.edges.index(p_coords)
                    left_node.edges.pop(left_p_idx)
                    left_node.edge_weight.pop(left_p_idx)

                    right_p_idx = right_node.edges.index(p_coords)
                    right_node.edges.pop(right_p_idx)
                    right_node.edge_weight.pop(right_p_idx)

                    print()
                    print(f'\t\t left_node {left_node} {list(map(lambda c: coord_to_node[c].value, left_node.edges))}')
                    print(f'\t\t\t edges: {left_node.edges}')
                    print(f'\t\t\t weights {left_node.edge_weight}')

                    print()
                    print(
                        f'\t\t right_node {right_node} {list(map(lambda c: coord_to_node[c].value, right_node.edges))}')
                    print(f'\t\t\t edges: {right_node.edges}')
                    print(f'\t\t\t weights {right_node.edge_weight}')


                break

                # n1 = coord_to_node[(x1, y1)]
                # n2 = coord_to_node[(x2, y2)]
                # i1 = n1.edges.index(n.coord)
                # i2 = n2.edges.index(n.coord)
                # (w1, w2) = (n1.edge_weight[i1], n2.edge_weight[i2])
                # n1.edges.pop(i1)
                # n2.edges.pop(i2)
                # new_weight = w1 + w2
                # n1.edge_weight.pop(i1)
                # n2.edge_weight.pop(i2)
                # n1.edges.append(n2.coord)
                # n1.edge_weight.append(new_weight)
                # n2.edges.append(n1.coord)
                # n2.edge_weight.append(new_weight)

        break


    return None


def part2(all_file):
    return None


def main():
    print(f' AoC 2019, Day 18')

    with open(CURRENT_FILE, 'r') as input_file:
        all_file = input_file.read()

    # print(f'\tpart 1:   ', end="")

    part1_answer = part1(all_file)
    return
    if part1_answer != part1_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part1_correct} ')
        print(f'\t\t Received : {part1_answer}')
    else:
        print(f'{part1_answer} \t\t\t ')

    print(f'\tpart 2:   ', end="")

    part2_answer = part2(all_file)

    if part2_answer != part2_correct:
        print(f'\n\t\t INCORRECT ANSWER')
        print(f'\t\t Should be: {part2_correct} ')
        print(f'\t\t Received : {part2_answer}')
    else:
        print(f'{part2_answer} \t\t\t ')


if __name__ == "__main__":
    main()
