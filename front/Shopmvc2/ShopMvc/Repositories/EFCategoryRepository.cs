using Microsoft.EntityFrameworkCore;
using ShopMvc.Models;
using ShopMvc.Models;

namespace ShopMvc.Repositories;

public class EFCategoryRepository : ICategoryRepository
{
    private readonly ApplicationDbContext _context;
    public EFCategoryRepository(ApplicationDbContext context) => _context = context;

    public async Task<IEnumerable<Category>> GetAllAsync() =>
        await _context.Categories.ToListAsync();

    public async Task<Category?> GetByIdAsync(int id) =>
        await _context.Categories.FirstOrDefaultAsync(c => c.Id == id);

    public async Task AddAsync(Category category)
    {
        _context.Categories.Add(category);
        await _context.SaveChangesAsync();
    }

    public async Task UpdateAsync(Category category)
    {
        _context.Categories.Update(category);
        await _context.SaveChangesAsync();
    }

    public async Task DeleteAsync(int id)
    {
        var cat = await _context.Categories.FindAsync(id);
        if (cat != null)
        {
            _context.Categories.Remove(cat);
            await _context.SaveChangesAsync();
        }
    }
}