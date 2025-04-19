from fastapi import Form, HTTPException
import env
import jwt

def create_jwt_token(data: str):
    try:
        token = jwt.encode({"id": data}, env.JWT_SECRET, algorithm="HS256")
        return token
    except:
        return None

async def validate_and_decode_jwt(token: str = Form(...)):
    try:
        # check for cookie
        print("Request Cookies:", token)
        if token is None:
            raise HTTPException(401)
        # decode token
        decoded_token = jwt.decode(token, env.JWT_SECRET, algorithms=["HS256"])
        return decoded_token["id"]
    except Exception as e:
        print("Error:", e)
        raise HTTPException(401)
