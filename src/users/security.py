from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId

from src.db.mongo import get_db
from src.common.constants import USERS_COL
from src.common.security import decode_token

security = HTTPBearer()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db)
):
    payload = decode_token(creds.credentials)

    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("sub")
    user = await db[USERS_COL].find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user["id"] = str(user["_id"])
    return user


async def get_current_user_id(user=Depends(get_current_user)) -> str:
    return user["id"]

