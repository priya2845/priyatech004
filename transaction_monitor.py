from sklearn.ensemble import RandomForestClassifier
import numpy as np

class TransactionFraudDetector:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.merchant_categories = {
            'electronics': 1,
            'clothing': 2,
            'food': 3,
            'entertainment': 4,
            'other': 0
        }
        self._initial_training()
    
    def preprocess_transaction(self, transaction_data):
        # Convert merchant category to numeric
        merchant_cat = str(transaction_data['merchant_category']).lower()
        merchant_cat_num = self.merchant_categories.get(merchant_cat, 0)
        
        # Convert boolean to integer
        location_match_num = 1 if transaction_data['location_match'] else 0

        
        # Convert device_id string to a numeric value using a more stable method
        device_id_str = str(transaction_data['device_id'])
        try:
            # Extract numeric parts if device ID contains numbers
            numeric_parts = ''.join(filter(str.isdigit, device_id_str))
            device_id_num = int(numeric_parts) if numeric_parts else 0
            # Ensure the number is within a reasonable range
            device_id_num = device_id_num % 1000
        except ValueError:
            device_id_num = 0
        
        # Create feature array
        features = [
            float(transaction_data['transaction_amount']),
            float(merchant_cat_num),
            float(transaction_data['time_of_day']),
            float(location_match_num),
            float(device_id_num),
            float(transaction_data['transaction_frequency']),
            float(transaction_data['average_transaction_amount'])
        ]
        return np.array(features).reshape(1, -1)

    def _initial_training(self):
        # Dummy training data (you should replace this with real historical data)
        X_train = np.array([
            [100, 1, 12, 1, 1, 5, 150],  # Normal transaction
            [1000, 2, 2, 1, 2, 3, 200],  # Normal transaction
            [5000, 3, 3, 0, 3, 1, 100],  # Fraudulent transaction
            [300, 1, 14, 1, 4, 4, 250],  # Normal transaction
            [3000, 4, 23, 0, 5, 1, 300],  # Fraudulent transaction
        ])
        y_train = np.array([0, 0, 1, 0, 1])  # 0: Normal, 1: Fraudulent
        
        # Fit the model with initial data
        self.model.fit(X_train, y_train)
    
    def predict_fraud_probability(self, transaction_data):
        processed_data = self.preprocess_transaction(transaction_data)
        fraud_probability = self.model.predict_proba(processed_data)[0][1]
        return fraud_probability
    
    def validate_transaction(self, transaction_data, threshold=0.7):
        fraud_prob = self.predict_fraud_probability(transaction_data)
        if fraud_prob > threshold:
            return {
                'status': 'rejected',
                'risk_score': fraud_prob,
                'reason': 'High fraud probability detected'
            }
        return {
            'status': 'approved',
            'risk_score': fraud_prob,
            'reason': 'Transaction appears legitimate'
        }