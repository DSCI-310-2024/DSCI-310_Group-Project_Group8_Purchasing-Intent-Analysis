#author: Calvin Choi, Nour Abdelfattah, Sana Shams, Sai Pusuluri
#date: 2024-04-09

"""
Analyzes preprocessed training and testing data by fitting a set of classifiers, including
Dummy, k-Nearest Neighbors (kNN), Support Vector Machine (SVM), and Random Forest, to compare their
cross-validation scores. It also evaluates the Random Forest classifier on the test set,
generates feature importances and a confusion matrix for visualization.

Usage:
    analysis.py <preprocessed_train_data> <preprocessed_test_data> <output_path>

Arguments:
    preprocessed_train_data -- Path to the CSV file containing preprocessed training data.
    preprocessed_test_data -- Path to the CSV file containing preprocessed testing data.
    output_path -- Directory where the output files will be saved. This includes model comparison results,
                   feature importances, performance metrics of the Random Forest classifier, and its confusion matrix visualization.

The script will generate and save the following outputs in the specified output directory:
    - Model comparison results across different classifiers.
    - Feature importances from the Random Forest classifier.
    - Performance metrics (Precision, Recall, Accuracy, F1 Score) for the Random Forest classifier on the test data.
    - A confusion matrix for the Random Forest classifier's predictions on the test set.
"""

import pandas as pd
import click
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, accuracy_score, f1_score
import numpy as np

import matplotlib.pyplot as plt

from py_predpurchase.function_model_cross_val import model_cross_validation
from py_predpurchase.function_feature_importance import get_feature_importances 
from py_predpurchase.function_classification_metrics import calculate_classification_metrics

@click.command()
@click.argument('preprocessed_train_data', type=str)
@click.argument('preprocessed_test_data', type=str)
@click.argument('output_path', type=str)
def analyze_data(preprocessed_train_data, preprocessed_test_data, output_path):
    # Load the data
    train_data = pd.read_csv(preprocessed_train_data)
    test_data = pd.read_csv(preprocessed_test_data)
    X_train = train_data.drop('Revenue', axis=1)
    y_train = train_data['Revenue']
    X_test = test_data.drop('Revenue', axis=1)
    y_test = test_data['Revenue']

    # Perform cross-validation and get results
    results_dict = model_cross_validation(train_data, test_data, 'Revenue', 13, 0.01)
    
    # Save the model comparison results
    results_df = pd.DataFrame(results_dict).T
    results_df.to_csv(f"{output_path}/model_comparison_results.csv")
    click.echo("Model comparison results saved to results folder.")

    random_forest = RandomForestClassifier(n_estimators=50, max_depth=50, random_state=123)
    random_forest.fit(X_train, y_train)

    # # Feature Importance using imported function
    # feature_importances_df = get_feature_importances(random_forest, X_train.columns)
    # feature_importances_df.to_csv(f"{output_path}/feature_importances.csv")
    # click.echo("Feature importances saved to results folder.")


    # Metrics for Random Forest on test data
    y_pred = random_forest.predict(X_test)
    metrics = calculate_classification_metrics(y_test, y_pred)
    metrics_df = pd.DataFrame(metrics, index=[0])
    metrics_df.to_csv(f"{output_path}/random_forest_metrics.csv", index=False)
    click.echo("Performance metrics saved to results folder.")

    # Confusion Matrix for Random Forest
    cm_display = ConfusionMatrixDisplay.from_estimator(random_forest, X_test, y_test)
    plt.figure(figsize=(10, 10))
    cm_display.plot()
    plt.title('Random Forest Confusion Matrix')
    plt.savefig(f"{output_path}/random_forest_confusion_matrix.png")
    plt.close()
    click.echo("Confusion matrix saved to results folder.")

def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
    scores = cross_validate(model, X_train, y_train, **kwargs)
    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    return pd.Series({col: f"{mean:.3f} (+/- {std:.3f})" for col, mean, std in zip(mean_scores.index, mean_scores, std_scores)})

if __name__ == '__main__':
    analyze_data()


