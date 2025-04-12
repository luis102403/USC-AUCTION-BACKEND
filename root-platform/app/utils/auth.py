import os
import jwt
import datetime




class JWTUtility:

    #SECRET_KEY = os.getenv['SECRET_KEY'] #Secure secret key to sign the token
    SECRET_KEY = 'sweds'


    @staticmethod
    def generate_jwt(payload, exp_time=600, **kwargs): 
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_time) #set "exp" claim in payload, if not exists its created.
        payload['iat'] = datetime.datetime.utcnow() #set "iat" claim about JWT time creation.

        # Add any additional claims passed via kwargs
        for key, value in kwargs.items():
            payload[key] = value

        token = jwt.encode(payload, JWTUtility.SECRET_KEY , algorithm='HS256')#generate and token signature
        print(f"exp claim of payload: {payload['exp']}")
        return token


    @staticmethod
    def verify_token(token, verify_exp=True):
        try:
            decoded_payload = jwt.decode(token,JWTUtility.SECRET_KEY , algorithms=['HS256'], options={"verify_exp":verify_exp})
            return decoded_payload
        except jwt.ExpiredSignatureError as e:
            return f'Token has expired {e}'
        except jwt.InvalidTokenError as e:
            return f'Invalid token {e}'
        except jwt.DecodeError as e:
            return f'Token is not in a valid format {e}'
        except jwt.ImmatureSignatureError as e:
            return f'Token validity not yet initialized {e}'
        except Exception:
            return 'An error occurred while decoding token'
        
    @staticmethod
    def verify_token_by_cc(token):
        decoded_payload = JWTUtility.verify_token(token=token)

        if isinstance(decoded_payload, str): #If verify_token returned a error message (string)
            return decoded_payload

        cc = decoded_payload.get('cc', 'Claim "cc" not found.')
        return cc



    @staticmethod
    def refresh_token(token, exp_time):
        decoded_payload = JWTUtility.verify_token(token, False) #To verify the old token validity ignoring the exp claim and get its payload anyway.
        
        if isinstance(decoded_payload, str): #If verify_token returned a error message (string)
            return decoded_payload 
        
        #If token is valid, its generate new token with payload info of old token.

        new_payload = decoded_payload.copy()
        return JWTUtility.generate_jwt(new_payload, exp_time)





    








    