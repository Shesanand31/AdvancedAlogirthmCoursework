import time

# ===============================
# Step 1: Hash Table (Separate Chaining)
# ===============================
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # each bucket is a list

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value  # update if exists
                return
        self.table[index].append([key, value])  # add new

    def search(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                self.table[index].remove(pair)
                return True
        return False

    def display(self):
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"Bucket {i}: {bucket}")


# ===============================
# Step 2: Product Entity Class
# ===============================
class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"{self.product_id} | {self.name} | RM{self.price:.2f} | Qty: {self.quantity}"


# ===============================
# Step 3: CLI Inventory System
# ===============================
def inventory_system():
    ht = HashTable(size=1000)  # larger table for many products
    products = []

    # Predefined baby products
    predefined = [
        Product("P001", "Baby Bottle", 15.90, 50),
        Product("P002", "Diaper Pack", 35.00, 100),
        Product("P003", "Baby Wipes", 12.50, 200),
        Product("P004", "Baby Lotion", 18.90, 75),
        Product("P005", "Baby Shampoo", 20.00, 60),
    ]
    for p in predefined:
        ht.insert(p.product_id, p)
        products.append(p)

    # Generate many products for realistic performance test
    for i in range(10000):
        pid = f"P{i+100:05d}"
        prod = Product(pid, f"Product{i}", i * 0.5, i % 100)
        ht.insert(pid, prod)
        products.append(prod)

    while True:
        print("\n--- Baby Shop Inventory System ---")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Delete Product")
        print("4. Display All Products")
        print("5. Performance Comparison (HashTable vs Array)")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            pid = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            price = float(input("Enter Price (RM): "))
            qty = int(input("Enter Quantity: "))
            prod = Product(pid, name, price, qty)
            ht.insert(pid, prod)
            products.append(prod)
            print("Product inserted!")

        elif choice == "2":
            pid = input("Enter Product ID to search: ")
            product = ht.search(pid)
            print(product if product else "Product not found.")

        elif choice == "3":
            pid = input("Enter Product ID to delete: ")
            if ht.delete(pid):
                print("Product deleted.")
                products = [p for p in products if p.product_id != pid]
            else:
                print("Product not found.")

        elif choice == "4":
            print("\n=== Current Inventory in Hash Table ===")
            ht.display()

        elif choice == "5":
            search_key = "P00500"  # pick a middle product for fairness
            iterations = 10000     # repeat searches

            # Hash Table search timing
            start = time.perf_counter()
            for _ in range(iterations):
                ht.search(search_key)
            end = time.perf_counter()
            hash_time = (end - start) / iterations

            # Array search timing
            start = time.perf_counter()
            for _ in range(iterations):
                found = None
                for p in products:
                    if p.product_id == search_key:
                        found = p
                        break
            end = time.perf_counter()
            array_time = (end - start) / iterations

            print("\n=== Performance Comparison ===")
            print(f"Hash Table Avg Search Time: {hash_time:.10f} seconds")
            print(f"Array Avg Search Time:      {array_time:.10f} seconds")

            if hash_time < array_time:
                print("Hash Table is faster on average (O(1) lookup).")
            else:
                print("Array search is slower (O(n) lookup).")

        elif choice == "6":
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


# ===============================
# Run Inventory System
# ===============================
if __name__ == "__main__":
    inventory_system()
