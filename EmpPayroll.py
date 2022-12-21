# Importing Necessary Modules
from pydantic import BaseModel
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import date
import uvicorn
import pyodbc


# Connecting Microsoft sql server managemnt studio
connect = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=(localdb)\ProjectModels;"
                      "Database=EmployeePayrollSystem;"
                      "Trusted_Connection=yes;")


cursor = connect.cursor()

# Creating objects of jinja template
templates = Jinja2Templates(directory='templates')

# Creating object of FastApi
api = FastAPI()

# Creating EmpoyeePayroll Class
class EmployeePayroll(BaseModel):
    id: int
    name: str
    gender: str
    profile_image: str
    department: str
    start_date: date
    salary: float
    

@api.get('/home/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})

@api.get('/get_employee/{id}', response_class=HTMLResponse)
def get_employee(request: Request, id):
    try:
        query = f'SELECT * FROM emp_payroll WHERE id = {id}'
        cursor.execute(query)
        employee = [row for row in cursor]
        data = {"id": employee[0][0], "Name": employee[0][1], "Gender": employee[0][2] ,"ProfileImage": employee[0][3],"Department": employee[0][4], "StartDate": employee[0][5], "Salary": employee[0][6]}
        if employee is not None:
            return templates.TemplateResponse('employee.html', {"request": request, "data": data})
        else:
            return {"message": "Please check the entered details"}
    except Exception as e:
        print(e)
    
@api.get('/display_employee/', response_class=HTMLResponse)
def display_employee(request: Request):
    try:
        query = 'SELECT * FROM emp_payroll'
        cursor.execute(query)
        employee = [row for row in cursor]
        if employee:
            data = employee
            return templates.TemplateResponse('employee.html', {"request": request, "data": data})
        else:
            return {"message": "Please check the entered details"}
    except Exception as e:
        print(e)

@api.post('/add_employee/')
def add_employee(emp: EmployeePayroll):
    try:
        query = f"INSERT INTO emp_payroll VALUES ({emp.id}, '{emp.name}', '{emp.gender}', '{emp.profile_image}' ,'{emp.department}', '{emp.start_date}', {emp.salary})"
        cursor.execute(query)
        connect.commit()
        return {"status": 200, "message": "Successfully Added The New Employee Detail"}
    except Exception as e:
        print(e)

@api.delete('/delete_employee/{id}')
def delete_employee(id):
    try:
        query = f'DELETE FROM emp_payroll WHERE id = {id}'
        cursor.execute(query)
        connect.commit()
        return {"status": 200, "message": "Successfully Deleted The Employee Detail"}
    except Exception as e:
        print(e)
    
@api.put('/update_employee/{id}')
def update_employee(id, emp:EmployeePayroll):
    try:
        show_data_query = f"UPDATE emp_payroll SET Name = '{emp.name}', Gender ='{emp.gender}' ,ProfileImage = '{emp.profile_image}',Department = '{emp.department}', StartDate = '{emp.start_date}', Salary = {emp.salary} WHERE Id = {emp.id}"
        cursor.execute(show_data_query)
        connect.commit()
        emp_data = get_employee(id)
        return {"status": 200, "message": "Successfully Updated The Employee Detail", "data": emp_data.items() }
    except Exception as e:
        print(e)

if __name__ == '__main__':
    uvicorn.run("EmpPayroll:api", host="127.0.0.1", port=8000)
    