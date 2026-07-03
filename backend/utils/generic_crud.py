from database.connection import db
from sqlalchemy.exc import IntegrityError


class GenericCrud:

    def __init__(self, model):
        self.model = model


    def create(self, data):

        if not data:
            raise ValueError("Dados não enviados")


        obj = self.model(**data)

        try:
            db.session.add(obj)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erro de integridade dos dados")

        return obj


    def get_all(self):

        return self.model.query.all()


    def get_by_id(self, id):

        if not isinstance(id, int):
            raise ValueError("ID inválido")

        obj = self.model.query.get(id)

        if not obj:
            raise ValueError("Registro não encontrado")

        return obj


    def update(self, id, data):

        if not data:
            raise ValueError("Dados não enviados")


        obj = self.get_by_id(id)

        try:

            for key, value in data.items():

                if hasattr(obj, key):
                    setattr(obj, key, value)

            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            raise ValueError("Erro ao atualizar")

        return obj


    def delete(self, id):

        obj = self.get_by_id(id)

        try:

            db.session.delete(obj)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(e)
            raise ValueError(str(e))

        return True