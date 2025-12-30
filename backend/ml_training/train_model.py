#!/usr/bin/env python3
"""
ML Model Training Script for GitHub Profile Authenticity
Trains multiple models and selects the best one
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from datetime import datetime
import os

class GitHubAuthenticityTrainer:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def load_data(self) -> tuple:
        """Load and prepare training data"""
        print("📊 Loading training data...")
        
        df = pd.read_csv(self.data_path)
        
        # Feature columns (exclude metadata)
        feature_cols = [
            'commit_frequency',
            'weekend_commit_ratio', 
            'night_commit_ratio',
            'original_repo_ratio',
            'commit_size_variance',
            'activity_consistency',
            'follower_repo_ratio',
            'language_diversity'
        ]
        
        self.feature_names = feature_cols
        
        X = df[feature_cols]
        y = df['label']
        
        print(f"✅ Loaded {len(df)} samples with {len(feature_cols)} features")
        print(f"📈 Class distribution: {dict(y.value_counts())}")
        
        return X, y
    
    def explore_data(self, X: pd.DataFrame, y: pd.Series):
        """Explore and visualize the training data"""
        print("\n🔍 Exploring training data...")
        
        # Create visualizations directory
        os.makedirs("visualizations", exist_ok=True)
        
        # Feature distributions by class
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        axes = axes.ravel()
        
        for i, feature in enumerate(self.feature_names):
            authentic = X[y == 1][feature]
            suspicious = X[y == 0][feature]
            
            axes[i].hist(authentic, alpha=0.7, label='Authentic', bins=20, color='green')
            axes[i].hist(suspicious, alpha=0.7, label='Suspicious', bins=20, color='red')
            axes[i].set_title(f'{feature}')
            axes[i].legend()
        
        plt.tight_layout()
        plt.savefig('visualizations/feature_distributions.png', dpi=300, bbox_inches='tight')
        print("📊 Saved feature distributions to visualizations/feature_distributions.png")
        
        # Correlation matrix
        plt.figure(figsize=(10, 8))
        correlation_matrix = X.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        plt.savefig('visualizations/correlation_matrix.png', dpi=300, bbox_inches='tight')
        print("📊 Saved correlation matrix to visualizations/correlation_matrix.png")
        
    def train_models(self, X: pd.DataFrame, y: pd.Series):
        """Train multiple ML models"""
        print("\n🧠 Training ML models...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models to train
        models_to_train = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=6,
                random_state=42
            ),
            'Logistic Regression': LogisticRegression(
                random_state=42,
                class_weight='balanced',
                max_iter=1000
            ),
            'SVM': SVC(
                kernel='rbf',
                probability=True,
                random_state=42,
                class_weight='balanced'
            )
        }
        
        # Train and evaluate each model
        results = {}
        
        for name, model in models_to_train.items():
            print(f"🔄 Training {name}...")
            
            # Use scaled data for SVM and Logistic Regression
            if name in ['SVM', 'Logistic Regression']:
                X_train_model = X_train_scaled
                X_test_model = X_test_scaled
            else:
                X_train_model = X_train
                X_test_model = X_test
            
            # Train model
            model.fit(X_train_model, y_train)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_model, y_train, cv=5, scoring='roc_auc')
            
            # Test predictions
            y_pred = model.predict(X_test_model)
            y_pred_proba = model.predict_proba(X_test_model)[:, 1]
            
            # Calculate metrics
            auc_score = roc_auc_score(y_test, y_pred_proba)
            
            results[name] = {
                'model': model,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'test_auc': auc_score,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
            
            print(f"✅ {name}: CV AUC = {cv_scores.mean():.3f} (±{cv_scores.std():.3f}), Test AUC = {auc_score:.3f}")
        
        self.models = results
        self.X_test = X_test
        self.y_test = y_test
        
        # Select best model
        best_model_name = max(results.keys(), key=lambda k: results[k]['test_auc'])
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\n🏆 Best model: {best_model_name} (AUC = {results[best_model_name]['test_auc']:.3f})")
        
        return results
    
    def hyperparameter_tuning(self, X: pd.DataFrame, y: pd.Series):
        """Perform hyperparameter tuning on the best model"""
        print(f"\n⚙️  Tuning hyperparameters for {self.best_model_name}...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        if self.best_model_name == 'Random Forest':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
            
            grid_search = GridSearchCV(
                RandomForestClassifier(random_state=42, class_weight='balanced'),
                param_grid,
                cv=5,
                scoring='roc_auc',
                n_jobs=-1,
                verbose=1
            )
            
        elif self.best_model_name == 'Gradient Boosting':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0]
            }
            
            grid_search = GridSearchCV(
                GradientBoostingClassifier(random_state=42),
                param_grid,
                cv=5,
                scoring='roc_auc',
                n_jobs=-1,
                verbose=1
            )
        
        else:
            print("⚠️  Hyperparameter tuning not implemented for this model type")
            return
        
        # Fit grid search
        grid_search.fit(X_train, y_train)
        
        # Update best model
        self.best_model = grid_search.best_estimator_
        
        print(f"✅ Best parameters: {grid_search.best_params_}")
        print(f"✅ Best CV score: {grid_search.best_score_:.3f}")
    
    def evaluate_model(self):
        """Evaluate the best model with detailed metrics"""
        print(f"\n📊 Evaluating {self.best_model_name}...")
        
        # Get predictions
        if self.best_model_name in ['SVM', 'Logistic Regression']:
            X_test_model = self.scaler.transform(self.X_test)
        else:
            X_test_model = self.X_test
            
        y_pred = self.best_model.predict(X_test_model)
        y_pred_proba = self.best_model.predict_proba(X_test_model)[:, 1]
        
        # Classification report
        print("\n📈 Classification Report:")
        print(classification_report(self.y_test, y_pred, target_names=['Suspicious', 'Authentic']))
        
        # Confusion matrix
        cm = confusion_matrix(self.y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Suspicious', 'Authentic'],
                   yticklabels=['Suspicious', 'Authentic'])
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('visualizations/confusion_matrix.png', dpi=300, bbox_inches='tight')
        print("📊 Saved confusion matrix to visualizations/confusion_matrix.png")
        
        # ROC curve
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        auc_score = roc_auc_score(self.y_test, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc_score:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('visualizations/roc_curve.png', dpi=300, bbox_inches='tight')
        print("📊 Saved ROC curve to visualizations/roc_curve.png")
        
        # Feature importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 6))
            plt.title("Feature Importances")
            plt.bar(range(len(importances)), importances[indices])
            plt.xticks(range(len(importances)), [self.feature_names[i] for i in indices], rotation=45)
            plt.tight_layout()
            plt.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
            print("📊 Saved feature importance to visualizations/feature_importance.png")
    
    def save_model(self):
        """Save the trained model and scaler"""
        print("\n💾 Saving trained model...")
        
        os.makedirs("../models", exist_ok=True)
        
        # Save model
        model_path = "../models/authenticity_model.joblib"
        joblib.dump(self.best_model, model_path)
        
        # Save scaler
        scaler_path = "../models/scaler.joblib"
        joblib.dump(self.scaler, scaler_path)
        
        # Save metadata
        metadata = {
            'model_type': self.best_model_name,
            'feature_names': self.feature_names,
            'trained_at': datetime.now().isoformat(),
            'test_auc': self.models[self.best_model_name]['test_auc']
        }
        
        metadata_path = "../models/model_metadata.json"
        import json
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Model saved to {model_path}")
        print(f"✅ Scaler saved to {scaler_path}")
        print(f"✅ Metadata saved to {metadata_path}")

def main():
    """Main training function"""
    print("🚀 Starting ML Model Training for GitHub Authenticity Analysis")
    print("=" * 70)
    
    # Check if training data exists
    data_path = "../data_collection/data/training_data.csv"
    if not os.path.exists(data_path):
        print(f"❌ Training data not found at {data_path}")
        print("Please run the data collection script first:")
        print("python data_collection/collect_training_data.py")
        return
    
    # Initialize trainer
    trainer = GitHubAuthenticityTrainer(data_path)
    
    # Load data
    X, y = trainer.load_data()
    
    # Explore data
    trainer.explore_data(X, y)
    
    # Train models
    results = trainer.train_models(X, y)
    
    # Hyperparameter tuning
    trainer.hyperparameter_tuning(X, y)
    
    # Evaluate best model
    trainer.evaluate_model()
    
    # Save model
    trainer.save_model()
    
    print("\n🎉 Model training completed successfully!")
    print("\n📊 Training Summary:")
    for name, result in results.items():
        print(f"  {name}: AUC = {result['test_auc']:.3f}")
    
    print(f"\n🏆 Best Model: {trainer.best_model_name}")
    print("\n💡 Next steps:")
    print("1. Review the visualizations in the 'visualizations' folder")
    print("2. The trained model is ready to use in your API")
    print("3. Restart your backend server to load the new model")

if __name__ == "__main__":
    main()