import datetime
import hashlib
import hmac
import json
from passlib.context import CryptContext
import bcrypt, base64
import time
from datetime import datetime, timezone
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_text(input: str) :
    return bcrypt.hashpw(input.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')    

def verify_password(user_password: str, hashed_password: str)-> bool:    
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def base64_url_encode(data):
    """Encodes data to Base64 URL format without padding."""
    encoded = base64.urlsafe_b64encode(data).rstrip(b'=')
    return encoded.decode('utf-8')

def base64_url_decode(encoded):
    """Decodes Base64 URL-encoded data."""
    # Add padding to the Base64 URL string
    padding = '=' * (4 - len(encoded) % 4)
    return base64.urlsafe_b64decode(encoded + padding)

def generate_jwt(payload, secret, algorithm='HS256'):    
    if algorithm != 'HS256':
        raise ValueError("Only 'HS256' algorithm is supported in this example.")
    
    # Header
    header = {
        "alg": algorithm,
        "typ": "JWT"
    }    
    # Encode Header
    encoded_header = base64_url_encode(json.dumps(header).encode('utf-8'))    
    # Encode Payload
    encoded_payload = base64_url_encode(json.dumps(payload).encode('utf-8'))    
    # Create Signature
    signing_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    signature = hmac.new(
        secret.encode('utf-8'),
        signing_input,
        hashlib.sha256
    ).digest()
    
    encoded_signature = base64_url_encode(signature)
    
    # Combine all parts
    jwt_token = f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    return jwt_token

def decode_jwt(token, secret, verify=True,check_exp=True):    
    try:
        # Split the token into parts
        encoded_header, encoded_payload, encoded_signature = token.split('.')
        
        # Decode the header and payload
        header = json.loads(base64_url_decode(encoded_header).decode('utf-8'))
        payload = json.loads(base64_url_decode(encoded_payload).decode('utf-8'))
        
        # Verify the signature if required
        if verify:
            signing_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
            expected_signature = hmac.new(
                secret.encode('utf-8'),
                signing_input,
                hashlib.sha256
            ).digest()
            encoded_expected_signature = base64.urlsafe_b64encode(expected_signature).rstrip(b'=').decode('utf-8')
            
            if encoded_signature != encoded_expected_signature:
                raise ValueError("Invalid signature: Token verification failed.")
            if check_exp:
                current_time = datetime.now(timezone.utc)
                if "exp" in payload:
                    exp_value = payload["exp"]
                    if exp_value.startswith('"') and exp_value.endswith('"'):
                        exp_value = exp_value.strip('"')
                    print("<----------- the payload exp is ---------",payload["exp"])  
                    #exp_time = datetime.fromtimestamp(float(exp_value), tz=timezone.utc)  
                    exp_time = datetime.fromisoformat(exp_value)  
                    
                    if current_time >= exp_time:
                        raise ValueError("Token has expired. ",exp_value)
                    else:
                        print("<--------- token not expired----------->",exp_value)
        
        return {"header": header, "payload": payload}
    
    except Exception as e:
        raise ValueError(f"Failed to decode token: {e}")

# Example usage
#if __name__ == "__main__":
#    payload = {
#        "sub": "1234567890",
#        "name": "John Doe",
#        "iat": 1609459200
#    }
#    secret_key = "your-256-bit-secret"
#    token = generate_jwt(payload, secret_key)
#    print(f"Generated JWT: {token}")
