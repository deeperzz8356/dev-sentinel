#!/usr/bin/env python3
"""
Quick ML Model Training Script
Trains a model with minimal setup for immediate use
"""

import pandas as pd
import numpy as np
import joblib
import json
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score

def generate_training_data():
    """Generate synthetic training data for quick training"""
    print("🤖 Generating synthetic training data...")
    
    np.random.seed(42)
    n_samples = 500
    
    data = []
    
    # Generate authentic profiles (60% of data)
    for i in range(int(n_samples * 0.6)):
        data.append({
            'commit_frequency': np.random.normal(20, 8),  # Regular commits
            'weekend_commit_ratio': np.random.uniform(0.1, 0.3),  # Low weekend
            'night_commit_ratio': np.random.uniform(0.05, 0.2),  # Low night
            'original_repo_ratio': np.random.uniform(0.6, 0.9),  # High original
            'commit_size_variance': np.random.uniform(0.3, 0.8),  # Varied sizes
            'activity_consistency': np.random.uniform(0.7, 0.95),  # Consistent
            'follower_repo_ratio': np.random.uniform(0.5, 3.0),  # Reasonable
            'language_diversity': np.random.randint(3, 8),  # Multiple languages
            'label': 1  # Authentic
        })
    
    # Generate suspicious profiles (40% of data)
    for i in range(int(n_samples * 0.4)):
        data.append({
            'commit_frequency': np.random.choice([
                np.random.normal(2, 1),    # Too few
                np.random.normal(80, 15)   # Too many
            ]),
            'weekend_commit_ratio': np.random.uniform(0.5, 0.8),  # High weekend
            'night_commit_ratio': np.random.uniform(0.4, 0.7),   # High night
            'original_repo_ratio': np.random.uniform(0.1, 0.4),  # Low original
            'commit_size_variance': np.random.uniform(0.05, 0.2), # Uniform sizes
            'activity_consistency': np.random.uniform(0.2, 0.5),  # Inconsistent
            'follower_repo_ratio': np.random.choice([
                np.random.uniform(0.01, 0.1),  # Too few followers
                np.random.uniform(10, 50)      # Too many followers
            ]),
            'language_diversity': np.random.randint(1, 3),  # Limited languages
            'label': 0  # Suspicious
        })
    
    # Clean data
    for record in data:
        record['commit_frequency'] = max(0, record['commit_frequency'])
        record['weekend_commit_ratio'] = np.clip(record['weekend_commit_ratio'], 0, 1)
        record['night_commit_ratio'] = np.clip(record['night_commit_ratio'], 0, 1)
        record['original_repo_ratio'] = np.clip(record['original_repo_ratio'], 0, 1)
        record['commit_size_variance'] = np.clip(record['commit_size_variance'], 0, 1)
        record['activity_consistency'] = np.clip(record['activity_consistency'], 0, 1)
        record['follower_repo_ratio'] = max(0, record['follower_repo_ratio'])
        record['language_diversity'] = max(1, record['language_diversity'])
    
    df = pd.DataFrame(data)
    print(f"✅ Generated {len(df)} training samples")
    print(f"📊 Authentic: {sum(df['label'])}, Suspicious: {len(df) - sum(df['label'])}")
    
    return df

def train_quick_model():
    """Train a quick ML model"""
    print("🧠 Training ML model...")
    
    # Generate training data
    df = generate_training_data()
    
    # Prepare features
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
    
    X = df[feature_cols]
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    print(f"✅ Model trained successfully!")
    print(f"📊 Test AUC Score: {auc_score:.3f}")
    print("\n📈 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Suspicious', 'Authentic']))
    
    # Save model
    os.makedirs("models", exist_ok=True)
    
    joblib.dump(model, "models/authenticity_model.joblib")
    joblib.dump(scaler, "models/scaler.joblib")
    
    # Save metadata
    metadata = {
        'model_type': 'Random Forest',
        'feature_names': feature_cols,
        'trained_at': datetime.now().isoformat(),
        'test_auc': float(auc_score),
        'training_samples': len(df),
        'training_method': 'synthetic_data'
    }
    
    with open("models/model_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("💾 Model saved to models/")
    return auc_score

def update_main_py():
    """Update main.py to use trained model"""
    print("🔄 Updating main.py to use trained model...")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        if 'simple_analyzer' in content:
            updated_content = content.replace(
                'from services.simple_analyzer import SimpleAnalyzer',
                'from services.trained_ml_analyzer import TrainedMLAnalyzer'
            ).replace(
                'analyzer = SimpleAnalyzer()',
                'analyzer = TrainedMLAnalyzer()'
            )
            
            with open('main.py', 'w') as f:
                f.write(updated_content)
            
            print("✅ Updated main.py to use trained ML model")
        else:
            print("⚠️  main.py already updated or has different structure")
            
    except Exception as e:
        print(f"⚠️  Could not update main.py: {e}")

def main():
    """Main quick training function"""
    print("⚡ Quick ML Model Training for Dev-Sentinel")
    print("=" * 50)
    
    # Train model
    auc_score = train_quick_model()
    
    # Update main.py
    update_main_py()
    
    print("\n🎉 Quick training completed!")
    print(f"🏆 Model AUC Score: {auc_score:.3f}")
    
    if auc_score > 0.8:
        print("✅ Excellent model performance!")
    elif auc_score > 0.7:
        print("✅ Good model performance!")
    else:
        print("⚠️  Model performance could be improved with more data")
    
    print("\n🚀 Next steps:")
    print("1. Restart your backend server: python main.py")
    print("2. The API will now use the trained ML model")
    print("3. Test with real GitHub usernames in the frontend")
    
    print("\n💡 For better performance:")
    print("- Collect real GitHub data: python data_collection/collect_training_data.py")
    print("- Train with real data: python ml_training/train_model.py")

if __name__ == "__main__":
    main()