using System.ComponentModel.DataAnnotations;
namespace ShopMvc.Models;

public class Product
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Vui lòng nhập tên sản phẩm")]
    [StringLength(100)]
    public string Name { get; set; } = string.Empty;

    [Range(0.01, 100000000000.00, ErrorMessage = "Giá phải lớn hơn 0")]
    public decimal Price { get; set; }

    public string? Description { get; set; }

    public int CategoryId { get; set; }
    public string? ImageUrl { get; set; }            // ảnh đại diện
    public List<string>? ImageUrls { get; set; }     // các ảnh khác
}
    
