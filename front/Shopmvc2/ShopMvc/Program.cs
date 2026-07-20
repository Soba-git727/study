using Microsoft.EntityFrameworkCore;
using ShopMvc.Models;
using ShopMvc.Repositories;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();

// EF Core + SQL Server 2022
builder.Services.AddDbContext<ShopMvc.Models.ApplicationDbContext>(options =>
    options.UseSqlServer(
        "Server=(localdb)\\ProjectModels;Database=ShopMvcDb;Trusted_Connection=True;TrustServerCertificate=True"));

// Repository (thay Mock bằng EF)
builder.Services.AddScoped<IProductRepository, EFProductRepository>();
builder.Services.AddScoped<ICategoryRepository, EFCategoryRepository>();

var app = builder.Build();

// Middleware giữ nguyên từ Bài 2
if (!app.Environment.IsDevelopment())
    app.UseExceptionHandler("/Home/Error");

app.UseHttpsRedirection();
app.UseStaticFiles();   // QUAN TRỌNG: cần để upload ảnh hoạt động
app.UseRouting();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
