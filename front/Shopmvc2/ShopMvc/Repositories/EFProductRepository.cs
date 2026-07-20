using Microsoft.EntityFrameworkCore;
using ShopMvc.Models;


namespace ShopMvc.Repositories;

public class EFProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context;
    public EFProductRepository(ApplicationDbContext context) => _context = context;

    // Include Category để tránh N+1 query
    public async Task<IEnumerable<Product>> GetAllAsync() =>
        await _context.Products.Include(p => p.Category).ToListAsync();

    public async Task<Product?> GetByIdAsync(int id) =>
        await _context.Products
                               .Include(p => p.Category)
                               .Include(p => p.Images)   // load gallery ảnh cho Display
                               .FirstOrDefaultAsync(p => p.Id == id);

    public async Task AddAsync(Product product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
    }

    public async Task UpdateAsync(Product product)
    {
        _context.Products.Update(product);
        await _context.SaveChangesAsync();
    }

    public async Task DeleteAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product != null)
        {
            _context.Products.Remove(product);
            await _context.SaveChangesAsync();
        }
    }
}