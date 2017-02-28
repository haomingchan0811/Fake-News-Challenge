import np
def calc_score(conf_mtx):

    #  Input: 4x4 confusion matrix (conf_mtx) where columns are predictions & rows are targets,
    #         in the form returned by sklearn.metrics.confusion_matrix. The order of labels in
    #          the confusion matrix is agree, disagree, discuss, unrelated.
    #
    #  Output: A score from 0.0 to 100.0 calculated using the Fake News Challenge FNC-1 
    #          scoring functions (see FakeNewsChallenge.org).
    # 
    # For a more detailed explanation and a Google spreadsheet version of this calculator
    # see: https://goo.gl/JAVL7h

    scoring_mask = [
        [1.00, 0.25, 0.25, 0.00],
        [0.25, 1.00, 0.25, 0.00],
        [0.25, 0.25, 1.00, 0.00],
        [0.00, 0.00, 0.00, 0.25]    
    ]

    max_category_scores = np.sum(conf_mtx, axis=1)
    
    # Discount "unrelated" right answers to only be worth 0.25 per the FNC-1 scoring function
    max_category_scores[3] = max_category_scores[3] * 0.25
   
    max_score = sum(max_category_scores)

    prediction_scores = conf_mtx * scoring_mask

    total_score = sum(sum(prediction_scores))
    return total_score/max_score * 100