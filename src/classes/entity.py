from pydantic import BaseModel


class EntityParams(BaseModel):
    # id: str # TODO: leave for the time being, make optional in future
    entity_type: str
    group_name: str


class Entity:
    def __init__(self, entity_params: EntityParams):
        # self.id = entity_params.id
        self.entity_type = entity_params.entity_type
        self.group_name = entity_params.group_name
