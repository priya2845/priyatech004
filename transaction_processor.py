from datetime import datetime
from transaction_monitor import TransactionFraudDetector

class TransactionProcessor:
    def __init__(self):
        self.fraud_detector = TransactionFraudDetector()
        
    def process_transaction(self, transaction):
        # Enrich transaction data
        enriched_data = self.enrich_transaction_data(transaction)
        
        # Validate transaction using AI model
        validation_result = self.fraud_detector.validate_transaction(enriched_data)
        
        if validation_result['status'] == 'approved':
            return self.execute_transaction(transaction)
        else:
            return self.handle_suspicious_transaction(transaction, validation_result)
    
    def enrich_transaction_data(self, transaction):
        return {
            'transaction_amount': transaction['amount'],
            'merchant_category': transaction['merchant']['category'],
            'time_of_day': datetime.now().hour,
            'location_match': self.verify_location(transaction),
            'device_id': transaction['device_id'],
            'transaction_frequency': self.get_user_transaction_frequency(transaction['user_id']),
            'average_transaction_amount': self.get_user_average_amount(transaction['user_id'])
        }
    
    def verify_location(self, transaction):
        # Simple location verification
        return True  # For testing purposes
    
    def get_user_transaction_frequency(self, user_id):
        # Return dummy frequency for testing
        return 5  # Assuming 5 transactions per day
    
    def get_user_average_amount(self, user_id):
        # Return dummy average amount for testing
        return 500.00
    
    def execute_transaction(self, transaction):
        # Simulate successful transaction
        return {
            'status': 'success',
            'message': 'Transaction processed successfully',
            'transaction_id': '12345'
        }
    
    def handle_suspicious_transaction(self, transaction, validation_result):
        # Handle rejected transaction
        return {
            'status': 'rejected',
            'message': 'Transaction flagged as suspicious',
            'risk_score': validation_result['risk_score']
        }