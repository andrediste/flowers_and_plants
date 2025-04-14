def init_metadata():
    from db.metadata import Base
    from db.models.orders import orders

    return Base.metadata
