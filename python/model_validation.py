import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve

def gini_from_auc(auc: float) -> float:
    return 2 * auc - 1

def ks_stat(y_true, score):
    fpr, tpr, _ = roc_curve(y_true, score)
    return float(np.max(tpr - fpr))

def psi(expected, actual, buckets=10):
    expected = np.asarray(expected)
    actual = np.asarray(actual)
    quantiles = np.percentile(expected, np.linspace(0,100,buckets+1))
    quantiles[0] -= 1e-9
    quantiles[-1] += 1e-9
    e_counts,_=np.histogram(expected,bins=quantiles)
    a_counts,_=np.histogram(actual,bins=quantiles)
    e_pct=np.maximum(e_counts/e_counts.sum(),1e-6)
    a_pct=np.maximum(a_counts/a_counts.sum(),1e-6)
    return float(np.sum((a_pct-e_pct)*np.log(a_pct/e_pct)))
