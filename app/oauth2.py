from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models, utils
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET KEY
#ALGORITHM
#EXPIRATION TIME FOR LOGIN OP

SECRETKEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def createToken(data: dict):
    toEncode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    toEncode.update({"exp" : expire})

    # THIS WILL ACTUALLY CREATE THE JWT TOKEN
    # MUST PASS HEADER, SECRET, PAYLOAD
    encodedJWT = jwt.encode(toEncode, SECRETKEY, algorithm=ALGORITHM)

    return encodedJWT

def verifyToken(token: str, exception):
    # TO DECODE, CREATE NEW KEY USING SECRETKEY AND PAYLOAD, COMPARE
    # Any of these lines can cause an error, so try/catch
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM])
        print(payload)
        id: str = payload.get("userID")

        if id is None:
            raise exception

        tokenData = schemas.TokenData(id=id)
    except JWTError:
        raise exception

    return tokenData

# QUESTION: what does depends do?
# We can use this function to verify a user before allowing them services like posting
def getCurrentUser(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Could not validate credentials", 
                            headers={"WWW-Authenticare" : "Bearer"})

    tokenData = verifyToken(token, exception) 
    print(tokenData)
    user = db.query(models.User).filter(models.User.id == tokenData.id).first()
    return user

