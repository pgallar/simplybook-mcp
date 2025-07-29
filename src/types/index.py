from typing import TypedDict, List, Optional

class Service(TypedDict):
    id: str
    name: str
    description: Optional[str]

class Booking(TypedDict):
    id: str
    service_id: str
    customer_id: str
    start_time: str
    end_time: str
    status: str

class Customer(TypedDict):
    id: str
    name: str
    email: str
    phone: Optional[str]

class ApiResponse(TypedDict):
    success: bool
    data: Optional[List[Any]]
    message: Optional[str]