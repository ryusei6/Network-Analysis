# -*- coding:utf-8 -*-
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import json
import numpy as np

import itertools
import collections
import pygraphviz as pgv

# --------------パラメータ調整------------------

# 表示レイアウト
layout_list = ['dot', 'neato', 'fdp', 'sfdp', 'twopi', 'circo'] # レイアウトの種類
layout = layout_list[2] # dot, fdpあたりが綺麗

fontsize = 300 # ノード名のフォントサイズ
edge_cut_point = 50 # edge_cut_point件以下のエッジは表示しない（孤立したノードも表示しない）
node_correction = 0.005 # ノードの大きさ補正
penwidth_correction = 0.1 # エッジの太さ補正

# --------------パラメータ調整ここまで------------------

def search_match_index(list, x):
    return list.index(x) if x in list else -1


def create_edge_weight_lists(edge_lists):
    edge_weight_lists = []
    for edge in edge_lists:
        match_index = search_match_index([edge_weight_list[0] for edge_weight_list in edge_weight_lists], (edge[0],edge[1]))
        if match_index >= 0:
            edge_weight_lists[match_index][1]['penwidth'] += 1
        else:
            edge_weight_lists.append([(edge[0],edge[1]), {'penwidth': 1}])
    return edge_weight_lists


def create_graph(edge_lists, node_correction, penwidth_correction):
    G = pgv.AGraph(directed=True,strict=False,rankdir='LR')
    # edge_color = '#40e0d6cc'
    edge_color = '#ff50a6cc'
    G.edge_attr['color'] = edge_color
    G.edge_attr['fillcolor'] = edge_color
    G.node_attr['style'] = 'filled'
    G.node_attr['color'] = '#000000'
    # G.node_attr['color'] = '#aaaaaa'
    # G.node_attr['color'] = '#00000015'
    G.node_attr['fillcolor'] = '#00000000'

    # edge_lists = [(1,1),(1,2),(2,1),(2,3),(1,3),(3,1),(3,4),(3,5),(3,6),(4,6),(7,1),(8,6),(6,9),(4,10),(6,11),(4,12),(13,12),(14,5),(15,3),(15,2),(7,10)]

    # nodeの重み付け情報取得
    node_weight_list = collections.Counter(itertools.chain.from_iterable(edge_lists)).most_common()
    # [(1, 7), (3, 7),...]

    # node 追加
    # for node_datum in node_weight_list:
    #     node = node_datum[0]
    #     count = node_datum[1]
    #     print('node:',node, '\n')
    #     print('count:',count, '\n')
    #     node_weight = count * node_correction
    #     G.add_node(node, fixedsize=True, width=node_weight, height=node_weight)
        # e.g. G.add_node(1,width=0.7, height=0.7)

    # edgeの重み付け情報取得
    edge_weight_lists = create_edge_weight_lists(edge_lists)
    # [[(1, 1), {'penwidth': 1}], [(1, 2), {'penwidth': 1}],...]

    # edge 追加
    survived_nodes = []
    for edge, penwidth in edge_weight_lists:
        # エッジの枝刈り
        if penwidth['penwidth'] <= edge_cut_point:
            continue

        for i in range(2):
            match_index = search_match_index(survived_nodes, edge[i])
            if match_index < 0:
                survived_nodes.append(edge[i])
        weight = penwidth['penwidth'] * penwidth_correction
        G.add_edge(edge, penwidth=weight)

    # ノード重み付け
    # ここのアルゴリズム考え直すべき
    for survived_node in survived_nodes:
        for node_datum in node_weight_list:
            node = node_datum[0]
            if survived_node == node:
                count = node_datum[1]
                node_weight = count * node_correction
                G.add_node(node, fixedsize=True, width=node_weight, height=node_weight, fontsize=fontsize)
                print('(node,count) = ({},{})'.format(node,count))


    # 図示
    # G.graph_attr['epsilon']='0.001'# 終了条件
    # print(G.string()) # グラフ情報表示
    G.layout(layout) # レイアウト指定
    G.draw('directed_graph.png')


def main():
    json_file = open('all_edge_lists.json','r')
    flow_data = json.load(json_file)
    all_edge_lists = flow_data['all_edge_lists']
    create_graph(all_edge_lists, node_correction, penwidth_correction)


if __name__ == '__main__':
    main()
