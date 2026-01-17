using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OrderManagementApp.Data;
using OrderManagementApp.Models;
using OrderManagementApp.Models.ViewModels;

namespace OrderManagementApp.Controllers
{
    public class OrdersController : Controller
    {
        private readonly OrderDbContext _context;

        public OrdersController(OrderDbContext context)
        {
            _context = context;
        }

        // ================= CREATE (GET) =================
        public IActionResult Create()
        {
            ViewBag.Products = _context.Products.ToList();
            return View();
        }

        // ================= CREATE (POST) =================
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(OrderCreateViewModel model)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.Products = _context.Products.ToList();
                return View(model);
            }

            var product = _context.Products.FirstOrDefault(p => p.Id == model.ProductId);
            if (product == null)
            {
                ModelState.AddModelError("ProductId", "Product does not exist");
                ViewBag.Products = _context.Products.ToList();
                return View(model);
            }

            if (model.Quantity > product.StockQuantity)
            {
                ModelState.AddModelError("Quantity", "Quantity exceeds available stock");
                ViewBag.Products = _context.Products.ToList();
                return View(model);
            }

            if (model.OrderDate.Date > DateTime.Today)
            {
                ModelState.AddModelError("OrderDate", "Order Date cannot be in the future");
                ViewBag.Products = _context.Products.ToList();
                return View(model);
            }

            if (model.DeliveryDate != null && model.DeliveryDate < model.OrderDate)
            {
                ModelState.AddModelError("DeliveryDate", "Delivery Date must be after Order Date");
                ViewBag.Products = _context.Products.ToList();
                return View(model);
            }

            var order = new Order
            {
                OrderNumber = model.OrderNumber,
                CustomerName = model.CustomerName,
                CustomerEmail = model.CustomerEmail,
                ProductId = model.ProductId,
                Quantity = model.Quantity,
                OrderDate = model.OrderDate,
                DeliveryDate = model.DeliveryDate
            };

            _context.Orders.Add(order);
            _context.SaveChanges();

            return RedirectToAction(nameof(Index));
        }

        // ================= LIST =================
        public IActionResult Index()
        {
            var orders = _context.Orders
                .Include(o => o.Product)
                .OrderByDescending(o => o.OrderDate)
                .ToList();

            return View(orders);
        }
    }
}
