from db import models

models.create_db_session()

results = session.query(models.SomeTable).filter(models.SomeTable.field1>0)

print results

models.end_db_session(session)
