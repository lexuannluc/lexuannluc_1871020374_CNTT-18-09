using Microsoft.EntityFrameworkCore;
using OrderManagementApp.Models;

namespace OrderManagementApp.Data
{
    public class OrderDbContext : DbContext
    {
        public OrderDbContext(DbContextOptions<OrderDbContext> options)
            : base(options)
        {
        }

        public DbSet<Product> Products { get; set; }
        public DbSet<Order> Orders { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // ===== SEED PRODUCTS (CHỈ 1 LẦN) =====
            modelBuilder.Entity<Product>().HasData(
                new Product { Id = 1, Name = "Laptop Dell", Sku = "SKU001", Price = 1500, StockQuantity = 50, Category = "Electronics" },
                new Product { Id = 2, Name = "iPhone 15", Sku = "SKU002", Price = 1200, StockQuantity = 40, Category = "Electronics" },
                new Product { Id = 3, Name = "Samsung TV", Sku = "SKU003", Price = 900, StockQuantity = 30, Category = "Electronics" },
                new Product { Id = 4, Name = "Office Chair", Sku = "SKU004", Price = 200, StockQuantity = 100, Category = "Furniture" },
                new Product { Id = 5, Name = "Desk Lamp", Sku = "SKU005", Price = 50, StockQuantity = 200, Category = "Furniture" },
                new Product { Id = 6, Name = "Mechanical Keyboard", Sku = "SKU006", Price = 120, StockQuantity = 70, Category = "Accessories" },
                new Product { Id = 7, Name = "Gaming Mouse", Sku = "SKU007", Price = 80, StockQuantity = 90, Category = "Accessories" },
                new Product { Id = 8, Name = "Headphones", Sku = "SKU008", Price = 150, StockQuantity = 60, Category = "Accessories" },
                new Product { Id = 9, Name = "Power Bank", Sku = "SKU009", Price = 40, StockQuantity = 150, Category = "Accessories" },
                new Product { Id = 10, Name = "USB-C Cable", Sku = "SKU010", Price = 20, StockQuantity = 300, Category = "Accessories" }
            );

            // ===== SEED ORDERS =====
            modelBuilder.Entity<Order>().HasData(
                 new Order { Id = 1, OrderNumber = "ORD-20260101-0001", ProductId = 1, CustomerName = "John Doe", CustomerEmail = "john1@gmail.com", Quantity = 1, OrderDate = new DateTime(2026, 1, 1) },
        new Order { Id = 2, OrderNumber = "ORD-20260102-0002", ProductId = 2, CustomerName = "Anna Smith", CustomerEmail = "anna2@gmail.com", Quantity = 2, OrderDate = new DateTime(2026, 1, 2) },
        new Order { Id = 3, OrderNumber = "ORD-20260103-0003", ProductId = 3, CustomerName = "Peter Brown", CustomerEmail = "peter3@gmail.com", Quantity = 1, OrderDate = new DateTime(2026, 1, 3) },
        new Order { Id = 4, OrderNumber = "ORD-20260104-0004", ProductId = 4, CustomerName = "Lucy Green", CustomerEmail = "lucy4@gmail.com", Quantity = 4, OrderDate = new DateTime(2026, 1, 4) },
        new Order { Id = 5, OrderNumber = "ORD-20260105-0005", ProductId = 5, CustomerName = "Tom White", CustomerEmail = "tom5@gmail.com", Quantity = 3, OrderDate = new DateTime(2026, 1, 5) },

        new Order { Id = 6, OrderNumber = "ORD-20260106-0006", ProductId = 6, CustomerName = "Emma Black", CustomerEmail = "emma6@gmail.com", Quantity = 2, OrderDate = new DateTime(2026, 1, 6) },
        new Order { Id = 7, OrderNumber = "ORD-20260107-0007", ProductId = 7, CustomerName = "David Wilson", CustomerEmail = "david7@gmail.com", Quantity = 1, OrderDate = new DateTime(2026, 1, 7) },
        new Order { Id = 8, OrderNumber = "ORD-20260108-0008", ProductId = 8, CustomerName = "Sophia Lee", CustomerEmail = "sophia8@gmail.com", Quantity = 2, OrderDate = new DateTime(2026, 1, 8) },
        new Order { Id = 9, OrderNumber = "ORD-20260109-0009", ProductId = 9, CustomerName = "James King", CustomerEmail = "james9@gmail.com", Quantity = 5, OrderDate = new DateTime(2026, 1, 9) },
        new Order { Id = 10, OrderNumber = "ORD-20260110-0010", ProductId = 10, CustomerName = "Linda Scott", CustomerEmail = "linda10@gmail.com", Quantity = 6, OrderDate = new DateTime(2026, 1, 10) },

        new Order { Id = 11, OrderNumber = "ORD-20260111-0011", ProductId = 1, CustomerName = "Chris Evans", CustomerEmail = "chris11@gmail.com", Quantity = 1, OrderDate = new DateTime(2026, 1, 11) },
        new Order { Id = 12, OrderNumber = "ORD-20260112-0012", ProductId = 2, CustomerName = "Natalie Portman", CustomerEmail = "natalie12@gmail.com", Quantity = 1, OrderDate = new DateTime(2026, 1, 12) },
        new Order { Id = 13, OrderNumber = "ORD-20260113-0013", ProductId = 3, CustomerName = "Robert Downey", CustomerEmail = "robert13@gmail.com", Quantity = 2, OrderDate = new DateTime(2026, 1, 13) },
        new Order { Id = 14, OrderNumber = "ORD-20260114-0014", ProductId = 4, CustomerName = "Scarlett Johansson", CustomerEmail = "scarlett14@gmail.com", Quantity = 1, OrderDate = new DateTime(2026, 1, 14) },
        new Order { Id = 15, OrderNumber = "ORD-20260115-0015", ProductId = 5, CustomerName = "Mark Ruffalo", CustomerEmail = "mark15@gmail.com", Quantity = 2, OrderDate = new DateTime(2026, 1, 15) },

        new Order { Id = 16, OrderNumber = "ORD-20260116-0016", ProductId = 6, CustomerName = "Jeremy Renner", CustomerEmail = "jeremy16@gmail.com", Quantity = 3, OrderDate = new DateTime(2026, 1, 16) },
        new Order { Id = 17, OrderNumber = "ORD-20260117-0017", ProductId = 7, CustomerName = "Paul Rudd", CustomerEmail = "paul17@gmail.com", Quantity = 2, OrderDate = new DateTime(2026, 1, 17) },
        new Order { Id = 18, OrderNumber = "ORD-20260118-0018", ProductId = 8, CustomerName = "Brie Larson", CustomerEmail = "brie18@gmail.com", Quantity = 1, OrderDate = new DateTime(2026, 1, 18) },
        new Order { Id = 19, OrderNumber = "ORD-20260119-0019", ProductId = 9, CustomerName = "Benedict Cumberbatch", CustomerEmail = "ben19@gmail.com", Quantity = 4, OrderDate = new DateTime(2026, 1, 19) },
        new Order { Id = 20, OrderNumber = "ORD-20260120-0020", ProductId = 10, CustomerName = "Tom Holland", CustomerEmail = "tom20@gmail.com", Quantity = 2, OrderDate = new DateTime(2026, 1, 20) }
            );
        }
    }
}
