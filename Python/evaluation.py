##############################################################################
# ENSEMBLE OF CLASSIFIER CHAINS                                              #
# Copyright (C) 2025                                                         #
#                                                                            #
# This code is free software: you can redistribute it and/or modify it under #
# the terms of the GNU General Public License as published by the Free       #
# Software Foundation, either version 3 of the License, or (at your option)  #
# any later version. This code is distributed in the hope that it will be    #
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of     #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General   #
# Public License for more details.                                           #
#                                                                            #
# Prof. Elaine Cecilia Gatto - UFLA - Lavras, Minas Gerais, Brazil           #
# Prof. Ricardo Cerri - USP - São Carlos, São Paulo, Brazil                  #
# Prof. Mauri Ferrandin - UFSC - Blumenau, Santa Catarina, Brazil            #
# Prof. Celine Vens - Ku Leuven - Kortrijik, West Flanders, Belgium          #
# PhD Felipe Nakano Kenji - Ku Leuven - Kortrijik, West Flanders, Belgium    #
#                                                                            #
# BIOMAL - http://www.biomal.ufscar.br                                       #
#                                                                            #
##############################################################################



########################################################################
#                                                                      #
########################################################################
import sys
import platform
import os

#FolderRoot = os.path.expanduser('~/HPML.ECC/Python')
#os.chdir(FolderRoot)
#current_directory = os.getcwd()
#sys.path.append('..')


import pandas as pd
import numpy as np

from collections import Counter
from sklearn.utils.multiclass import type_of_target

import warnings
from sklearn.exceptions import UndefinedMetricWarning

from sklearn.metrics import (
    accuracy_score, hamming_loss, zero_one_loss,
    average_precision_score, f1_score, precision_score,
    recall_score, jaccard_score, roc_auc_score, precision_recall_curve,
    precision_recall_fscore_support, roc_curve, auc, coverage_error, 
    label_ranking_loss)

import confusion_matrix as cm
import measures as ms


