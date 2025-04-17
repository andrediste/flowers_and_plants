def init_metadata():
    from db.metadata import Base
    from db.orders import models

    return Base.metadata
