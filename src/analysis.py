import pandas as pd
import click
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
import math
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import ConfusionMatrixDisplay

@click.command()
@click.option('--data', type=str, help="Path to clean and preprocessed data")
@click.option('--train-data', type=str, help="Path to training data")
@click.option('--test-data', type=str, help="Path to testing data")
@click.option('--output_path', type=str, help="Path to output object")

def analyze_data(data, train_data, test_data, output_path):
    """EDA Analysis Portion """
    # obtaining summary of dataset
    data_summary = data.describe(include = 'all')
    print(data_summary)
    click.echo(f"Data Summary")

    # creating X_train split
    X_train = train_data.drop(target, axis=1)
    # creating y_train split
    y_train = train_data[target]
    # creating X_test split
    X_test = test_data.drop(target, axis=1)
    # creating y_test split
    y_test = test_data[target]


"""Cross validation Function"""
def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):

    scores = cross_validate(model, X_train, y_train, **kwargs)

    mean_scores = pd.DataFrame(scores).mean()
    std_scores = pd.DataFrame(scores).std()
    out_col = []

    for i in range(len(mean_scores)):
        out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores.iloc[i], std_scores.iloc[i])))

    return pd.Series(data=out_col, index=mean_scores.index)

"""Results Dictionary to store results """
results_dict = {}


"""Dummy Classifier"""

# defining dummy classifier model
dummy = DummyClassifier()

# defining dummy classifier pipeline
dummy_pipe = make_pipeline(preprocessor, dummy)

# fitting dummy model and reporting results to the results_dict
results_dict["dummy"] = mean_std_cross_val_scores(
    dummy_pipe, X_train, y_train, cv=10, return_train_score=True
)

# viewing dummy classifier results 
results_df = pd.DataFrame(results_dict).T
click.echo("Dummy Complete!")

"""KNN Classifier"""

##################
## Finding best K


n = math.sqrt(len(y_test))
knn_results = {}

# Range of k values to test
k_values = range(1, n-1)
# Loop over each k value, create a kNN model, and perform cross-validation
for k in k_values:
    knn_model = KNeighborsClassifier(n_neighbors=k, p=2, metric='euclidean')
    knn_pipe = make_pipeline(preprocessor, knn_model)
    scores = cross_validate(knn_pipe, X_train, y_train, cv=10, return_train_score=True, scoring='accuracy')
    mean_score = scores['test_score'].mean()
    std_score = scores['test_score'].std()
    knn_results[k] = (mean_score, std_score)

# Convert the results dictionary to a DataFrame for easier analysis
knn_results_df = pd.DataFrame(knn_results, index=['mean_accuracy', 'std_accuracy']).T

# Find the k value with the highest mean accuracy
best_k = knn_results_df['mean_accuracy'].idxmax()
best_score = knn_results_df.loc[best_k, 'mean_accuracy']
best_std = knn_results_df.loc[best_k, 'std_accuracy']
click.echo("Best K Complete!")


####################
# Make the kNN model
kNN_model = KNeighborsClassifier(n_neighbors=best_k,p=2,metric='euclidean')

# defining kNN classifer pipeline
knn_pipe = make_pipeline(preprocessor, kNN_model)

# fitting kNN model and reporting results to the results_dict
results_dict["knn"] = mean_std_cross_val_scores(
    knn_pipe, X_train, y_train, cv=10, return_train_score=True
)

# viewing kNN classifier results 
results_df = pd.DataFrame(results_dict).T
click.echo("KNN Complete!")

"""SVM RBF Model"""

#defining SVM RBF classifier 
SVM = SVC(gamma = 0.01)

#defining SVM RBF pipeline 
svm_pipe = make_pipeline(preprocessor, SVM)

#fitting SVM model and appending results 
results_dict['SVM'] = mean_std_cross_val_scores(svm_pipe, X_train, y_train, cv = 10, return_train_score = True
                                               )
#displaying SVM RBF classifier results 
results_df = pd.DataFrame(results_dict).T
click.echo("SVM RBF Complete!")


"""Random Forest Model"""

# defining a Random Forests Classifier
random_forest = RandomForestClassifier(n_estimators=50, max_depth = 50, random_state = 123)

# defining a pipeline that uses the Random Forest Classifier
randomfr_pipe = make_pipeline(preprocessor, random_forest) 

# fitting dummy model and reporting results to the results_dict
results_dict["random_forest"] = mean_std_cross_val_scores(
    randomfr_pipe, X_train, y_train, cv=10, return_train_score=True
)

# viewing dummy classifier results 
results_df = pd.DataFrame(results_dict).T
click.echo("Random Forests Complete!")
results_df.savefig(f'ModelResults.png')

"""Confusion Matrix"""


randomfr_pipe.fit(X_train, y_train)
randomfr_pipe.predict(X_test)
cm = ConfusionMatrixDisplay.from_estimator(
    randomfr_pipe, X_test, y_test, values_format="d", display_labels=["No Revenue", "Revenue"]
)

cm.ax_.set_title("Figure 11: Random Forests Confusion Matrix")
cm.savefig(f'RandomForest_ConfusionMatrix.png')
cm.close()
click.echo("Confusion Matrix Complete!")