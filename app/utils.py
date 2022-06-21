from passlib.context import CryptContext

######################################### FILE SUMMARY:
########### THIS FILE CONTAINS MISC UTILITIES, LIKE PASSWORD HASHING LOGIC/IMPORTS, COMPARING HASHES

# This line tells passlib what hashing algo we using to encrypt passwords on PostgreSQL database
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plainPass: str, hashedPass):
    return pwd_context.verify(plainPass, hashedPass)
