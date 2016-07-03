import scipy.io as sio

folder = "./database/"
data_base_name = 'SummaryDatabase.mat'
data_base = sio.loadmat(folder + data_base_name)

pre_spatial_set = data_base['Pre_SpatialSet']
pre_feature_sets = data_base['Pre_FeatureSets']
spike_train_SpatialSet = data_base['SPtrain_SpatialSet']

