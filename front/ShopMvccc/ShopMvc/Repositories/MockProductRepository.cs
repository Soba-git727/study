using ShopMvc.Models;

namespace ShopMvc.Repositories;

public class MockProductRepository : IProductRepository
{
    private readonly List<Product> _products = new()
    {
        new Product
        {
            Id = 1,
            Name = "Laptop Dell XPS",
            Price = 28990000,
            Description = "Ultrabook 13.4 inch",
            CategoryId = 1,
            ImageUrl = "/images/laptop.jpg" // Thêm đường dẫn ảnh mẫu cho Laptop
        },
        new Product
        {
            Id = 2,
            Name = "Chuột Logitech MX",
            Price = 1890000,
            Description = "Chuột không dây",
            CategoryId = 2,
            ImageUrl = "/images/mouse.jpg" // Thêm đường dẫn ảnh mẫu cho Chuột
        }
    };

    public IEnumerable<Product> GetAll() => _products;
    public Product? GetById(int id) => _products.FirstOrDefault(p => p.Id == id);

    public void Add(Product product)
    {
        product.Id = _products.Count == 0 ? 1 : _products.Max(p => p.Id) + 1;
        _products.Add(product);
    }

    public void Update(Product product)
    {
        var i = _products.FindIndex(p => p.Id == product.Id);
        if (i != -1) _products[i] = product;
    }

    public void Delete(int id)
    {
        var p = _products.FirstOrDefault(x => x.Id == id);
        if (p != null) _products.Remove(p);
    }
}