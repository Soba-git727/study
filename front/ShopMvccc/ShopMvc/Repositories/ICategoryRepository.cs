using ShopMvc.Models;

namespace ShopMvc.Repositories;

public interface ICategoryRepository
{
    IEnumerable<Category> GetAllCategories();
}