
"""REST API for the HR Management System."""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="HR Management System", version="1.0.0")


class EmployeeCreate(BaseModel):
    """Validate employee details supplied by API clients."""

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(min_length=2, max_length=100)
    salary: float = Field(gt=0)


class Employee(EmployeeCreate):
    """Represent an employee with a unique identifier."""

    id: int


employees: dict[int, Employee] = {}


@app.get("/health")
def health_check():
    """Return the application's health status."""
    return {"status": "ok"}


@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee_data: EmployeeCreate):
    """Create an employee if the email is not already registered."""
    if any(
        employee.email == employee_data.email
        for employee in employees.values()
    ):
        raise HTTPException(
            status_code=409,
            detail="An employee with this email already exists",
        )

    employee_id = max(employees, default=0) + 1
    employee = Employee(id=employee_id, **employee_data.model_dump())
    employees[employee_id] = employee
    return employee


@app.get("/employees", response_model=list[Employee])
def list_employees():
    """Return all registered employees."""
    return list(employees.values())


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    """Return an employee by ID or raise a not-found error."""
    employee = employees.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee_data: EmployeeCreate):
    """Replace an employee's details while preserving their ID."""
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")

    if any(
        existing_id != employee_id and employee.email == employee_data.email
        for existing_id, employee in employees.items()
    ):
        raise HTTPException(
            status_code=409,
            detail="An employee with this email already exists",
        )

    updated_employee = Employee(
        id=employee_id,
        **employee_data.model_dump(),
    )
    employees[employee_id] = updated_employee
    return updated_employee


@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_employee(employee_id: int):
    """Delete an employee or raise a not-found error."""
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees[employee_id]
