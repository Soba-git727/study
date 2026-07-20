using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using ShopMvc.Models;
using ShopMvc.Repositories;

namespace ShopMvc.Controllers;

public class ProductController : Controller
{
    private readonly IProductRepository _productRepository;
    private readonly ICategoryRepository _categoryRepository;

    public ProductController(IProductRepository productRepository,
                            ICategoryRepository categoryRepository)
    {
        _productRepository = productRepository;
        _categoryRepository = categoryRepository;
    }

    public async Task<IActionResult> Index()
    {
        var products = await _productRepository.GetAllAsync();
        return View(products);
    }

    public async Task<IActionResult> Display(int id)
    {
        var product = await _productRepository.GetByIdAsync(id);
        if (product == null) return NotFound();
        return View(product);
    }

    // [GET] Form thêm sản phẩm
    public async Task<IActionResult> Add()
    {
        ViewBag.Categories = new SelectList(
            await _categoryRepository.GetAllAsync(), "Id", "Name");
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> Add(Product product, IFormFile? imageUrl)
    {
        if (ModelState.IsValid)
        {
            if (imageUrl != null && imageUrl.Length > 0)
                product.ImageUrl = await SaveImage(imageUrl);

            await _productRepository.AddAsync(product);
            return RedirectToAction(nameof(Index));
        }
        ViewBag.Categories = new SelectList(
            await _categoryRepository.GetAllAsync(), "Id", "Name");
        return View(product);
    }

    // [GET] Form sửa sản phẩm
    public async Task<IActionResult> Update(int id)
    {
        var product = await _productRepository.GetByIdAsync(id);
        if (product == null) return NotFound();
        ViewBag.Categories = new SelectList(
            await _categoryRepository.GetAllAsync(), "Id", "Name", product.CategoryId);
        return View(product);
    }

    [HttpPost]
    public async Task<IActionResult> Update(int id, Product product, IFormFile? imageUrl)
    {
        ModelState.Remove(nameof(Product.ImageUrl));  // Không validate trường ảnh
        if (id != product.Id) return NotFound();

        if (ModelState.IsValid)
        {
            var existing = await _productRepository.GetByIdAsync(id);
            if (existing == null) return NotFound();

            // Update dữ liệu
            existing.Name = product.Name;
            existing.Price = product.Price;
            existing.Description = product.Description;
            existing.CategoryId = product.CategoryId;

            // Nếu upload ảnh mới, lưu đường dẫn; nếu không thì giữ ảnh cũ
            if (imageUrl != null && imageUrl.Length > 0)
                existing.ImageUrl = await SaveImage(imageUrl);

            await _productRepository.UpdateAsync(existing);
            return RedirectToAction(nameof(Index));
        }

        ViewBag.Categories = new SelectList(
            await _categoryRepository.GetAllAsync(), "Id", "Name", product.CategoryId);
        return View(product);
    }

    private async Task<string> SaveImage(IFormFile image)
    {
        // Y như Bài 2: copy ảnh vào wwwroot/images/...
        var uploadsFolder = Path.Combine("wwwroot", "images");
        Directory.CreateDirectory(uploadsFolder);
        var fileName = Guid.NewGuid() + Path.GetExtension(image.FileName);
        var filePath = Path.Combine(uploadsFolder, fileName);
        using (var fileStream = new FileStream(filePath, FileMode.Create))
        {
            await image.CopyToAsync(fileStream);
        }
        return "/images/" + fileName;
    }
}