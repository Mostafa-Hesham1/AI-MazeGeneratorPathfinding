import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class DecisionTreeNode:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain
        self.value = value

    def is_leaf_node(self):
        return self.left is None and self.right is None

class DecisionTreeClassifier:
    def __init__(self, min_samples_split=2, max_depth=2, feature_names=None):
        self.root = None
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.feature_names = feature_names
    
    def build_tree(self, dataset, curr_depth=0):
        X, Y = dataset[:,:-1], dataset[:,-1]
        num_samples, num_features = np.shape(X)
        if num_samples >= self.min_samples_split and curr_depth <= self.max_depth:
            best_split = self.get_best_split(dataset, num_samples, num_features)
            if best_split["info_gain"] > 0:
                left_subtree = self.build_tree(best_split["dataset_left"], curr_depth + 1)
                right_subtree = self.build_tree(best_split["dataset_right"], curr_depth + 1)
                return DecisionTreeNode(best_split["feature_index"], best_split["threshold"], 
                                        left_subtree, right_subtree, best_split["info_gain"])
        leaf_value = self.calculate_leaf_value(Y)
        return DecisionTreeNode(value=leaf_value)

    def get_best_split(self, dataset, num_samples, num_features):
        best_split = {}
        max_info_gain = -float("inf")
        for feature_index in range(num_features):
            feature_values = dataset[:, feature_index]
            possible_thresholds = np.unique(feature_values)
            for threshold in possible_thresholds:
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)
                if len(dataset_left) > 0 and len(dataset_right) > 0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    curr_info_gain = self.information_gain(y, left_y, right_y)
                    if curr_info_gain > max_info_gain:
                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = curr_info_gain
                        max_info_gain = curr_info_gain
        return best_split

    def split(self, dataset, feature_index, threshold):
        dataset_left = np.array([row for row in dataset if row[feature_index] <= threshold])
        dataset_right = np.array([row for row in dataset if row[feature_index] > threshold])
        return dataset_left, dataset_right

    def information_gain(self, parent, l_child, r_child):
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)
        gain = self.entropy(parent) - (weight_l*self.entropy(l_child) + weight_r*self.entropy(r_child))
        return gain

    def entropy(self, y):
        class_labels = np.unique(y)
        entropy = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            entropy -= p_cls * np.log2(p_cls)
        return entropy

    def calculate_leaf_value(self, Y):
        Y = list(Y)
        return max(Y, key=Y.count)

    def fit(self, X, Y):
        Y = Y.reshape(-1, 1)
    
        dataset = np.concatenate((X, Y), axis=1)
    
        self.root = self.build_tree(dataset)


    def predict(self, X):
        return [self.make_prediction(x, self.root) for x in X]

    def make_prediction(self, x, tree):
        if tree.value is not None: 
            return tree.value
        feature_val = x[tree.feature_index]
        if feature_val <= tree.threshold:
            return self.make_prediction(x, tree.left)
        else:
            return self.make_prediction(x, tree.right)



    
    def print_tree(self):
        self._print_tree(self.root)


        accuracy = self.calculate_accuracy(X_test, Y_test)
        print(f"\nAccuracy: {accuracy:.2%}")

    def _print_tree(self, node, depth=0):
        indent = "  " * depth
        if node.is_leaf_node():
            print(f"{indent}Class: {node.value}")
        else:
            feature_name = self.feature_names[node.feature_index]
            print(f"{indent}If {feature_name} <= {node.threshold}:")
            self._print_tree(node.left, depth + 1)

            print(f"{indent}Else:")
            self._print_tree(node.right, depth + 1)
    

    def calculate_accuracy(self, X_test, Y_test):
        predictions = self.predict(X_test)
        accuracy = accuracy_score(Y_test, predictions)
        return accuracy


iris_df = pd.read_csv('Iris.csv')

X = iris_df[['PetalLengthCm', 'PetalWidthCm', 'SepalLengthCm', 'SepalWidthCm']].values
Y = iris_df['Species'].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

feature_names = ['PetalLengthCm', 'PetalWidthCm', 'SepalLengthCm', 'SepalWidthCm']
custom_dt_classifier = DecisionTreeClassifier(max_depth=10, feature_names=feature_names)
custom_dt_classifier.fit(X_train, Y_train)

custom_dt_classifier.print_tree()
