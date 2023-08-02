import matplotlib.pyplot as plt
import shap
from sklearn.inspection import permutation_importance

# Assuming you have your data (X_train, y_train) and a trained model (model)



def plot_parameters_impact_on_model(
        model, 
        X,
        y
        ):
    
    results = permutation_importance(
        model, X, y, scoring = 'accuracy')
    feature_importance = results.importances_mean
    feature_importance
    
    explainer = shap.Explainer(model, X)
    shap_values = explainer.shap_values(X)
    
    shap_values
    
    
    sorted_indices = feature_importance.argsort()[::-1]
    sorted_importance = feature_importance[sorted_indices]
    sorted_feature_names = [cols[i] for i in sorted_indices]
    
    # Plot the feature importances
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(sorted_importance)), sorted_importance)
    plt.xticks(range(len(sorted_importance)), sorted_feature_names, rotation=45, ha='right')
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.show()
    
    import numpy as np
    
    shap.summary_plot(shap_values, X, plot_type='bar', show=False)
    
    # If you want to include the feature importance values as well:
    importance_values = np.abs(shap_values).mean(0)
    plt.barh(range(len(importance_values)), importance_values, color='#1f77b4', alpha=0.5, align='center', height=0.8)
    
    plt.xlabel('SHAP Value (magnitude of effect)')
    plt.title('Shapley Summary Plot')
    plt.tight_layout()
    plt.show()
    
    
    shap.summary_plot(shap_values, X)
