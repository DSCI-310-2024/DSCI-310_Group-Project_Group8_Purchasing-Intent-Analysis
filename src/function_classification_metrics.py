from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

def calculate_classification_metrics(y_true, y_pred):
    """
    Calculates classification metrics for model predictions including precision, 
    recall, accuracy and F1 scores. 
    
    Parameters:
    - y_true: pd.Series, true target values in a dataset
    - y_pred: pd.Series, predicted target values by the model.
    
    Returns:
    - dict, containing precision, recall, accuracy, and F1 score.
    """
    metrics = {
        'Precision': precision_score(y_true, y_pred, average='weighted'),
        'Recall': recall_score(y_true, y_pred, average='weighted'),
        'Accuracy': accuracy_score(y_true, y_pred),
        'F1 Score': f1_score(y_true, y_pred, average='weighted')
    }
    return metrics