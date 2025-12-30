#!/usr/bin/env python3
"""
Train ML Model with Real Excel Data
Uses the provided DevDebt_2000_Profiles_With_Usernames.xlsx dataset
"""

import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import seaborn as sns

class ExcelDataTrainer:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = None
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        
    def load_excel_data(self):
        """Load and explore the Excel dataset"""
        print("📊 Loading Excel dataset...")
        
        try:
            # Try different sheet names
            try:
                self.df = pd.read_excel(self.excel_path, sheet_name=0)
            except:
                self.df = pd.read_excel(self.excel_path)
            
            print(f"✅ Loaded {len(self.df)} profiles from Excel")
            print(f"📋 Columns: {list(self.df.columns)}")
            print(f"📊 Dataset shape: {self.df.shape}")
            
            # Display first few rows
            print("\n🔍 First 5 rows:")
            print(self.df.head())
            
            # Check for missing values
            print("\n❓ Missing values:")
            missing = self.df.isnull().sum()
            print(missing[missing > 0])
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return False
    
    def explore_data(self):
        """Explore the dataset structure"""
        print("\n🔍 Exploring dataset...")
        
        # Basic statistics
        print("\n📈 Dataset Info:")
        print(self.df.info())
        
        print("\n📊 Numerical columns statistics:")
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            print(self.df[numerical_cols].describe())
        
        # Check for potential label column
        potential_labels = ['label', 'authentic', 'suspicious', 'is_authentic', 'class', 'target']
        label_col = None
        
        for col in self.df.columns:
            col_lower = col.lower()
            if any(label in col_lower for label in potential_labels):
                label_col = col
                break
        
        if label_col:
            print(f"\n🎯 Found potential label column: '{label_col}'")
            print(f"Label distribution:")
            print(self.df[label_col].value_counts())
        else:
            print("\n⚠️  No obvious label column found. Available columns:")
            for i, col in enumerate(self.df.columns):
                print(f"  {i}: {col}")
        
        return label_col
    
    def prepare_features(self, label_col=None):
        """Prepare features for ML training"""
        print("\n⚙️  Preparing features...")
        
        # If no label column specified, ask user or make assumption
        if label_col is None:
            # Look for common patterns
            for col in self.df.columns:
                if 'authentic' in col.lower() or 'label' in col.lower():
                    label_col = col
                    break
        
        if label_col is None:
            print("❌ No label column found. Please specify which column contains the labels.")
            print("Available columns:")
            for i, col in enumerate(self.df.columns):
                print(f"  {i}: {col}")
            return None, None
        
        print(f"🎯 Using '{label_col}' as label column")
        
        # Separate features and labels
        feature_cols = [col for col in self.df.columns if col != label_col and col.lower() != 'username']
        
        # Handle different data types
        X = self.df[feature_cols].copy()
        y = self.df[label_col].copy()
        
        # Encode categorical variables
        for col in X.columns:
            if X[col].dtype == 'object':
                print(f"🔤 Encoding categorical column: {col}")
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
        
        # Handle missing values
        X = X.fillna(X.mean())
        
        # Encode labels if they're not numeric
        if y.dtype == 'object':
            print(f"🔤 Encoding labels...")
            le_y = LabelEncoder()
            y = le_y.fit_transform(y)
            self.label_encoders['target'] = le_y
            print(f"Label mapping: {dict(zip(le_y.classes_, le_y.transform(le_y.classes_)))}")
        
        self.feature_names = list(X.columns)
        print(f"✅ Prepared {len(self.feature_names)} features: {self.feature_names}")
        print(f"📊 Label distribution: {dict(zip(*np.unique(y, return_counts=True)))}")
        
        return X, y
    
    def train_models(self, X, y):
        """Train multiple ML models"""
        print("\n🧠 Training ML models...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models
        models_to_train = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                random_state=42,
                class_weight='balanced',
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=8,
                learning_rate=0.1,
                random_state=42
            ),
            'Logistic Regression': LogisticRegression(
                random_state=42,
                class_weight='balanced',
                max_iter=1000
            )
        }
        
        results = {}
        
        for name, model in models_to_train.items():
            print(f"🔄 Training {name}...")
            
            # Use scaled data for Logistic Regression
            if name == 'Logistic Regression':
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
    
    def hyperparameter_tuning(self, X, y):
        """Perform hyperparameter tuning on the best model"""
        print(f"\n⚙️  Tuning hyperparameters for {self.best_model_name}...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        if self.best_model_name == 'Random Forest':
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 15, 20],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            }
            
            grid_search = GridSearchCV(
                RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1),
                param_grid,
                cv=3,  # Reduced for speed
                scoring='roc_auc',
                n_jobs=-1,
                verbose=1
            )
            
        elif self.best_model_name == 'Gradient Boosting':
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [6, 8, 10],
                'learning_rate': [0.05, 0.1, 0.15]
            }
            
            grid_search = GridSearchCV(
                GradientBoostingClassifier(random_state=42),
                param_grid,
                cv=3,
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
        """Evaluate the best model"""
        print(f"\n📊 Evaluating {self.best_model_name}...")
        
        # Get predictions
        if self.best_model_name == 'Logistic Regression':
            X_test_model = self.scaler.transform(self.X_test)
        else:
            X_test_model = self.X_test
            
        y_pred = self.best_model.predict(X_test_model)
        y_pred_proba = self.best_model.predict_proba(X_test_model)[:, 1]
        
        # Classification report
        print("\n📈 Classification Report:")
        print(classification_report(self.y_test, y_pred))
        
        # Create visualizations directory
        os.makedirs("visualizations", exist_ok=True)
        
        # Confusion matrix
        cm = confusion_matrix(self.y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('visualizations/confusion_matrix_excel.png', dpi=300, bbox_inches='tight')
        print("📊 Saved confusion matrix to visualizations/confusion_matrix_excel.png")
        
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
        plt.savefig('visualizations/roc_curve_excel.png', dpi=300, bbox_inches='tight')
        print("📊 Saved ROC curve to visualizations/roc_curve_excel.png")
        
        # Feature importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(12, 8))
            plt.title("Feature Importances")
            plt.bar(range(len(importances)), importances[indices])
            plt.xticks(range(len(importances)), [self.feature_names[i] for i in indices], rotation=45)
            plt.tight_layout()
            plt.savefig('visualizations/feature_importance_excel.png', dpi=300, bbox_inches='tight')
            print("📊 Saved feature importance to visualizations/feature_importance_excel.png")
            
            # Print top features
            print(f"\n🔝 Top 10 Most Important Features:")
            for i in range(min(10, len(importances))):
                idx = indices[i]
                print(f"  {i+1}. {self.feature_names[idx]}: {importances[idx]:.4f}")
    
    def save_model(self):
        """Save the trained model"""
        print("\n💾 Saving trained model...")
        
        os.makedirs("models", exist_ok=True)
        
        # Save model
        model_path = "models/authenticity_model.joblib"
        joblib.dump(self.best_model, model_path)
        
        # Save scaler
        scaler_path = "models/scaler.joblib"
        joblib.dump(self.scaler, scaler_path)
        
        # Save label encoders
        encoders_path = "models/label_encoders.joblib"
        joblib.dump(self.label_encoders, encoders_path)
        
        # Save metadata
        metadata = {
            'model_type': self.best_model_name,
            'feature_names': self.feature_names,
            'trained_at': datetime.now().isoformat(),
            'test_auc': self.models[self.best_model_name]['test_auc'],
            'training_samples': len(self.df),
            'data_source': 'DevDebt_2000_Profiles_With_Usernames.xlsx',
            'label_encoders': list(self.label_encoders.keys())
        }
        
        metadata_path = "models/model_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Model saved to {model_path}")
        print(f"✅ Scaler saved to {scaler_path}")
        print(f"✅ Label encoders saved to {encoders_path}")
        print(f"✅ Metadata saved to {metadata_path}")

def main():
    """Main training function"""
    print("🚀 Training ML Model with Excel Data")
    print("=" * 50)
    
    excel_path = "data_collection/DevDebt_2000_Profiles_With_Usernames.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"❌ Excel file not found: {excel_path}")
        print("Please make sure the file is in the correct location.")
        return
    
    # Initialize trainer
    trainer = ExcelDataTrainer(excel_path)
    
    # Load data
    if not trainer.load_excel_data():
        return
    
    # Explore data
    label_col = trainer.explore_data()
    
    # Prepare features
    X, y = trainer.prepare_features(label_col)
    if X is None:
        return
    
    # Train models
    results = trainer.train_models(X, y)
    
    # Hyperparameter tuning
    trainer.hyperparameter_tuning(X, y)
    
    # Evaluate model
    trainer.evaluate_model()
    
    # Save model
    trainer.save_model()
    
    print("\n🎉 Excel data model training completed!")
    print(f"🏆 Best Model: {trainer.best_model_name}")
    print(f"📊 Test AUC: {trainer.models[trainer.best_model_name]['test_auc']:.3f}")
    
    print("\n💡 Next steps:")
    print("1. Restart your backend server to load the new model")
    print("2. The API will now use the Excel-trained model")
    print("3. Check visualizations folder for model performance plots")

if __name__ == "__main__":
    main()