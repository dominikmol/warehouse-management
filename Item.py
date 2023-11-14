from Database import DataBase


class Item (DataBase):
    # dodaj nowy przedmiot do magazynu
    def addItem(self, item_name, price):
        self.cursor.execute("""
                            SELECT name FROM Item WHERE name=:n
                            """, {'n': item_name})

        if self.cursor.fetchone() is not None:
            return

        with self.connection:
            self.cursor.execute(
                'INSERT INTO Item (name, price) VALUES(?,?)', (item_name, price))

    # edytuj nazwe przedmiotu o nazweie x
    def editName(self, old_name, new_name):
        self.cursor.execute(
            "SELECT id FROM Item WHERE name=:n", {'n': old_name})

        if self.cursor.fetchone() is None:
            return

        with self.connection:
            self.cursor.execute(
                "UPDATE Item SET name=:n1 WHERE name=:n2", {'n1': new_name, 'n2': old_name})

    # edytuj cene przedmiotu o nazweie x
    def editPrice(self, item_name, new_price):
        self.cursor.execute(
            "SELECT id FROM Item WHERE name=:n", {'n': item_name})

        if self.cursor.fetchone() is None:
            return

        with self.connection:
            self.cursor.execute(
                "UPDATE Item SET price=:p WHERE name=:n", {'p': new_price, 'n': item_name})


def main():
    inv = Item()
    inv.addItem('myszka Razer', 99.99)


main()
