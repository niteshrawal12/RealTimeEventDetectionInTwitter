#Single-window based Event detection method
#implemented 19KDD-Real-time Event Detection on Social Data Streams paper
################# AKP-19RTED(Louvain Method)#############################
##########################################################################
from __future__ import division
import collections
import math
import matplotlib.pyplot as plt
import ast
import networkx as nx
import community as community_louvain
import matplotlib.cm as cm
from collections import defaultdict
##########################
from numpy import dot
from numpy.linalg import norm
def cos_sim(a,b):
    # print("a= ",a)
    # print("b= ",b)
    c_sim= round(dot(a, b)/(norm(a)*norm(b)),2)
    return c_sim
#############################
import time
# start_time = time.clock()
start = time.perf_counter()
##############################
tweet_dict = {}
sim_matrix = []
total_tweet_length = 0
total_user_list =[]
total_entity_list =[]
with open('./input_file.txt') as file:
    for line in file:
        if not line.strip():
            continue
        else:
            line = line.split("\t")
            # print("type of line",type(line))
            take_string =line[3].strip()  #For conversion of String --> List
            tweet_dict[line[0]] = {'text':line[2].split(),'uid': line[1], 'entities': ast.literal_eval(take_string)} #Dictionary Creation
            # print("type of line[0]", type(line[0])) #String
            # print("type of line[1]", type(line[1].split())) #List
            # print("type of line[2]", type(line[2].split())) #List
            # print("type of line[3]", type(ast.literal_eval(take_string))) #List
            total_tweet_length = total_tweet_length + len(line[2].split())
            total_user_list.extend(line[1].split())
            total_entity_list.extend(ast.literal_eval(take_string))
            # print("length of tweet", len(line[1].split()))
keys_list = list(tweet_dict.keys())
keys_list.sort()
print("List of Keys: ", keys_list)
print("No of Tweets: ", len(keys_list))
print("Tweet Dictionary: ",tweet_dict)
print("Total Entity List: ", len(total_entity_list), total_entity_list)
print("Unique Entity Set: ", len(set(total_entity_list)), set(total_entity_list))

############## Inverted_Index with Entity vector ###########
inv_index = {}
u_ent_list = list(set(total_entity_list))
for ent in u_ent_list:
    # print(word)
    vec =[] #Check wheather the entity present / absent in a tweet
    for tweet in keys_list:
        # print(tweet)
        if ent in tweet_dict[tweet]["entities"]:
            vec.append(1)
        else:
            vec.append(0)
    inv_index[ent] = vec
print("Inverted Index :", inv_index)

################ Entity Graph Generation ####################

node_list = list(inv_index.keys())
print(type(node_list),len(node_list), node_list)
EG = nx.Graph()
g_node_list = node_list #temp node list for removing duplicate nodes
EG.add_nodes_from(node_list) # Add all nodes
list_to_remove=[]
for node in node_list:
    # print("main node list =", node_list)
    # print("for- ",node)
    list_to_remove.append(node)
    # print("nodes to be removed : ",list_to_remove)
    check_list = list(set(g_node_list) - set(list_to_remove))
    # print("now length of node list = ", len(check_list),check_list)
    for nodex in check_list:
        sim = cos_sim(inv_index[node], inv_index[nodex])
        # print("check with- ", nodex, " sim =", sim)
        if sim >= 0.2:
            EG.add_edge(node,nodex, weight=sim)
            # print("Edge added between ",node,"--",nodex)
        else:
            continue
print(len(EG.nodes()), EG.nodes())
print(len(EG.edges()),EG.edges())
print("ADJ-List of EG: ",EG.adj)
pos = nx.spring_layout(EG, scale=1.2)
##### Draw nodes with labels
nx.draw(EG, pos, node_size=300, node_color='orange', with_labels=True)
edge_labels = dict([((u, v), d['weight'])
                        for u, v, d in EG.edges(data=True)])
####Draw edges with labels
nx.draw_networkx_edge_labels(EG, pos, font_size=7, edge_labels=edge_labels)
# plt.show()
plt.savefig("entitygraph.png")
plt.clf()
################ Community detection ##############
####### 1. Louvain Method ##################
def get_events_from_partition(P):
    event_dict = defaultdict(list)
    for key, val in sorted(P.items()):
        event_dict[val].append(key)
    return dict(event_dict)
print("\n\nCommunities extracted using Louvain Method")
print('------------------------------------------')
partition1 = community_louvain.best_partition(EG,weight='weight') # retuns dictionary
# print(type(partition))
print("Phase1-",partition1)
no_of_events = set(list(partition1.values()))
print("No_of_events =", len(no_of_events))
events = get_events_from_partition(partition1)
print("Extracted events are= ",events)
# draw the graph
pos = nx.spring_layout(EG)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition1.values()) + 1)
nx.draw_networkx_nodes(EG, pos, partition1.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition1.values()))
nx.draw_networkx_edges(EG, pos, alpha=0.5)
# nx.draw_networkx_edge_labels(EG,pos,edge_labels=labels, alpha=0.5)
plt.savefig("LM-event1.png")
plt.clf()
# compute the best partition
partition2 = community_louvain.best_partition(EG,weight='weight')
print("Phase2-",partition2)
no_of_events = set(list(partition2.values()))
print("No_of_events =", len(no_of_events))
events = get_events_from_partition(partition2)
print("Extracted events are= ",events)
# draw the graph
pos = nx.spring_layout(EG)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition2.values()) + 1)
nx.draw_networkx_nodes(EG, pos, partition2.keys(), node_size=80,
                       cmap=cmap, node_color=list(partition2.values()))
nx.draw_networkx_edges(EG, pos, alpha=0.5)
plt.savefig("LM-event2.png")
plt.clf()
print("--------------------------------------------------")
################################## Execution Time ##############
print("Total Execution time in sec tpc :", time.perf_counter()- start)
# print("Total Execution time in sec:",time.clock() - start_time)