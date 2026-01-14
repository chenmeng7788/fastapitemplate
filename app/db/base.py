from app.db.session import engine
from app.models import user

user.Base.metadata.create_all(bind=engine)