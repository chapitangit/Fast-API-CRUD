import strawberry
from typing import Optional,List

from datetime import date, datetime


from  ..database.mongodb import create_mongo_client
mydb = create_mongo_client()


@strawberry.input
class EmployeeDetails:
    employee_id: Optional[str] = None
    employee_name: Optional[str] = None
    division: Optional[str] = None
    position: Optional[str] = None
    status: bool
    created: Optional[datetime] = None
    updated: Optional[datetime] = None


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def insert_employee(self, employee_details: EmployeeDetails) -> str:
        if not employee_details.employee_id:
            return "Employee ID cannot be null"
        
        employee_collection = mydb['employee']
        
        # Check if an employee with the same employee_id or employee_name already exists
        existing_employee = employee_collection.find_one({
            "$or": [
                {"employee_id": employee_details.employee_id},
                {"employee_name": employee_details.employee_name}
            ]
        })
        
        if existing_employee:
            return "Employee with this ID or name already exists"
        
        employee_data = employee_details.__dict__
        employee_data['created'] = employee_data.get('created') or datetime.now()
        employee_data['updated'] = datetime.now().isoformat()
        
        # Insert the employee data into the MongoDB collection
        result = employee_collection.insert_one(employee_data)
        
        if result.inserted_id:
            return f"Employee inserted with ID: {result.inserted_id}"
        else:
            return "Failed to insert employee"




# @strawberry.type
# class Mutation:
#     @strawberry.mutation
#     async def insert_employee(self, employee_details: EmployeeDetails) -> str:
#         employee_data = employee_details.__dict__
#         employee_data['created'] = employee_data.get('created') or datetime.now()
#         employee_data['updated'] = datetime.now().isoformat()

#         # Insert the employee data into the MongoDB collection
#         employee_collection = mydb['employee']
#         result = employee_collection.insert_one(employee_data)
        
#         if result.inserted_id:
#             return f"Employee inserted with ID: {result.inserted_id}"
#         else:
#             return "Failed to insert employee"
