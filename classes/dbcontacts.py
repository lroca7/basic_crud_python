from .contact import Contact
# from .dbcsv import DBbyCSV
from .dbpostgresql import DBPostgresql

SCHEMA = {
    'id': {
        'type': 'autoincrement',
    }, 
    'name': {
        'type': 'string',
        'min_length': 3,
        'max_length': 50
    }, 
    'surname': {
        'type': 'string',
        'min_length': 5,
        'max_length': 100
    }, 
    'email': {
        'type': 'string',
        'max_length': 254
    }, 
    'phone': {
        'type': 'int'
    }, 
    'birthday': {
        'type': 'date'
    }
}

class DBContacts(DBPostgresql):

    def __init__(self):
        super().__init__(SCHEMA, 'contacts')

    
    def save_contact(self, contact):
        data = {
            'name':contact.name, 
            'surname':contact.surname, 
            'email':contact.email, 
            'phone':contact.phone, 
            'birthday':contact.birthday
        }
        return self.insert(data)
    

    def update_contact(self, id_object, data):
        if not id_object:
            raise ValueError('Debes envíar el id del contacto')
        if not data:
            raise ValueError('Debes envíar al menos un parámetro a actualizar')
        self.update(id_object, data)


    def delete_contact(self, id_object):
        if not id_object:
            raise ValueError('Debes envíar el id del contacto')
        self.delete(id_object)


    def list_contacts(self):
        list_contacts = self.get_all()
        return self._create_object_contacts(list_contacts)

    
    def get_schema(self):
        return SCHEMA


    def search_contacts(self, filters):
        if not filters:
            raise ValueError('Debes envíar al menos un filtro')

        list_contacts = self.get_by_filters(filters)
        return self._create_object_contacts(list_contacts)


    def _create_object_contacts(self, list_contacts):

        if not list_contacts:
            return None

        object_contacts = []
        # Convertimos los datos a objectos de tipo contact
        for contact in list_contacts:
            c = Contact(contact['id'], contact['name'], contact['surname'], contact['email'], contact['phone'], contact['birthday'])
            object_contacts.append(c)

        return object_contacts