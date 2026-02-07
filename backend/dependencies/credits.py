from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.auth import get_current_user
from core.database import get_db
from models import User

def consume_credit(cost: int = 1):
    async def credit_dependency(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
        if user.credits < cost:
            raise HTTPException(status_code=402, detail="Insufficient credits")
        
        # Deduct credits
        user.credits -= cost
        await db.commit()
        await db.refresh(user)
        
        try:
            yield user
        except HTTPException as e:
            # If the endpoint raises a 4xx error (client error), refund the credit
            if e.status_code >= 400:
                user.credits += cost
                await db.commit()
            raise e
        except Exception as e:
            # For unhandled exceptions (500s), we also refund? 
            user.credits += cost
            await db.commit()
            raise e

    return credit_dependency
