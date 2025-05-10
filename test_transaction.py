from transaction_processor import TransactionProcessor
import matplotlib.pyplot as plt
import numpy as np

def test_fraud_detection():
    try:
        # Initialize the processor
        processor = TransactionProcessor()
        
        # Sample transaction data with all required fields
        test_transaction = {
            'amount': 1000.00,
            'merchant': {
                'category': 'electronics'
            },
            'device_id': 'device_123',
            'user_id': 'user_456',
            'location': {
                'latitude': 40.7128,
                'longitude': -74.0060
            },
            'time_of_day': 14,
            'location_match': True,
            'transaction_frequency': 5,
            'average_transaction_amount': 800.00
        }
        
        # Process the transaction
        result = processor.process_transaction(test_transaction)
        
        if result and isinstance(result, dict):
            # Create visualization
            plt.figure(figsize=(10, 6))
            
            # Create bar chart
            risk_score = result.get('risk_score', 0)  # Default to 0 if not found
            threshold = 0.7
            
            bars = plt.bar(['Risk Score', 'Threshold'], [risk_score, threshold])
            bars[0].set_color('green' if result.get('status') == 'approved' else 'red')
            bars[1].set_color('gray')
            
            # Customize the plot
            plt.title('Transaction Fraud Risk Analysis')
            plt.ylabel('Risk Score')
            plt.ylim(0, 1)
            
            # Add transaction status
            status_text = f"Status: {result.get('status', 'UNKNOWN').upper()}\n{result.get('reason', 'No reason provided')}"
            plt.text(0.5, -0.2, status_text, ha='center', transform=plt.gca().transAxes)
            
            # Show the plot
            plt.show()
            
            # Print numerical results
            print("Transaction Processing Result:", result)
        else:
            print("Error: Invalid result format returned from transaction processing")
            
    except Exception as e:
        print(f"Error processing transaction: {str(e)}")

if __name__ == "__main__":
    test_fraud_detection()