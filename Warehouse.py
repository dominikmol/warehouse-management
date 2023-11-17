from Database import DataBase


class Warehouse (DataBase):
    # dodaj nowy magazyn
    def addWarehouse(self, warehouse_name, warehouse_location):
        # sprawdzanie czy wartości zostały poprawnie wprowadzone
        if not isinstance(warehouse_name, str) or not isinstance(warehouse_location, str):
            print("incorrectly entered data")
            return False
        
        # wyszukaj czy taki magazyn istnieje
        self.cursor.execute("""
                            SELECT * FROM Warehouse WHERE name=:n AND location=:l
                            """, {'n': warehouse_name, 'l': warehouse_location})

        # jeśli istnieje to zakończ
        if self.cursor.fetchone() is not None:
            print("taki magazyn już jest w bazie")
            return

        # dodaj nowy magazyn
        with self.connection:
            self.cursor.execute("""
                                INSERT INTO Warehouse (name, location) VALUES(?,?)
                                """, (warehouse_name, warehouse_location))

    # edycja nazwy magazynu o nazwie x
    def editName(self, old_name, new_name):
        # sprawdzanie czy wartości zostały poprawnie wprowadzone
        if not isinstance(old_name, str) or not isinstance(new_name, str):
            print("incorrectly entered data")
            return False
        
        # wyszukiwanie czy taki magazyn istnieje
        self.cursor.execute("""
                            SELECT * FROM Warehouse WHERE name=:n
                            """, {'n': old_name})

        # jeśli nie ma to zakończ funkcje
        if self.cursor.fetchone() is None:
            print("nie ma takiego magazynu obecnie")
            return

        # zaktualizuj nazwe magazynu
        with self.connection:
            self.cursor.execute("""
                                UPDATE Warehouse SET name=:n1 WHERE name=:n2
                                """, {'n1': new_name, 'n2': old_name})

    # edycja lokacji magazynu o nazwie x
    def editLocation(self, warehouse_name, new_location):
        # sprawdzanie czy wartości zostały poprawnie wprowadzone
        if not isinstance(warehouse_name, str) or not isinstance(new_location, str):
            print("incorrectly entered data")
            return False
        
        # wyszukiwanie czy taki magazyn istnieje
        self.cursor.execute("""
                            SELECT * FROM Warehouse WHERE name=:n
                            """, {'n': warehouse_name})

        # jeśli nie ma to zakończ funkcje
        if self.cursor.fetchone() is None:
            print("nie ma takiego magazynu obecnie")
            return

        # zaktualizuj lokacje magazynu
        with self.connection:
            self.cursor.execute("""
                                UPDATE Warehouse SET location=:l WHERE name=:n
                                """, {'l': new_location, 'n': warehouse_name})

    # wyświetl wszystkie magazyny
    def showWarehouses(self):
        self.cursor.execute(
            "SELECT name, location FROM Warehouse")
        search = self.cursor.fetchall()

        if search is None:
            return

        for warehouse in search:
            print(f"name: {warehouse[0]} --- location: {warehouse[1]}")


def main():
    inv = Warehouse()
    inv.showWarehouses()


main()
