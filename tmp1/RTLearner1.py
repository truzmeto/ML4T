"""
A simple wrapper for Decision Tree Regression. (c) 2018 T. Ruzmetov
"""
import numpy as np
import pandas as pd
from copy import deepcopy
from collections import Counter
from operator import itemgetter
from random import randint


class RTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = np.array([])
        
    def author(self):
        return 'truzmetov3'
     
    def get_split_indices(self, dataX, num_samps):
        """
        fvdflkjnv;dfkmv
        """
        feature_index = randint(0, dataX.shape[1] - 1)
        split_index1 = randint(0, num_samps - 1)
        split_index2 = randint(0, num_samps - 1)
        split_val = (dataX[split_index1][feature_index]
                     + dataX[split_index2][feature_index])/2
        left_indices = [i for i in xrange(dataX.shape[0])
                        if dataX[i][feature_index] <= split_val]
        right_indices = [i for i in xrange(dataX.shape[0])
                        if dataX[i][feature_index] > split_val]
        return left_indices, right_indices, feature_index, split_val

    
    
    def buildTree(self, dataX, dataY, rootX=[], rootY=[]):
        """
        This is eager DT algorithm for regression that chooses best feature for splitting based
        on its highest abs(corr(X_i,Y)). Median of the chosen feature is used as splitting value.
        If all features have the same abs(corr(X_i,Y)), choose the first feature and pass.
        If the best feature can't split the target into two groups, choose the next best feature; 
        if none of the features do, return the leaf.
        
        Returns:
        tree: A numpy ndarray. Each row represents a node and four columns are feature indices 
        (int type; index for a leaf is -1), splitting values, and starting rows, from the current 
        root, for its left and right subtrees (if any)
        """

        num_feats = dataX.shape[1]
        num_samps = dataX.shape[0]

        #return the most common value from the root of current node if no sample left
        if num_samps < 1:
            return np.array([-1, Counter(rootY).most_common(1)[0][0], np.nan, np.nan])

        # return leaf, if there are <= leaf_size samples 
        if num_samps <= self.leaf_size:
            return np.array([-1, Counter(dataY).most_common(1)[0][0], np.nan, np.nan])

        # return leaf, if all data in dataY are the same
        if num_samps <= len(np.unique(dataY)) == 1:
            return np.array([-1, Counter(dataY).most_common(1)[0][0], np.nan, np.nan])
        
        remain_feats_for_split = list(range(num_feats))

        # Choose a random feature, and a random split value
        left_index, right_index, feature_index, split_val = self.get_split_indices(dataX, num_samps)

       ############################################################################################ 
        #feat_corr_i = 0
        #while len(remain_feats_for_split) > 0:
        #    best_feat_i = feature_index
         
            # break out of the loop if split is successful            
        #    if len(left_index) < 1 or len(right_index) < 1:
        #        break
        #    remain_feats_for_split.remove(best_feat_i)
        #    feat_corr_i += 1

        while len(left_indices) < 1 or len(right_indices) < 1:
            left_index, right_index, feature_index, split_val = \
                      self.get_split_indices(x_train, num_instances


        ############################################################################################
       
        #If we complete the while loop and run out of features to split, return leaf
        #if len(remain_feats_for_split) == 0:
        #    return np.array([-1, Counter(dataY).most_common(1)[0][0], np.nan, np.nan])

        # Build left and right branches and the root                    
        lefttree = self.buildTree(dataX[left_index], dataY[left_index], dataX, dataY)
        righttree = self.buildTree(dataX[right_index], dataY[right_index], dataX, dataY)

        # Set the starting row for the right subtree of the current root
        if lefttree.ndim == 1:
            righttree_start = 2 # The right subtree starts 2 rows down
        elif lefttree.ndim > 1:
            righttree_start = lefttree.shape[0] + 1

            
        root = np.array([feature_index, split_val, 1, righttree_start])
        return np.vstack((root, lefttree, righttree))
       
    def recur_search(self, point, row):
        """A private function to be used with query. It recursively searches 
        the decision tree matrix and returns a predicted value for point
        Parameters:
        point: A numpy 1D array of test query
        row: The row of the decision tree matrix to search
    
        Returns 
        pred: The predicted value
        """

        # Get the feature on the row and its corresponding splitting value
        feat, split_val = self.tree[row, 0:2]
        
        # If splitting value of feature is -1, we have reached a leaf so return it
        if feat == -1:
            return split_val

        # If the corresponding feature's value from point <= split_val, go to the left tree
        elif point[int(feat)] <= split_val:
            pred = self.recur_search(point, row + int(self.tree[row, 2]))

        # Otherwise, go to the right tree
        else:
            pred = self.recur_search(point, row + int(self.tree[row, 3]))
        
        return pred


    def addEvidence(self, dataX, dataY):
        """Add training data to learner
        Parameters:
        dataX: A numpy ndarray of X values of data to add
        dataY: A numpy 1D array of Y training values
        Returns: An updated tree matrix for DTLearner
        """

        new_tree = self.buildTree(dataX, dataY)

        # If self.tree is currently None, simply assign new_tree to it
        if self.tree is None:
            self.tree = new_tree

        # Otherwise, append new_tree to self.tree
        else:
            self.tree = np.vstack((self.tree, new_tree))
        
        # If there is only a single row, expand tree to a numpy ndarray for consistency
        if len(self.tree.shape) == 1:
            self.tree = np.expand_dims(self.tree, axis=0)
        
        if self.verbose:
            self.get_learner_info()
        
        
    def query(self, points):
        """Estimates a set of test points given the model we built
        
        Parameters:
        points: A numpy ndarray of test queries
        Returns: 
        preds: A numpy 1D array of the estimated values
        """

        preds = []
        for point in points:
            preds.append(self.recur_search(point, row=0))
        return np.asarray(preds)


    def get_learner_info(self):
        print ("Info about this Decision Tree Learner:")
        print ("leaf_size =", self.leaf_size)
        if self.tree is not None:
            print ("tree shape =", self.tree.shape)
            print ("tree as a matrix:")
            # Create a dataframe from tree for a user-friendly view
            df_tree = pd.DataFrame(self.tree, columns=["factor", "split_val", "left", "right"])
            df_tree.index.name = "node"
            print (df_tree)
        else:
            print ("Tree has no data")


if __name__=="__main__":
    print "This is a Decision Tree Learner\n"