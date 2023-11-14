from Database import DataBase


class Operation (DataBase):
    # add new items to the Warehouse
    def addItemToWarehouse(self, item_name, warehouse_name, quantity):
        # sprawdz czy istnieje podany przedmiot, magazyn oraz czy typ operacji istnieje
        self.cursor.execute("""
                            SELECT Item.id, Warehouse.id, OperationType.id
                            FROM Item, Warehouse, OperationType
                            WHERE Item.name=:in AND Warehouse.name=:wn AND OperationType.name = 'add items'
                            """, {'in': item_name, 'wn': warehouse_name})
        search = self.cursor.fetchone()
        if search is None:
            return False

        # jeśli podane rzeczy są dodaj nową operacje
        with self.connection:
            self.cursor.execute("""
                                INSERT INTO Operation (itemId, warehouseId, operationTypeId, quantity) VALUES (?,?,?,?)
                                """, (search[0], search[1], search[2], quantity))

        # po wykonanej operacji sprawdź czy już ten przedmiot jest w wskazanym magazynie
        self.cursor.execute("""
                            SELECT id, quantity 
                            FROM StockStatus 
                            WHERE itemId=:i AND warehouseId=:w
                            """, {'i': search[0], 'w': search[1]})
        status = self.cursor.fetchone()
        if status is None:
            # jesli nie ma to stwórz i dodaj
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO StockStatus (itemId, warehouseId, quantity) VALUES (?,?,?)",
                    (search[0], search[1], quantity))
        else:
            # jesli jest to zaktualizuj stany
            with self.connection:
                self.cursor.execute(
                    "UPDATE StockStatus SET quantity=:q WHERE id=:i",
                    {'q': status[1]+quantity, 'i': status[0]})

    # usun przedmiot z magazynu
    def deleteItemFromWarehouse(self, item_name, warehouse_name, quantity):
        # sprawdz czy wskazane rzeczy istnieja
        self.cursor.execute("""
                            SELECT Item.id, Warehouse.id, OperationType.id
                            FROM Item, Warehouse, OperationType
                            WHERE Item.name=:in AND Warehouse.name=:wn AND OperationType.name = 'delete items'
                            """, {'in': item_name, 'wn': warehouse_name})
        search = self.cursor.fetchone()
        if search is None:
            return False

        # sprawdz czy przedmiot jest w wskazanym magazynie
        self.cursor.execute("""
                            SELECT id, quantity FROM StockStatus WHERE itemId=:i AND warehouseId=:w
                            """, {'i': search[0], 'w': search[1]})
        status = self.cursor.fetchone()
        if status is None:
            return False
        if quantity > status[1]:
            return False

        # usun przedmiot jestli podana ilosc nie jest większa od obecnego stanu
        with self.connection:
            self.cursor.execute(
                "UPDATE StockStatus SET quantity=:q WHERE id=:i",
                {'q': status[1]-quantity, 'i': status[0]})
            self.cursor.execute("""
                                INSERT INTO Operation (itemId, warehouseId, operationTypeId, quantity) VALUES (?,?,?,?)
                                """, (search[0], search[1], search[2], quantity))
        return True

    # przenies przedmioty pomiedzy magazynami
    def moveItems(self, item_name, from_warehouse, to_warehouse, quantity):
        # sprawdz czy wskazane magazyny istnieja
        self.cursor.execute("""
                            select id FROM Warehouse WHERE name=:from_warehouse OR name=:to_warehouse
                            """, {'from_warehouse': from_warehouse, 'to_warehouse': to_warehouse})
        search = self.cursor.fetchall()
        if search is None:
            return
        result = {'from_warehouse': search[0][0], 'to_warehouse': search[1][0]}
        # sprawdz czy przedmiot i typ operacji istnieje
        self.cursor.execute("""
                            SELECT Item.id, OperationType.id
                            FROM Item, OperationType
                            WHERE Item.name=:in AND OperationType.name = 'move items'
                            """, {'in': item_name})
        search = self.cursor.fetchone()
        if search is None:
            return
        result["item_id"] = search[0]
        result["operation_type"] = search[1]

        # sprawdz stan na magazynie z którego chcesz przeniesc
        self.cursor.execute("""
                            SELECT id, quantity 
                            FROM StockStatus 
                            WHERE itemId=:i AND warehouseId=:w
                            """, {'i': result["item_id"], 'w': result['from_warehouse']})

        # zakończ jeśli nie ma takiego przedmiotu w wskazanym magazynie
        if self.cursor.fetchone() is None:
            return

        # wykonaj operacje usuwania i sprawdz czy została wykonana poprawnie
        status = self.deleteItemFromWarehouse(
            item_name, from_warehouse, quantity)
        if status == False:
            return
        # wykonaj operacje dodania jeśli usuwanie zostało zakończone pomyślnie
        self.addItemToWarehouse(item_name, to_warehouse, quantity)


def main():
    inv = Operation()
    # inv.addItemToWarehouse('myszka Razer',  'w1', 15)
    # inv.addItemToWarehouse('myszka Razer',  'w2', 30)
    # inv.addItemToWarehouse('myszka Razer',  'w3', 55)
    # inv.deleteItemFromWarehouse('myszka Razer', 'w2', 20)
    # inv.moveItems('myszka Razer', 'w3', 'w1', 12)
    # inv.addItemToWarehouse('Słuchawki Genesis Argon 400',  'w2', 30)
    # inv.addItemToWarehouse('Pad Genesis PV65',  'w2', 15)
    # inv.addItemToWarehouse('Słuchawki Genesis Argon 400',  'w1', 100)
    # inv.addItemToWarehouse('Pad Genesis P65',  'w1', 8)
    # inv.addItemToWarehouse('Pad Genesis P65',  'w2', 14)
    # inv.addItemToWarehouse('Pad Genesis P65',  'w3', 33)


main()
