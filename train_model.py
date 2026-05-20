import pandas as pd
import joblib

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV
)

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)

# =====================================================
# LOAD DATA
# =====================================================

print("\n📂 Loading dataset...")

df = pd.read_csv(
    "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

print("✅ Dataset loaded successfully")

# =====================================================
# CLEAN DATA
# =====================================================

print("\n🧹 Cleaning data...")

# Remove unnecessary column
df.drop("customerID", axis=1, inplace=True)

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Remove missing values
df.dropna(inplace=True)

# Encode target column
df["Churn"] = df["Churn"].map({
    "Yes": 1,
    "No": 0
})

print("✅ Data cleaned")

# =====================================================
# ENCODING
# =====================================================

print("\n🔄 Performing one-hot encoding...")

df = pd.get_dummies(
    df,
    drop_first=True
)

print("✅ Encoding completed")

# =====================================================
# FEATURES & TARGET
# =====================================================

X = df.drop("Churn", axis=1)

y = df["Churn"]

# =====================================================
# SAVE FEATURE COLUMNS
# IMPORTANT FOR CHATBOT & PREDICTION
# =====================================================

joblib.dump(
    X.columns.tolist(),
    "model_columns.pkl"
)

print("✅ Feature columns saved")

# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("✅ Train-test split completed")

# =====================================================
# RANDOM FOREST MODEL
# =====================================================

rf = RandomForestClassifier(
    random_state=42,
    class_weight="balanced"
)

# =====================================================
# HYPERPARAMETERS
# =====================================================

params = {

    "n_estimators": [100, 200],

    "max_depth": [5, 10, None],

    "min_samples_split": [2, 5],

    "min_samples_leaf": [1, 2]
}

# =====================================================
# GRID SEARCH
# =====================================================

grid = GridSearchCV(
    estimator=rf,

    param_grid=params,

    cv=5,

    scoring="accuracy",

    n_jobs=-1
)

# =====================================================
# TRAIN MODEL
# =====================================================

print("\n🚀 Training optimized Random Forest model...")

grid.fit(X_train, y_train)

print("✅ Model training completed")

# =====================================================
# BEST MODEL
# =====================================================

best_model = grid.best_estimator_

# =====================================================
# PREDICTIONS
# =====================================================

y_pred = best_model.predict(X_test)

y_prob = best_model.predict_proba(X_test)[:, 1]

# =====================================================
# EVALUATION METRICS
# =====================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

# =====================================================
# RESULTS
# =====================================================

print("\n🔥 BEST MODEL RESULTS")
print("=" * 50)

print(f"✅ Accuracy  : {accuracy:.4f}")

print(f"✅ ROC-AUC   : {roc_auc:.4f}")

print("\n📊 Classification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\n📌 Confusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

print("\n🏆 Best Parameters:")
print(grid.best_params_)

# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    best_model,
    "model.pkl"
)

print("\n💾 Optimized model saved as:")
print("   ✅ model.pkl")

print("\n💾 Feature columns saved as:")
print("   ✅ model_columns.pkl")

print("\n🎉 Training pipeline completed successfully!")