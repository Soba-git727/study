using ShopMvc.Models;

namespace ShopMvc.Repositories;

public class MockCategoryRepository : ICategoryRepository
{
    private readonly List<Category> _categories = new()
    {
        new Category { Id = 1, Name = "Laptop" },
        new Category { Id = 2, Name = "Phụ kiện" }
    };

    public IEnumerable<Category> GetAllCategories() => _categories;
}