import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, status, Response, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel
import time
from . import schema



app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'postgres', user='postgres', password = '10p19fb1094', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was succesful")
        break
    except Exception as error:
        print("Connection to database failed")    
        print("Error:", error)
        time.sleep(2)
        
        
        
# Add Sensor
@app.post("/add_sensor",status_code=status.HTTP_201_CREATED)
def add_sensor(sensor: schema.Add_Sensor):
    print(sensor)
    cursor.execute("""INSERT INTO sensordetail (sensor_id, sensor_name, sensor_type, location) VALUES (%s, %s, %s, %s) RETURNING * """,(sensor.SensorID, sensor.SensorName, sensor.SensorType, sensor.Location))
    new_sensor = cursor.fetchone()
    conn.commit()
    return {"New Sensor" : new_sensor}



# Write From NodeMCU
@app.post("/add_data",status_code=status.HTTP_201_CREATED)
def add_data(data: schema.Write_Data):
    cursor.execute("""INSERT INTO sensordata (sensor_id, sensor_data) VALUES (%s, %s) RETURNING * """,(data.SensorID, data.SensorData))
    new_data = cursor.fetchone()
    conn.commit()
    return {"New Data" : new_data}
    
    
#Read from the database with an ID
@app.get("/read_data/{id}")
def read_data(id : int):
    cursor.execute("""SELECT * FROM sensordata WHERE sensor_id = %s """,(str(id)))
    Sensor_data = cursor.fetchall()
    if not Sensor_data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=  f"the sensor data with id {id} was not found")
    return {"Sensor_Data" : Sensor_data}


# Delete a sensor from the database
@app.delete("/delete_sensor/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(id: int):
    cursor.execute("""DELETE FROM sensordetails WHERE sensor_id = %s RETURNING *""",(str(id)),)
    deleted_sensor = cursor.fetchone()
    if deleted_sensor==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the id:{id} doesn't exist") 

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Create a User
@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(user_data : schema.User):
    cursor.execute("""INSERT INTO user_details (email, password) VALUES (%s, %s) RETURNING *""",(user_data.Email, user_data.Password))
    new_user = cursor.fetchone()
    conn.commit()
    return {"New user" : new_user}

# Verify the User
@app.post("/verify_user")
def verify_user( User : schema.VerifyUser):
    cursor.execute("""SELECT * FROM user_details WHERE email = %s AND password = %s""", (User.Email,User.Password ))
    user_data = cursor.fetchone()
    if not user_data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"user was not found")
    return {"Status" : "Verified"}