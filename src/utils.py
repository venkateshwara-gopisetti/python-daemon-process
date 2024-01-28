"""
Utility functions for defining pydantic classes for request bodies
"""

from pydantic import BaseModel

class Message(BaseModel):
    """
    Sample pydantic class for message
    """
    message:str

class Item(BaseModel):
    """
    Sample poydantic class for easy object creation
    """
    request_id:str
    thread_ident: str
    timestamp: str
    status: str
