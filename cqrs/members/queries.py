from typing import List
from domain.data.sqlalchemy_models import Profile_Members

class ProfileMembersListQuery:
    def __init__(self):
        self._records: List[Profile_Members] = list()
        
    @property
    def records(self):
        return self._records
    
    @records.setter
    def records(self, records):
        self._records = records