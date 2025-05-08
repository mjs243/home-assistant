def get_domain(entity_id):
    """Get the domain of an entity based on its entity_id"""
    if "." in entity_id:
        return entity_id.split(".")[0]
    else:
        raise ValueError("Invalid entity_id format")