#!/usr/bin/env python3
"""
Complete ML Model Training Workflow
This script handles the entire process from data collection to model training
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print("Error:", e.stderr)
        return False

def main():
    """Main training workflow"""
    print("🚀 Dev-Sentinel ML Model Training Workflow")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if GitHub token is available
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        print(f"✅ GitHub token found (length: {len(github_token)})")
    else:
        print("⚠️  No GitHub token found. Data collection will be rate-limited.")
        print("To add a token, edit .env file and add: GITHUB_TOKEN=your_token_here")
    
    # Step 1: Install ML dependencies
    print("\n📦 Step 1: Installing ML dependencies...")
    if not run_command("pip install scikit-learn pandas matplotlib seaborn", 
                      "Installing ML dependencies"):
        print("❌ Failed to install dependencies. Please install manually:")
        print("pip install scikit-learn pandas matplotlib seaborn")
        return
    
    # Step 2: Collect training data
    print("\n📊 Step 2: Collecting training data...")
    if not run_command("python data_collection/collect_training_data.py", 
                      "Collecting training data"):
        print("❌ Data collection failed. Please check the error above.")
        return
    
    # Step 3: Train ML model
    print("\n🧠 Step 3: Training ML model...")
    if not run_command("python ml_training/train_model.py", 
                      "Training ML model"):
        print("❌ Model training failed. Please check the error above.")
        return
    
    # Step 4: Update main.py to use trained model
    print("\n🔄 Step 4: Updating API to use trained model...")
    
    # Read current main.py
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Replace simple analyzer with trained analyzer
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
            print("⚠️  main.py already using trained model or different structure")
            
    except Exception as e:
        print(f"⚠️  Could not update main.py automatically: {e}")
        print("Please manually update main.py to use TrainedMLAnalyzer")
    
    # Success message
    print("\n🎉 ML Model Training Completed Successfully!")
    print("\n📊 What was accomplished:")
    print("✅ Collected training data from real GitHub profiles")
    print("✅ Trained multiple ML models (Random Forest, Gradient Boosting, etc.)")
    print("✅ Selected best performing model")
    print("✅ Saved trained model and scaler")
    print("✅ Generated model evaluation visualizations")
    
    print("\n📁 Generated files:")
    print("📊 data_collection/data/training_data.csv - Training dataset")
    print("🧠 models/authenticity_model.joblib - Trained ML model")
    print("⚖️  models/scaler.joblib - Feature scaler")
    print("📋 models/model_metadata.json - Model information")
    print("📈 ml_training/visualizations/ - Model evaluation plots")
    
    print("\n🚀 Next steps:")
    print("1. Restart your backend server to load the new ML model")
    print("2. Test the API with real GitHub usernames")
    print("3. Check the visualizations to understand model performance")
    print("4. The frontend will now use real ML predictions!")
    
    print("\n💡 To restart the backend:")
    print("python main.py")

if __name__ == "__main__":
    main()