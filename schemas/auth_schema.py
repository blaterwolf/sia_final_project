from pydantic import BaseModel

# * TokenData
# ? Kailangan to para sa paggawa nung access_token. Kinginang yan.


class TokenData(BaseModel):
    author_id: str
    user_name: str

# * AuthForm
# ? So kapag nag-POST tayo ito yung parang isesend natin na JSON file tapos ito yung parang schema na gagamitin yung mga req.body na nga na eme


class AuthForm(BaseModel):
    user_name: str
    password: str
