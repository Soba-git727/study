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

    // Danh sách sản phẩm
    public IActionResult Index() => View(_productRepository.GetAll());

    // Form thêm
    public IActionResult Add()
    {
        ViewBag.Categories = new SelectList(
            _categoryRepository.GetAllCategories(), "Id", "Name");
        return View();
    }

    [HttpPost]
    public IActionResult Add(Product product)
    {
        if (ModelState.IsValid)
        {
            _productRepository.Add(product);
            return RedirectToAction(nameof(Index));
        }
        ViewBag.Categories = new SelectList(
            _categoryRepository.GetAllCategories(), "Id", "Name");
        return View(product);
    }

    // Chi tiết
    public IActionResult Display(int id)
    {
        var product = _productRepository.GetById(id);
        return product == null ? NotFound() : View(product);
    }

    // Form sửa
    public IActionResult Update(int id)
    {
        var product = _productRepository.GetById(id);
        return product == null ? NotFound() : View(product);
    }

    [HttpPost]
    public IActionResult Update(Product product)
    {
        if (ModelState.IsValid)
        {
            _productRepository.Update(product);
            return RedirectToAction(nameof(Index));
        }
        return View(product);
    }

    // Xác nhận xóa
    public IActionResult Delete(int id)
    {
        var product = _productRepository.GetById(id);
        return product == null ? NotFound() : View(product);
    }

    [HttpPost, ActionName("DeleteConfirmed")]
    public IActionResult DeleteConfirmed(int id)
    {
        _productRepository.Delete(id);
        return RedirectToAction(nameof(Index));
    }
    [HttpPost]
    public async Task<IActionResult> Add(Product product, IFormFile? imageUrl)
    {
        if (ModelState.IsValid)
        {
            if (imageUrl != null && imageUrl.Length > 0)
                product.ImageUrl = await SaveImage(imageUrl);

            _productRepository.Add(product);
            return RedirectToAction(nameof(Index));
        }
        ViewBag.Categories = new SelectList(
            _categoryRepository.GetAllCategories(), "Id", "Name");
        return View(product);
    }

    private async Task<string> SaveImage(IFormFile image)
    {
        // tên file an toàn, tránh trùng
        var fileName = $"{Guid.NewGuid()}_{Path.GetFileName(image.FileName)}";
        var savePath = Path.Combine("wwwroot/images", fileName);

        using var stream = new FileStream(savePath, FileMode.Create);
        await image.CopyToAsync(stream);

        return "/images/" + fileName;   // đường dẫn tương đối để hiển thị
    }
}