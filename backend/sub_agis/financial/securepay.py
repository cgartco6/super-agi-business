import stripe
from typing import Dict, Any
from ..security.encryption_manager import encrypt_data

class SecurePay:
    def __init__(self):
        self.stripe_api = stripe
        self.stripe_api.api_key = config.STRIPE_SECRET_KEY
        self.fund_allocation = {
            'ai_fund': 0.20,
            'reserve': 0.30,
            'owner': 0.50
        }
    
    def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process payment and allocate funds according to business rules"""
        try:
            # Create Stripe charge
            charge = self.stripe_api.Charge.create(
                amount=int(payment_data['amount'] * 100),  # Convert to cents
                currency=payment_data['currency'],
                source=payment_data['token'],
                description=payment_data['description']
            )
            
            if charge['paid']:
                # Allocate funds
                allocation = self._allocate_funds(payment_data['amount'])
                # Store encrypted transaction
                self._store_transaction(payment_data, charge.id, allocation)
                
                return {
                    'status': 'success',
                    'transaction_id': charge.id,
                    'allocation': allocation
                }
            else:
                return {'status': 'failed', 'reason': charge['failure_message']}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _allocate_funds(self, amount: float) -> Dict[str, float]:
        """Calculate fund allocation based on business rules"""
        return {
            'ai_fund': round(amount * self.fund_allocation['ai_fund'], 2),
            'reserve': round(amount * self.fund_allocation['reserve'], 2),
            'owner': round(amount * self.fund_allocation['owner'], 2)
        }
    
    def _store_transaction(self, payment_data: Dict, charge_id: str, allocation: Dict) -> None:
        """Securely store transaction details"""
        encrypted_data = encrypt_data({
            'original_data': payment_data,
            'charge_id': charge_id,
            'allocation': allocation,
            'timestamp': datetime.now()
        })
        
        # Save to database
        db.execute(
            "INSERT INTO transactions (encrypted_data) VALUES (?)",
            (encrypted_data,)
        )
