from sklearn.cluster import KMeans
from sklearn import metrics


class K_Means(object):

    @classmethod
    def fit_predict(cls, X, n_cluster=10):
        cluster_model = KMeans(n_clusters=n_cluster, random_state=9)
        x_pred = cluster_model.fit_predict(X)
        return x_pred
