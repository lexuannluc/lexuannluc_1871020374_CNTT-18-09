using System;
using System.ComponentModel.DataAnnotations;

namespace OrderManagementApp.Models.ViewModels
{
    public class OrderCreateViewModel
    {
        [Required]
        [RegularExpression(@"^ORD-\d{8}-\d{4}$",
            ErrorMessage = "Order Number must be in format ORD-YYYYMMDD-XXXX")]
        public string OrderNumber { get; set; }

        [Required]
        [StringLength(100, MinimumLength = 2,
            ErrorMessage = "Customer Name must be between 2 and 100 characters")]
        public string CustomerName { get; set; }

        [Required]
        [EmailAddress(ErrorMessage = "Invalid email address")]
        public string CustomerEmail { get; set; }

        [Required]
        public int ProductId { get; set; }

        [Required]
        [Range(1, int.MaxValue, ErrorMessage = "Quantity must be greater than 0")]
        public int Quantity { get; set; }

        [Required]
        [DataType(DataType.Date)]
        public DateTime OrderDate { get; set; }

        [DataType(DataType.Date)]
        public DateTime? DeliveryDate { get; set; }
    }
}
