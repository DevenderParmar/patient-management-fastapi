from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
app = FastAPI()  # object


class Patient(BaseModel):
    id: Annotated[str,
                  Field(..., description='Id number of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='The name of the patient')]
    city: Annotated[str,
                    Field(..., description='The name of the city of the patient')]
    age: Annotated[int, Field(..., ge=0, le=120,
                              description='The age of the patient')]
    gender: Annotated[Literal['male', 'female', 'other'],
                      Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., ge=1,
                                   description='height of the Patientin meters')]
    weight: Annotated[float, Field(..., ge=1,
                                   description='weighto of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 0)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'underage'
        elif self.bmi >= 18.5 and self.bmi <= 24.9:
            return 'normal'
        elif self.bmi >= 25 and self.bmi <= 29.9:
            return 'overweight'
        elif self.bmi >= 30:
            return 'obese'
        
class UpdatePatient(BaseModel):
    name : Annotated[Optional[str],Field(default=None)]
    city :Annotated[Optional[str],Field(default=None) ]
    age :Annotated[Optional[int],Field(default= None,ge=0)]
    gender :Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height :Annotated[Optional[float],Field(default=None,ge=0)]
    weight :Annotated[Optional[float],Field(default=None,ge=0)]


def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)


def load_data():
    with open("patient.json", 'r') as f:
        data = json.load(f)
        return data


@app.get("/")  # route create kara
def hello():
    # return {"message":"hello world"}
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patients records"}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="This is the Patient id for DB", example=["P001"])):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail='Patient id not found')


@app.get('/sort')
def sort_patient(
        sort_by: str = Query(..., description='sort patient based on height, weight, bmi', example=['height']), order: str = Query('asc', description='order of sorting like asc or desc', example='asc')):

    valid_field = ['height', 'weight', 'bmi']

    if sort_by not in valid_field:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Please select from {valid_field}"
        )

    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Please select asc or desc"
        )

    data = load_data()
    sort_order = True if order == 'desc' else False

    sort_data = sorted(data.values(), key=lambda x: x.get(
        sort_by, 0), reverse=sort_order)

    return sort_data


@app.post('/create')
def create_patient(patient: Patient):

    data = load_data()

    if patient.id in data:

        raise HTTPException(
            status_code=400, detail='The Patient id already exist')

    data[patient.id] = patient.model_dump(exclude='id')
    
    save_data(data)
    return JSONResponse(status_code= 201,content = {'message':'New patient created successfully'}) 

@app.put('/edit/{patient_id}')
def edit_patient_details(patient_id:str ,update_patient:UpdatePatient):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient doesnt exist')
    
    existed_data = data[patient_id]
    
    updated_data = update_patient.model_dump(exclude_unset=True)
    
    for key,value in updated_data.items():
        existed_data[key] = value
    
    
    existed_data['id'] = patient_id
    updated_patient_object = Patient(**existed_data)
    
    existed_data = updated_patient_object.model_dump(exclude='id')
        
    data[patient_id]  = existed_data
    
    save_data(data)
    
    return JSONResponse(status_code=200,content={'message':'patient updated successfully'})
     
