"""
Script to create plots for Hiearchical clustering using Ward's method
"""


import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import os
import sys
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.image import grid_to_graph

#from glm import glm, glm_diagnostics

project_path          = "../../"
path_to_data          = project_path+"data/ds009/"
location_of_images    = project_path+"images/"
location_of_functions = project_path+"code/utils/functions/" 
final_data            = "../data/"
behav_suffix           = "/behav/task001_run001/behavdata.txt"
t_data           =  final_data + '/t_stat/'
p_data           =  final_data + '/p-values/'


#sys.path.append(os.path.join(os.path.dirname(__file__), "../functions/"))
sys.path.append(location_of_functions)

sub_list = os.listdir(path_to_data)
sub_list = [i for i in sub_list if 'sub' in i]

from hypothesis import t_stat
from Image_Visualizing import present_3d, make_mask
from tgrouping import t_grouping_neighbor

i = 'sub001'

#####################################
##########    Clustering   ##########
#####################################

t_stat = np.load(t_data+i+"_tstat.npy")
mask = nib.load(path_to_data+i+'/anatomy/inplane001_brain_mask.nii.gz')
mask_data = mask.get_data()

data_new= make_mask(t_stat, mask_data, fit=True)[...,19:22]


X = np.reshape(data_new, (-1, 1))

connectivity = grid_to_graph(n_x= data_new.shape[0], n_y = data_new.shape[1], n_z = data_new.shape[2])

n_clusters = 3 # number of regions
ward = AgglomerativeClustering(n_clusters=n_clusters,
        linkage='ward', connectivity=connectivity).fit(X)
label = np.reshape(ward.labels_, data_new.shape)

label_mean = np.zeros(n_clusters)
center = list()


#####################################
########## Final Output    ##########
#####################################

total=np.zeros((3*64,3*64))

ward = label
t_stat = t_stat

prop_t = 0.15

rachels_ones = np.ones((64, 64, 34))
fitted_mask = make_mask(rachels_ones, mask_data, fit = True)
fitted_mask[fitted_mask > 0] = 1
neighbors=1
t_cluster = t_grouping_neighbor(t_stat, fitted_mask, prop_t, neighbors = neighbors, prop = True, abs_on = True, binary = True, off_value = 0, masked_value = .5)[0]
t_cluster = t_cluster[...,19:22]
t_final = t_stat[...,19:22]

for i in range(ward.shape[-1]):
    total[(i*64):((i+1)*64),0:64]=ward[...,i]
    
for i in range(t_final.shape[-1]):
    total[(i*64):((i+1)*64),64:128]=t_final[...,i]
    
for i in range(t_cluster.shape[-1]):
    total[(i*64):((i+1)*64),128:192]=t_cluster[...,i]











