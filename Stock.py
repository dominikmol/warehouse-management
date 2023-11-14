from Database import DataBase


class StorageStock (DataBase):
    def showStocks(self):
        self.cursor.execute("""
                            SELECT Warehouse.name as warehouseName, item.name as itemName, StockStatus.quantity 
                            FROM StockStatus
                            INNER JOIN Warehouse on Warehouse.id = StockStatus.warehouseId
                            INNER JOIN item on item.id = StockStatus.itemId
                            ORDER BY warehouseName;
                            """)
        search = self.cursor.fetchall()

        if search is None:
            return

        # tworzenie listy unikalnych magazyow z wyszukania
        warehouse_list = []
        for stock in search:
            if stock[0] in warehouse_list:
                continue
            warehouse_list.append(stock[0])

        # wyswietania stanu magazyow
        for warehouse in warehouse_list:
            print(f"warehouse: {warehouse}")
            for stock in search:
                print(f"\t{stock[1]} - {stock[2]}")


def main():
    inv = StorageStock()
    inv.showStocks()


main()


#  sqlite> SELECT item.name as itemName, StockStatus.quantity, Warehouse.name as warehouseName
#     ...> FROM StockStatus
#     ...> INNER JOIN item on item.id = StockStatus.itemId
#     ...> INNER JOIN Warehouse on Warehouse.id = StockStatus.warehouseId
#     ...> ORDER BY warehouse;