########################################################################
#                                                                      #
########################################################################
def multilabel_label_problem_measures(true_labels: pd.DataFrame, pred_labels: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates measures for label prediction problems in multi-label classification.

    Parameters:
    ----------
    true_labels (pd.DataFrame): The DataFrame containing the true binary labels (0 or 1) for each instance.
    
    pred_labels (pd.DataFrame): The DataFrame containing the predicted binary labels (0 or 1) for each instance.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing all the calculated metrics.

    Metrics Calculated:
    -------------------
    - Constant Label Problem (CLP)
    - Wrong Label Problem (WLP)
    - Missing Label Problem (MLP)

    Interpretation:
    ----------
    1. **Wrong Label Problem (WLP)**
        Definition: Measures the number of labels that are predicted but should not be. The ideal value is zero.        
        - **Low WLP**: Indicates fewer incorrect predictions of labels.
        - **High WLP**: Indicates that the classifier often predicts incorrect labels.
        - **Reference**: Rivolli, A., Soares, C., & Carvalho, A. C. P. de L. F. de. (2018). Enhancing 
        multilabel classification for food truck recommendation. Expert Systems. Wiley-Blackwell. 
        DOI: 10.1111/exsy.12304

    2. **Missing Label Problem (MLP)**
        Definition: Measures the proportion of labels that should have been predicted but were not. The ideal value is zero.        
        - **Low MLP**: Indicates that most of the relevant labels are predicted.
        - **High MLP**: Indicates that many relevant labels are missing in the predictions.
        - **Reference**: Rivolli, A., Soares, C., & Carvalho, A. C. P. de L. F. de. (2018). Enhancing 
        multilabel classification for food truck recommendation. Expert Systems. Wiley-Blackwell. 
        DOI: 10.1111/exsy.12304

    3. **Constant Label Problem (CLP)**
        Definition: Measures the occurrence where the same label is predicted for all instances. The ideal value is zero.        
        - **Low CLP**: Indicates that predictions vary and are more closely aligned with true labels.
        - **High CLP**: Indicates that the classifier predicts the same label for all instances.
        - **Reference**: Rivolli, A., Soares, C., & Carvalho, A. C. P. de L. F. de. (2018). Enhancing 
        multilabel classification for food truck recommendation. Expert Systems. Wiley-Blackwell. 
        DOI: 10.1111/exsy.12304
  

    Example Usage:
    --------------
    >>> result_df = multilabel_label_problem_measures(true_labels, pred_labels)
    >>> print(result_df)
    """

    matrix_confusion = cm.mlem_confusion_matrix(true_labels, pred_labels)

    clp = ms.mlem_clp(matrix_confusion)
    mlp = ms.mlem_mlp(matrix_confusion)
    wlp = ms.mlem_wlp(matrix_confusion)

    # Store all metrics in a dictionary
    metrics_dict = {    
        'clp': clp,
        'mlp': mlp,
        'wlp': wlp
    }

    # Convert dictionary to DataFrame
    # metrics_df = pd.DataFrame([metrics_dict])

    # Converter o dicionário em um DataFrame com colunas "Measure" e "Value"
    metrics_df = pd.DataFrame(list(metrics_dict.items()), columns=['Measure', 'Value'])

    return metrics_df



########################################################################
#                                                                      #
########################################################################
def multilabel_bipartition_measures(true_labels: pd.DataFrame, pred_labels: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates various evaluation metrics for multi-label classification.

    Parameters:
    ----------
    true_labels (pd.DataFrame): The DataFrame containing the true binary labels (0 or 1) for each instance.
    
    pred_labels (pd.DataFrame): The DataFrame containing the predicted binary labels (0 or 1) for each instance.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing all the calculated metrics.

    Metrics Calculated:
    -------------------
    - Accuracy
    - Hamming Loss
    - Zero-One Loss
    - F1 Score (macro, micro, weighted, samples)
    - Precision (macro, micro, weighted, samples)
    - Recall (macro, micro, weighted, samples)
    - Precision Recall F1 Support (macro, micro, weighted, samples)
    - Jaccard Score (macro, micro, weighted, samples)

    Interpretation:
    ----------------
    1. **Accuracy**
        Definition: The proportion of correctly predicted labels (both positive and negative) over 
        the total number of labels.
        - **High Accuracy**: Indicates that the classifier correctly predicted a high proportion of labels.
        - **Low Accuracy**: Indicates that the classifier made many incorrect predictions.
        - **Reference**: [Wikipedia: Accuracy and Precision](https://en.wikipedia.org/wiki/Accuracy_and_precision)

    2. **Hamming Loss**
        Definition: The fraction of labels that are incorrectly predicted, either due to false
        positives or false negatives, normalized by the total number of labels.    
        - **Low Hamming Loss**: Indicates fewer incorrect predictions.
        - **High Hamming Loss**: Indicates many incorrect predictions.
        - **Reference**: [Hamming Loss on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.hamming_loss.html)

    3. **Subset Accuracy**
        Definition: The proportion of instances for which the classifier predicted all the labels 
        exactly right (i.e., the predicted label set matches the true label set exactly).
        - **High Subset Accuracy**: Indicates that the classifier correctly predicted all labels for 
          many instances.
        - **Low Subset Accuracy**: Indicates that the classifier often missed some labels or included 
          incorrect labels.
        - **Reference**: [Subset Accuracy on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)

    4. **Zero-One Loss**
        Definition: The fraction of instances where the classifier’s prediction does not match the 
        true label set (i.e., the prediction is not an exact match).    
        - **Low Zero-One Loss**: Indicates that the classifier makes fewer predictions that do not match 
          the true labels exactly.
        - **High Zero-One Loss**: Indicates that the classifier often makes incorrect predictions.
        - **Reference**: [Zero-One Loss on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.zero_one_loss.html)

    5. **Precision (Macro)**
        Definition: The average precision score calculated for each label independently and then 
        averaged, treating all labels equally.    
        - **High Macro Precision**: Indicates good performance across all labels individually.
        - **Low Macro Precision**: Indicates poor performance on some labels.
        - **Reference**: [Precision Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)

    6. **Precision (Micro)**
        Definition: The total number of true positives divided by the total number of true positives 
        and false positives, aggregated across all labels.    
        - **High Micro Precision**: Indicates good overall performance when considering all labels collectively.
        - **Low Micro Precision**: Indicates many false positives relative to true positives.
        - **Reference**: [Precision Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)

    7. **Precision (Weighted)**
        Definition: The precision score calculated for each label, weighted by the number of true 
        instances for each label, and then averaged.
        - **High Weighted Precision**: Indicates good performance when accounting for the number of 
          instances for each label.
        - **Low Weighted Precision**: Indicates varying performance across labels.
        - **Reference**: [Precision Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)

    8. **Precision (Samples)**
        Definition: The precision score computed for each instance individually, then averaged.    
        - **High Sample Precision**: Indicates good performance on average across different instances.
        - **Low Sample Precision**: Indicates that the classifier often makes incorrect predictions for some instances.
        - **Reference**: [Precision Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)

    9. **Recall (Macro)**
        Definition: The average recall score calculated for each label independently and then 
        averaged, treating all labels equally.    
        - **High Macro Recall**: Indicates good identification of relevant labels across all labels individually.
        - **Low Macro Recall**: Indicates that the classifier misses many relevant labels.
        - **Reference**: [Recall Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)

    10. **Recall (Micro)**
        Definition: The total number of true positives divided by the total number of true positives 
        and false negatives, aggregated across all labels.    
        - **High Micro Recall**: Indicates good overall identification of relevant labels.
        - **Low Micro Recall**: Indicates that the classifier misses many relevant labels.
        - **Reference**: [Recall Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)

    11. **Recall (Weighted)**
        Definition: The recall score calculated for each label, weighted by the number of true 
        instances for each label, and then averaged.    
        - **High Weighted Recall**: Indicates good performance when considering the number of instances for each label.
        - **Low Weighted Recall**: Indicates varying performance in identifying relevant labels.
        - **Reference**: [Recall Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)

    12. **Recall (Samples)**
        Definition: The recall score computed for each instance individually, then averaged.    
        - **High Sample Recall**: Indicates good identification of relevant labels on average across instances.
        - **Low Sample Recall**: Indicates that the classifier misses many relevant labels for some instances.
        - **Reference**: [Recall Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)

    13. **F1 Score (Macro)**
        Definition: The average F1 score calculated for each label independently and then averaged, 
        treating all labels equally.    
        - **High Macro F1**: Indicates a good balance between precision and recall across all labels.
        - **Low Macro F1**: Indicates poor balance between precision and recall.
        - **Reference**: [F1 Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)

    14. **F1 Score (Micro)**
        Definition: The total number of true positives divided by the total number of true positives, 
        false positives, and false negatives, aggregated across all labels.
        - **High Micro F1**: Indicates good overall balance between precision and recall.
        - **Low Micro F1**: Indicates poor overall balance between precision and recall.
        - **Reference**: [F1 Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)

    15. **F1 Score (Weighted)**
        Definition: The F1 score calculated for each label, weighted by the number of true instances
          for each label, and then averaged.    
        - **High Weighted F1**: Indicates good performance considering the number of instances for each label.
        - **Low Weighted F1**: Indicates varying performance across labels.
        - **Reference**: [F1 Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)

    16. **F1 Score (Samples)**
        Definition: The F1 score computed for each instance individually, then averaged.
        - **High Sample F1**: Indicates good balance between precision and recall for each instance.
        - **Low Sample F1**: Indicates that the balance between precision and recall varies significantly across instances.
        - **Reference**: [F1 Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)

    17. **Jaccard Score (Macro)**
        Definition: The average Jaccard score computed for each label independently and then 
        averaged, treating all labels equally.
        - **High Macro Jaccard Score**: Indicates good performance across all labels individually.
        - **Low Macro Jaccard Score**: Indicates poor performance on some labels.
        - **Reference**: [Jaccard Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html)

    18. **Jaccard Score (Micro)**
        Definition: The total number of true positives divided by the total number of true positives,
        false positives, and false negatives, aggregated across all labels.
        - **High Micro Jaccard Score**: Indicates good overall performance in terms of similarity and diversity.
        - **Low Micro Jaccard Score**: Indicates poor performance in capturing similarities and differences across labels.
        - **Reference**: [Jaccard Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html)

    19. **Jaccard Score (Weighted)**
        Definition: The Jaccard score calculated for each label, weighted by the number of true 
        instances for each label, and then averaged.
        - **High Weighted Jaccard Score**: Indicates good performance considering the number of instances for each label.
        - **Low Weighted Jaccard Score**: Indicates varying performance across labels.
        - **Reference**: [Jaccard Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html)

    20. **Jaccard Score (Samples)**
        Definition: The Jaccard score computed for each instance individually, then averaged.
        - **High Sample Jaccard Score**: Indicates good performance on average for each instance.
        - **Low Sample Jaccard Score**: Indicates varying performance across instances.
        - **Reference**: [Jaccard Score on scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html)

    Example Usage:
    --------------
    >>> result_df = multilabel_bipartition_measures(true_labels, pred_labels)
    >>> print(result_df)
    """

    # Basic metrics
    accuracy_mlem = ms.mlem_accuracy(true_labels, pred_labels)
    hamming_l = hamming_loss(np.array(true_labels), np.array(pred_labels))    
    zol = zero_one_loss(np.array(true_labels), np.array(pred_labels))    
    sa = ms.mlem_subset_accuracy(true_labels, pred_labels)

    # Precision Scores
    precision_macro = precision_score(true_labels, pred_labels, average='macro', zero_division='warn')    
    precision_micro = precision_score(true_labels, pred_labels, average='micro', zero_division='warn')
    precision_weighted = precision_score(true_labels, pred_labels, average='weighted', zero_division='warn')
    precision_samples = precision_score(true_labels, pred_labels, average='samples', zero_division='warn')
    precision_none = precision_score(true_labels, pred_labels, average=None, zero_division='warn')
    
    # Recall Scores
    recall_macro = recall_score(true_labels, pred_labels, average='macro', zero_division='warn')  
    recall_micro = recall_score(true_labels, pred_labels, average='micro', zero_division='warn')
    recall_weighted = recall_score(true_labels, pred_labels, average='weighted', zero_division='warn')
    recall_samples = recall_score(true_labels, pred_labels, average='samples', zero_division='warn')
    recall_none = recall_score(true_labels, pred_labels, average=None, zero_division='warn')
       
    # F1 Scores
    f1_macro = f1_score(true_labels, pred_labels, average='macro', zero_division='warn')
    f1_micro = f1_score(true_labels, pred_labels, average='micro', zero_division='warn')
    f1_weighted = f1_score(true_labels, pred_labels, average='weighted', zero_division='warn')
    f1_samples = f1_score(true_labels, pred_labels, average='samples', zero_division='warn')
    f1_none = f1_score(true_labels, pred_labels, average=None, zero_division='warn')

    # Jaccard Scores
    jaccard_macro = jaccard_score(true_labels, pred_labels, average='macro', zero_division="warn")
    jaccard_micro = jaccard_score(true_labels, pred_labels, average='micro', zero_division="warn")
    jaccard_weighted = jaccard_score(true_labels, pred_labels, average='weighted', zero_division="warn")
    jaccard_samples = jaccard_score(true_labels, pred_labels, average='samples', zero_division="warn")    
    jaccard_none = jaccard_score(true_labels, pred_labels, average=None, zero_division="warn")    

    # Precision, Recall, F1, and Support Scores
    rpf_macro = precision_recall_fscore_support(true_labels, pred_labels, average='macro', zero_division="warn")
    rpf_micro = precision_recall_fscore_support(true_labels, pred_labels, average='micro', zero_division="warn")
    rpf_weighted = precision_recall_fscore_support(true_labels, pred_labels, average='weighted', zero_division="warn")
    rpf_samples = precision_recall_fscore_support(true_labels, pred_labels, average='samples', zero_division="warn")    
    rpf_none = precision_recall_fscore_support(true_labels, pred_labels, average=None, zero_division="warn")    

    # Store all metrics in a dictionary
    metrics_dict = {
        'accuracy': accuracy_mlem,        
        'f1_macro': f1_macro,
        'f1_micro': f1_micro,
        'f1_weighted': f1_weighted,
        'f1_samples': f1_samples, 
        'hamming_loss': hamming_l,              
        'jaccard_macro': jaccard_macro,
        'jaccard_micro': jaccard_micro,
        'jaccard_weighted': jaccard_weighted,
        'jaccard_samples': jaccard_samples,
        'precision_macro': precision_macro,
        'precision_micro': precision_micro,
        'precision_weighted': precision_weighted,
        'precision_samples': precision_samples,        
        'recall_macro': recall_macro,
        'recall_micro': recall_micro,
        'recall_weighted': recall_weighted,
        'recall_samples': recall_samples,  
        #'precision_recall_fscore_support_macro': rpf_macro,
        #'precision_recall_fscore_support_micro': rpf_micro,
        #'precision_recall_fscore_support_weighted': rpf_weighted,
        #'precision_recall_fscore_support_samples': rpf_samples,
        'zero_one_loss': zol     
    }

    # Convert dictionary to DataFrame
    # metrics_df = pd.DataFrame([metrics_dict])

    # Converter o dicionário em um DataFrame com colunas "Measure" e "Value"
    metrics_df = pd.DataFrame(list(metrics_dict.items()), columns=['Measure', 'Value'])

    return metrics_df




########################################################################
#                                                                      #
########################################################################
def multilabel_curves_measures(true_labels: pd.DataFrame, pred_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates various evaluation metrics related to ranking curves for multi-label classification.

    Parameters:
    ----------
    true_labels (pd.DataFrame): The DataFrame containing the true binary labels (0 or 1) for each instance.
    
    pred_scores (pd.DataFrame): The DataFrame containing the predicted probabilities for each label.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the computed curve-based metrics.

    Metrics Computed:
    ------------------
    - Average Precision (AP) Score (Macro, Micro, Weighted, Samples)
    - ROC AUC Score (Macro, Micro, Weighted, Samples)

    Interpretation:
    ----------------
    1. **Average Precision (AP) Score**
        Definition: Measures the quality of the ranking of predicted probabilities. It summarizes the 
        precision-recall curve by calculating the average precision over all instances.
        - **AP Macro**: The average precision score calculated for each label independently and then 
          averaged, treating all labels equally.
          - High AP Macro: Indicates good performance across all labels, regardless of class imbalance.
        - **AP Micro**: The average precision score calculated by aggregating the contributions of all labels 
          to compute the average precision.
          - High AP Micro: Indicates good overall performance when considering the aggregate precision.
        - **AP Weighted**: The average precision score calculated for each label, weighted by the number of 
          true instances for each label, and then averaged.
          - High AP Weighted: Indicates good performance when considering the number of instances for each label.
        - **AP Samples**: The average precision score computed for each instance individually and then averaged.
          - High AP Samples: Indicates good performance on average across different instances.

    2. **ROC AUC Score**
        Definition: Measures the area under the Receiver Operating Characteristic (ROC) curve, summarizing the 
        trade-off between true positive rate and false positive rate.
        - **ROC AUC Macro**: The ROC AUC score calculated for each label independently and then averaged, 
          treating all labels equally.
          - High ROC AUC Macro: Indicates good performance across all labels, regardless of class imbalance.
        - **ROC AUC Micro**: The ROC AUC score calculated by aggregating the contributions of all labels to 
          compute the average ROC AUC.
          - High ROC AUC Micro: Indicates good overall performance when considering the aggregate true positive 
            rate and false positive rate.
        - **ROC AUC Weighted**: The ROC AUC score calculated for each label, weighted by the number of true 
          instances for each label, and then averaged.
          - High ROC AUC Weighted: Indicates good performance when considering the number of instances for each label.
        - **ROC AUC Samples**: The ROC AUC score computed for each instance individually and then averaged.
          - High ROC AUC Samples: Indicates good performance on average across different instances.

    Example Usage:
    --------------
    >>> result_df = multilabel_curves_measures(true_labels, pred_scores)
    >>> print(result_df)
    """

    # Average Precision Scores
    average_precision_macro = average_precision_score(true_labels, pred_scores, average='macro')
    average_precision_micro = average_precision_score(true_labels, pred_scores, average='micro')
    average_precision_weighted = average_precision_score(true_labels, pred_scores, average='weighted')
    average_precision_samples = average_precision_score(true_labels, pred_scores, average='samples')    
    
    # ROC AUC Scores
    roc_auc_macro = roc_auc_score(true_labels, pred_scores, average='macro')
    roc_auc_micro = roc_auc_score(true_labels, pred_scores, average='micro')
    roc_auc_weighted = roc_auc_score(true_labels, pred_scores, average='weighted')
    roc_auc_samples = roc_auc_score(true_labels, pred_scores, average='samples')      


    # Store all metrics in a dictionary
    metrics_dict = {
        'auprc_macro': average_precision_macro,
        'auprc_micro': average_precision_micro,
        'auprc_weighted': average_precision_weighted,
        'auprc_samples': average_precision_samples,
        'roc_auc_macro': roc_auc_macro,
        'roc_auc_micro': roc_auc_micro,
        'roc_auc_weighted': roc_auc_weighted,
        'roc_auc_samples': roc_auc_samples
    }

    # Convert dictionary to DataFrame
    # metrics_df = pd.DataFrame([metrics_dict])

    # Converter o dicionário em um DataFrame com colunas "Measure" e "Value"
    metrics_df = pd.DataFrame(list(metrics_dict.items()), columns=['Measure', 'Value'])

    return metrics_df


########################################################################
#                                                                      #
########################################################################
def multilabel_ranking_measures(true_labels: pd.DataFrame, pred_scores: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates various ranking-based evaluation metrics for multi-label classification.

    Parameters:
    ----------
    true_labels (pd.DataFrame): The DataFrame containing the true binary labels for each instance.

    pred_scores (pd.DataFrame): The DataFrame containing the predicted scores for each label.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the computed ranking-based metrics.

    Metrics Computed:
    ------------------
    - Average Precision
    - Coverage Error
    - Is Error
    - Margin Loss
    - Ranking Error
    - Ranking Loss
    - One Error

    Interpretation:
    ----------------
    1. **Average Precision**
        Definition: Measures the quality of the ranking of predicted labels. It is the average of the 
        precision scores calculated at each position in the ranked list of predictions, weighted by 
        the number of relevant items found.
        - A value of 1.0 indicates perfect ranking where all relevant labels are ranked above all 
          irrelevant labels for every instance.
        - Lower values indicate that the model is not effectively ranking all relevant labels before 
          irrelevant ones.

    2. **Coverage Error**
        Definition: Measures the average number of labels that need to be checked before finding all 
        relevant labels for each instance.
        - A value of 3.5 indicates that, on average, you need to check 3.5 labels to find all relevant 
          labels.
        - Lower values are preferable as they suggest that fewer labels need to be checked to find all 
          relevant ones, indicating better model performance.

    3. **Is Error**
        Definition: Indicates whether there is any discrepancy between the predicted ranking and the true 
        ranking. 
        - A value of 1.0 suggests that there is an error in the ranking, meaning that the predicted 
          ranking does not match the true ranking exactly.
        - A value of 0.0 indicates that the predicted ranking matches the true ranking exactly.

    4. **Margin Loss**
        Definition: Measures the average number of positions by which positive labels are ranked below 
        negative labels. 
        - A Margin Loss value of 1.25 indicates that, on average, positive labels are ranked 1.25 
          positions below negative labels.
        - Lower values are preferable as they suggest that positive labels are ranked closer to the top 
          compared to negative labels.

    5. **Ranking Error**
        Definition: Calculates the sum of squared differences between the predicted and true rankings. 
        - A value of 9.5 indicates the total magnitude of the ranking errors.
        - Lower values are better, indicating that the predicted ranking is closer to the true ranking.

    6. **Ranking Loss**
        Definition: Measures the fraction of label pairs where the ranking is incorrect. 
        - A value of approximately 0.67 indicates that about 67% of label pairs are ranked incorrectly.
        - Lower values are preferred, indicating that the majority of label pairs are ranked correctly.

    7. **One Error**
        Definition: Measures the proportion of instances where the highest-ranked label is not in the set 
        of true labels.
        - A value of 0.0 indicates that for every instance, the highest-ranked label is always a true label.
        - A value of 1.0 indicates that for every instance, the highest-ranked label is never a true label.
        - Lower values are better, indicating that the model is effective at ranking at least one relevant
        label as the highest-ranked label for each instance.

    References:
    ----------
    - The metrics used are commonly referenced in multi-label ranking evaluation literature and libraries.
    - For detailed explanations, see the respective methods in the `ms` (multi-label metrics) library 
    documentation and scikit-learn documentation for `label_ranking_loss` and `coverage_error`.

    Examples:
    ----------
    >>> true_labels = pd.DataFrame([[1, 0, 0], [0, 1, 1], [1, 1, 0]], columns=['A', 'B', 'C'])
    >>> pred_scores = pd.DataFrame([[0.2, 0.5, 0.3], [0.4, 0.2, 0.6], [0.7, 0.1, 0.2]], columns=['A', 'B', 'C'])
    >>> result_df = multilabel_ranking_measures(true_labels, pred_scores)
    >>> print(result_df)
    """
    
    # Compute the various ranking metrics
    average_precision = ms.mlem_average_precision(true_labels, pred_scores)
    precision_atk = ms.mlem_precision_at_k(true_labels, pred_scores)
    coverage = coverage_error(true_labels, pred_scores)
    iserror = ms.mlem_is_error(true_labels, pred_scores)
    margin_loss = ms.mlem_margin_loss(true_labels, pred_scores)       
    ranking_error = ms.mlem_ranking_error(true_labels, pred_scores)       
    ranking_loss = label_ranking_loss(true_labels, pred_scores)       
    one_error = ms.mlem_one_error(true_labels, pred_scores)

    # Store all metrics in a dictionary
    metrics_dict = {    
        'average_precision': average_precision,
        'coverage': coverage,
        'is_error': iserror,
        'margin_loss': margin_loss,
        'precision_atk': precision_atk,
        'ranking_error': ranking_error,
        'ranking_loss': ranking_loss,    
        'one_error': one_error
    }

    # Convert dictionary to DataFrame
    metrics_df = pd.DataFrame(list(metrics_dict.items()), columns=['Measure', 'Value'])

    return metrics_df


########################################################################
#                                                                      #
########################################################################
def robust_multilabel_metric(y_true, y_scores, metric_func, average='macro', class_names=None, verbose=True):
    """
    Compute robust multilabel evaluation metrics, ignoring classes with undefined behavior.

    Objectives:
    -----------
    - To compute multilabel classification metrics (e.g., ROC AUC, AUPRC) safely.
    - Automatically detect and skip classes that do not have both positive and negative samples.
    - Return metric value along with the list of ignored class names.
    - Provide readable warning messages for skipped classes when verbose=True.

    Parameters:
    -----------
    y_true : array-like of shape (n_samples, n_classes)
        Ground truth binary indicator matrix.

    y_scores : array-like of shape (n_samples, n_classes)
        Predicted scores or probabilities.

    metric_func : callable
        Scikit-learn compatible metric function (e.g., `roc_auc_score`, `average_precision_score`).

    average : str, default='macro'
        Averaging method to compute the metric across labels.
        Options:
        - 'macro' : unweighted mean of the per-label scores
        - 'micro' : global metrics by aggregating TP, FP, FN across all labels
        - 'weighted' : mean of per-label scores, weighted by support
        - 'samples' : metrics computed per instance, then averaged

    class_names : list of str, optional
        List of class names corresponding to columns of y_true. If None, uses "Class 0", "Class 1", etc.

    verbose : bool, default=True
        If True, prints warnings for each ignored class or failed metric.

    Returns:
    --------
    score : float or np.nan
        The computed metric score. If no class is valid, returns np.nan.

    ignored_classes : list of str
        List of class names that were skipped because they lacked positive/negative examples.

    Example:
    --------
    >>> from sklearn.metrics import roc_auc_score
    >>> y_true = np.array([[1, 0, 1], [0, 1, 1], [1, 0, 0]])
    >>> y_scores = np.array([[0.9, 0.1, 0.8], [0.2, 0.7, 0.6], [0.8, 0.2, 0.3]])
    >>> class_names = ["LabelA", "LabelB", "LabelC"]
    >>> score, ignored = robust_multilabel_metric(y_true, y_scores, roc_auc_score, average='macro', class_names=class_names)
    >>> print(score)
    0.916...
    >>> print(ignored)
    []

    Notes
    -----
    Author: Mauri Ferrandin and Elaine Cecília Gatto
    """
    ignored_classes = []
    valid_scores = []

    n_classes = y_true.shape[1]

    for i in range(n_classes):
        true_col = y_true[:, i]
        pred_col = y_scores[:, i]

        if len(np.unique(true_col)) < 2:
            class_label = class_names[i] if class_names else f"Class {i}"
            ignored_classes.append(class_label)
            if verbose:
                print(f"⚠️ Class '{class_label}' ignored: only one class present in true labels.")
            continue

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                warnings.simplefilter("ignore", category=UndefinedMetricWarning)
                score_i = metric_func(true_col, pred_col)
            valid_scores.append(score_i)
        except ValueError:
            class_label = class_names[i] if class_names else f"Class {i}"
            ignored_classes.append(class_label)
            if verbose:
                print(f"⚠️ Class '{class_label}' ignored due to error when computing the metric.")

    if not valid_scores:
        if verbose:
            print(f"⚠️ Metric '{metric_func.__name__}' with '{average}' averaging failed: no valid classes.")
        return np.nan, ignored_classes

    if average == 'macro':
        return np.mean(valid_scores), ignored_classes
    elif average == 'weighted':
        supports = [np.sum(y_true[:, i]) for i in range(n_classes) if len(np.unique(y_true[:, i])) > 1]
        total_support = np.sum(supports)
        weights = [s / total_support for s in supports]
        return np.average(valid_scores, weights=weights), ignored_classes
    elif average == 'samples':
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                return metric_func(y_true, y_scores, average='samples'), ignored_classes
        except ValueError:
            return np.nan, ignored_classes
    elif average == 'micro':
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)
                return metric_func(y_true, y_scores, average='micro'), ignored_classes
        except ValueError:
            return np.nan, ignored_classes




########################################################################
#                                                                      #
########################################################################
def multilabel_curve_metrics(true_labels: pd.DataFrame, predicted_scores: pd.DataFrame):
    """
    Compute multilabel curve-based evaluation metrics (AUPRC and ROC AUC) with support 
    for multiple averaging strategies and robust handling of undefined metric cases.

    Objectives
    ----------
    - Compute AUPRC and ROC AUC using ['macro', 'micro', 'weighted', 'samples'] averaging.
    - Gracefully skip labels that lack positive or negative samples, avoiding metric errors.
    - Return the list of ignored class names per metric and print informative warnings.

    Parameters
    ----------
    true_labels : pd.DataFrame
        Binary matrix (shape: n_samples x n_classes) of ground truth labels.
        Column names are treated as class names.

    predicted_scores : pd.DataFrame
        Matrix of predicted scores or probabilities (same shape and column order as true_labels).

    Returns
    -------
    metrics_df : pd.DataFrame
        DataFrame containing:
        - 'Measure': Metric name (e.g., 'auprc_macro')
        - 'Value'  : Metric value (float or np.nan if undefined)

    ignored_df : pd.DataFrame
        DataFrame containing:
        - 'Measure'         : Name of the metric (same as in metrics_df)
        - 'Ignored_Classes' : List of class names skipped due to insufficient variability

    Example
    -------
    >>> metrics_df, ignored_df = multilabel_curve_metrics(y_test, y_proba)
    >>> print(metrics_df)
            Measure     Value
        0  auprc_macro    0.88
        1  auprc_micro    0.91
        ...
    >>> print(ignored_df)
            Measure       Ignored_Classes
        0  roc_auc_macro   ['Label1']
        1  roc_auc_weighted ['Label1']

    Notes
    -----
    Author: Mauri Ferrandin and Elaine Cecília Gatto
    """
    metrics_data = []
    ignored_data = []

    class_names = true_labels.columns.tolist()

    for metric_func, metric_name in [
        (average_precision_score, 'auprc'),
        (roc_auc_score, 'roc_auc')
    ]:
        for avg in ['macro', 'micro', 'weighted', 'samples']:
            score, ignored = robust_multilabel_metric(
                y_true=true_labels.values,
                y_scores=predicted_scores.values,
                metric_func=metric_func,
                average=avg,
                class_names=class_names,
                verbose=True
            )

            metrics_data.append({
                'Measure': f'{metric_name}_{avg}',
                'Value': score
            })

            ignored_data.append({
                'Measure': f'{metric_name}_{avg}',
                'Ignored_Classes': ignored if ignored else []
            })

    metrics_df = pd.DataFrame(metrics_data)
    ignored_df = pd.DataFrame(ignored_data)

    return metrics_df, ignored_df


def verificar_sinal_colunas(df):
    resultado = {}
    for col in df.columns:
        unicos = df[col].unique()
        if all(unicos > 0):
            resultado[col] = 'positive'
        elif all(unicos < 0):
            resultado[col] = 'negative'
        elif all(unicos == 0):
            resultado[col] = 'zero'
        else:
            resultado[col] = 'both'
    return pd.Series(resultado, name="Tipo de valores")



def safe_predict_proba(chain, X_test, Y_train):
    """
    Safely computes class probabilities for each label in a Classifier Chain, handling single-class cases.

    This function replicates the internal behavior of `ClassifierChain.predict_proba` but includes a fix for
    cases where certain labels in the training set have only one class (e.g., all 0s or all 1s).
    Scikit-learn's default behavior raises an IndexError in such cases when trying to access probabilities
    for non-existent classes. This function avoids that by assuming a constant probability of 0 or 1 
    depending on the single class seen during training.

    Parameters
    ----------
    chain : sklearn.multioutput.ClassifierChain
        A fitted ClassifierChain model using any binary classifier as base estimator (e.g., RandomForestClassifier).
    
    X_test : pandas.DataFrame
        The input feature set for which the probability predictions will be made. Should have the same
        structure and columns as used during training.
    
    Y_train : pandas.DataFrame
        The original multi-label target used during training. Needed to determine the number and order
        of output labels and to handle label names properly.

    Returns
    -------
    prob_df : pandas.DataFrame
        A DataFrame of shape (n_samples, n_labels), containing the predicted probabilities
        for the positive class (label = 1) for each label.

    Example
    -------
    >>> from sklearn.multioutput import ClassifierChain
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> chain = ClassifierChain(RandomForestClassifier())
    >>> chain.fit(X_train, Y_train)
    >>> prob_df = safe_predict_proba(chain, X_test, Y_train)
    >>> prob_df.to_csv("y_pred_proba.csv", index=False)

    Notes
    -----
    Author: Ricardo Cerri and Elaine Cecília Gatto
    Created: 2025    
    """    

    n_samples = X_test.shape[0]
    n_labels = Y_train.shape[1]
    probas = np.zeros((n_samples, n_labels))

    X_aug = X_test.values  # start with raw test features

    for idx, estimator in enumerate(chain.estimators_):
        if idx > 0:
            # Add predicted probabilities of previous labels as features
            X_aug = np.hstack((X_test.values, probas[:, :idx]))

        proba = estimator.predict_proba(X_aug)

        if proba.shape[1] == 2:
            # Standard binary case: use probability of class 1
            probas[:, idx] = proba[:, 1]
        else:
            # Single-class case: force consistent output
            label_class = estimator.classes_[0]
            probas[:, idx] = 1.0 if label_class == 1 else 0.0

    return pd.DataFrame(probas, columns=Y_train.columns)


"""
Cerri:
probas = np.zeros((X_test.shape[0], y_train.shape[1]))

for idx, estimator in enumerate(chain.estimators_):
    X_aug = ...  # como o chain constrói internamente
    proba = estimator.predict_proba(X_aug)
    if proba.shape[1] == 2:
        probas[:, idx] = proba[:, 1]
    else:
        # classe única: assume que é sempre a classe presente
        probas[:, idx] = proba[:, 0]  # ou 1.0 se for classe positiva
"""
