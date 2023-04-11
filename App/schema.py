from pydantic import BaseModel, EmailStr
from datetime import datetime


class Add_Sensor(BaseModel):
    SensorID: int
    SensorName: str
    SensorType: str
    Location: str
    class Config:
        orm_mode = True





class Write_Data(BaseModel):
    SensorID: int
    SensorData: str  
    # Timestamp: datetime = datetime.now()
    



class Read_Data(BaseModel):
    SensorID: int
    SensorData: str
    Timestamp: datetime
    
    

class User(BaseModel):
    Email: EmailStr
    Password:str
    
        
class VerifyUser(BaseModel):
    Email:EmailStr
    Password:str        
        

        