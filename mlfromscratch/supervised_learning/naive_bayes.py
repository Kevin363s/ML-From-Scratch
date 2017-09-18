from __future__ import division, print_function
from sklearn import datasets
import matplotlib.pyplot as plt
import math
import sys
import os
import numpy as np
import pandas as pd

from mlfromscratch.utils.data_manipulation import train_test_split, normalize
from mlfromscratch.utils.data_operation import accuracy_score
from mlfromscratch.unsupervised_learning import PCA
from mlfromscratch.utils import Plot


class NaiveBayes():
    """The Gaussian Naive Bayes classifier. """
    def __init__(self):
        self.classes = None
        self.X = None
        self.y = None
        # Gaussian prob. distribution parameters
        self.parameters = []

    def fit(self, X, y):
        self.X = X
        self.y = y
        self.classes = np.unique(y)
        # Calculate the mean and variance of each feature for each class
        for i in range(len(self.classes)):
            c = self.classes[i]
            # Only select the rows where the species equals the given class
            x_where_c = X[np.where(y == c)]
            # Add the mean and variance for each feature
            self.parameters.append([])
            for j in range(len(x_where_c[0, :])):
                col = x_where_c[:, j]
                parameters = {}
                parameters["mean"] = col.mean()
                parameters["var"] = col.var()
                self.parameters[i].append(parameters)

    def _calculate_probability(self, mean, var, x):
        """ Gaussian probability distribution """
        coeff = (1.0 / (math.sqrt((2.0 * math.pi) * var)))
        exponent = math.exp(-(math.pow(x - mean, 2) / (2 * var)))
        return coeff * exponent

    def _calculate_prior(self, c):
        """ Calculate the prior of class c (samples where class == c / total number
        of samples)"""
        # Selects the rows where the class label is c
        x_where_c = self.X[np.where(self.y == c)]
        n_class_instances = np.shape(x_where_c)[0]
        n_total_instances = np.shape(self.X)[0]
        return n_class_instances / n_total_instances

    def _classify(self, sample):
        """ Classify using Bayes Rule, P(Y|X) = P(X|Y)*P(Y)/P(X)
        P(X|Y) - Probability. Gaussian distribution (given by calculate_probability)
        P(Y) - Prior (given by calculate_prior)
        P(X) - Scales the posterior to the range 0 - 1 (ignored)
        Classify the sample as the class that results in the largest P(Y|X)
        (posterior)
        """
        posteriors = []
        # Go through list of classes
        for i in range(len(self.classes)):
            c = self.classes[i]
            prior = self._calculate_prior(c)
            posterior = prior
            # multiply with the additional probabilties
            # Naive assumption (independence):
            # P(x1,x2,x3|Y) = P(x1|Y)*P(x2|Y)*P(x3|Y)
            for j, params in enumerate(self.parameters[i]):
                sample_feature = sample[j]
                mean = params["mean"]
                var = params["var"]
                # Determine P(x|Y)
                prob = self._calculate_probability(mean, var, sample_feature)
                # Multiply with the rest
                posterior *= prob
            # Total probability = P(Y)*P(x1|Y)*P(x2|Y)*...*P(xN|Y)
            posteriors.append(posterior)
        # Get the largest probability and return the class corresponding
        # to that probability
        index_of_max = np.argmax(posteriors)
        max_value = posteriors[index_of_max]

        return self.classes[index_of_max]

    def predict(self, X):
        """ Predict the class labels corresponding to the
        samples in X"""
        y_pred = []
        for sample in X:
            y = self._classify(sample)
            y_pred.append(y)
        return y_pred

