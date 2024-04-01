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

    results_dict = {}

    # Dummy Classifier
    dummy = DummyClassifier(strategy='most_frequent')
    results_dict["dummy"] = mean_std_cross_val_scores(dummy, X_train, y_train, cv=10, return_train_score=True)

    # kNN Classifier
    best_k = 13
    knn = KNeighborsClassifier(n_neighbors=best_k)
    results_dict["knn"] = mean_std_cross_val_scores(knn, X_train, y_train, cv=10, return_train_score=True)

    # SVM Classifier
    svm = SVC(gamma=0.01)
    results_dict["SVM"] = mean_std_cross_val_scores(svm, X_train, y_train, cv=10, return_train_score=True)

    # Random Forest Classifier
    random_forest = RandomForestClassifier(n_estimators=50, max_depth=50, random_state=123)
    results_dict["random_forest"] = mean_std_cross_val_scores(random_forest, X_train, y_train, cv=10, return_train_score=True)

    # Comapring results across all models
    results_df = pd.DataFrame(results_dict).T
    results_df.to_csv(f"{output_path}/model_comparison_results.csv")
    click.echo("Model comparison results saved to results folder.")

    # Feature Importance from Random Forest
    random_forest.fit(X_train, y_train)
    feature_importances = pd.Series(random_forest.feature_importances_, index=X_train.columns)
    feature_importances_sorted = feature_importances.sort_values(ascending=False)
    feature_importances_sorted.to_csv(f"{output_path}/feature_importances.csv")
    click.echo("Feature importances saved to results folder.")

    # Metrics for Random Forest on test data
    y_pred = random_forest.predict(X_test)
    metrics = {
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred)
    }
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


#import pandas as pd
# import click
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, OneHotEncoder
# from sklearn.compose import make_column_transformer
# import math
# import matplotlib.pyplot as plt
# from sklearn.dummy import DummyClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.svm import SVC
# from sklearn.metrics import ConfusionMatrixDisplay
# from sklearn.pipeline import make_pipeline
# from sklearn.model_selection import cross_validate
# from sklearn.metrics import confusion_matrix
# import numpy as np


# @click.command()
# @click.argument('processed_train_data', type=str)
# @click.argument('processed_test_data', type=str)
# @click.argument('output_path', type=str)

# def analyze_data(processed_train_data, processed_test_data, output_path):
    
#     train_data = pd.read_csv(processed_train_data)
#     test_data = pd.read_csv(processed_test_data)

#     target = 'Revenue'

#     # creating X_train split
#     X_train = train_data.drop(target, axis=1)
#     # creating y_train split
#     y_train = train_data[target]
#     # creating X_test split
#     X_test = test_data.drop(target, axis=1)
#     # creating y_test split
#     y_test = test_data[target]


#     # Function to perform cross-validation and return mean/std scores
#     def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
#         scores = cross_validate(model, X_train, y_train, **kwargs)
#         mean_scores = pd.DataFrame(scores).mean()
#         std_scores = pd.DataFrame(scores).std()
#         return pd.Series({col: f"{mean:.3f} (+/- {std:.3f})" for col, mean, std in zip(mean_scores.index, mean_scores,
#                                                                                        std_scores)})

#     # Dictionary to store results
#     results_dict = {}

#     # Dummy Classifier
#     dummy = DummyClassifier()
#     results_dict["Dummy"] = mean_std_cross_val_scores(dummy, X_train, y_train, cv=5, return_train_score=True)

#     # KNN Classifier - Finding best K
#     sqrt_len = int(np.sqrt(len(y_train)))
#     k_values = range(1, min(50, sqrt_len))  # Limiting to a sensible range for k
#     best_mean_score = 0
#     best_k = 1

#     for k in k_values:
#         knn_model = KNeighborsClassifier(n_neighbors=k)
#         scores = cross_validate(knn_model, X_train, y_train, cv=5, scoring='accuracy')
#         mean_score = np.mean(scores['test_score'])
#         if mean_score > best_mean_score:
#             best_mean_score = mean_score
#             best_k = k

#     # Retrain and evaluate best KNN model
#     best_knn_model = KNeighborsClassifier(n_neighbors=best_k)
#     results_dict["KNN_best_k"] = mean_std_cross_val_scores(best_knn_model, X_train, y_train, cv=5,
#                                                            return_train_score=True)
#     click.echo(f"Best K for KNN: {best_k} with mean accuracy: {best_mean_score:.3f}")

#     # SVM RBF Classifier
#     svm_rbf = SVC(kernel='rbf', gamma= 0.01)
#     results_dict["SVM_RBF"] = mean_std_cross_val_scores(svm_rbf, X_train, y_train, cv=5, return_train_score=True)

#     # Random Forest Classifier
#     random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
#     results_dict["Random_Forest"] = mean_std_cross_val_scores(random_forest, X_train, y_train, cv=5,
#                                                               return_train_score=True)

#     # Convert results to DataFrame and save to CSV
#     results_df = pd.DataFrame(results_dict).T
#     results_df.to_csv(f"{output_path}/model_comparison_results.csv", index=True)
#     click.echo("Model comparison results saved.")

#     # Fit the Random Forest model and generate confusion matrix
#     random_forest.fit(X_train, y_train)
#     y_pred = random_forest.predict(X_test)
#     cm = confusion_matrix(y_test, y_pred)
#     disp = ConfusionMatrixDisplay(confusion_matrix=cm)
#     disp.plot()
#     plt.title('Random Forest Confusion Matrix')
#     plt.savefig(f"{output_path}/random_forest_confusion_matrix.png")
#     plt.close()
#     click.echo("Confusion matrix saved.")

# if __name__ == '__main__':
#     analyze_data()