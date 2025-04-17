from fastapi import Request, HTTPException
import env
import jwt

def create_jwt_token(data: str):
    try:
        token = jwt.encode({"id": data}, env.JWT_SECRET, algorithm="HS256")
        return token
    except:
        return None

async def validate_and_decode_jwt(request: Request):
    try:
        # check for cookie
        token = request.cookies["token"]
        decoded_token = jwt.decode(token, env.JWT_SECRET, algorithms=["HS256"])
        return decoded_token["id"]
    except Exception as e:
        print("Error:", e)
        raise HTTPException(401)
