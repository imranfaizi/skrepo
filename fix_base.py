content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boutique Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { font-family: "Poppins", sans-serif; }
        body { background-color: #f0f2f5; margin: 0; padding: 0; }
        #sidebar { width: 260px; height: 100vh; background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); position: fixed; top: 0; left: 0; z-index: 100; display: flex; flex-direction: column; overflow: hidden; }
        #sidebar .sidebar-header { padding: 25px 20px; background: rgba(0,0,0,0.2); text-align: center; flex-shrink: 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        #sidebar .sidebar-header .shop-icon { width: 55px; height: 55px; background: linear-gradient(135deg, #e83e8c, #c2185b); border-radius: 15px; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px; font-size: 24px; color: white; box-shadow: 0 4px 15px rgba(232,62,140,0.4); }
        #sidebar .sidebar-header h4 { color: #fff; margin: 0; font-size: 16px; font-weight: 700; }
        #sidebar .sidebar-header p { color: #a0aec0; margin: 3px 0 0 0; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; }
        #sidebar .sidebar-nav { flex: 1; overflow-y: auto; padding: 10px 0 20px; }
        #sidebar .sidebar-nav::-webkit-scrollbar { width: 4px; }
        #sidebar .sidebar-nav::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }
        #sidebar ul.components { padding: 0; list-style: none; margin: 0; }
        #sidebar ul li a { padding: 11px 20px; display: flex; align-items: center; color: #a0aec0; text-decoration: none; font-size: 13.5px; transition: all 0.2s; margin: 2px 10px; border-radius: 8px; }
        #sidebar ul li a:hover { background: rgba(255,255,255,0.08); color: #fff; transform: translateX(3px); }
        #sidebar ul li a.active { background: linear-gradient(135deg, #e83e8c, #c2185b); color: #fff; box-shadow: 0 4px 12px rgba(232,62,140,0.35); font-weight: 500; }
        #sidebar ul li a i { margin-right: 10px; width: 18px; font-size: 15px; }
        .sidebar-label { padding: 12px 20px 4px; font-size: 10px; color: #4a5568; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
        #content { margin-left: 260px; min-height: 100vh; display: flex; flex-direction: column; }
        .top-navbar { background: #fff; border-bottom: 1px solid #e2e8f0; padding: 14px 25px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; position: sticky; top: 0; z-index: 99; }
        .top-navbar .page-heading { font-size: 18px; font-weight: 600; color: #1a202c; margin: 0; }
        .user-badge { background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 25px; padding: 6px 14px; font-size: 13px; color: #4a5568; font-weight: 500; }
        .page-content { padding: 25px; flex: 1; }
        .stat-card { border: none; border-radius: 16px; padding: 22px; color: white; box-shadow: 0 4px 20px rgba(0,0,0,0.12); transition: transform 0.2s; position: relative; overflow: hidden; height: 100%; }
        .stat-card:hover { transform: translateY(-3px); }
        .stat-card .card-icon { position: absolute; right: 15px; top: 15px; font-size: 45px; opacity: 0.15; }
        .stat-card .label { font-size: 12px; font-weight: 500; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
        .stat-card .value { font-size: 28px; font-weight: 700; margin: 0; line-height: 1.2; }
        .stat-card .sub { font-size: 12px; opacity: 0.75; margin-top: 6px; }
        .content-card { background: #fff; border: none; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); overflow: hidden; height: 100%; }
        .content-card .card-header-custom { padding: 16px 20px; border-bottom: 1px solid #f0f4f8; display: flex; align-items: center; justify-content: space-between; background: #fff; }
        .content-card .card-header-custom h6 { font-size: 15px; font-weight: 600; color: #1a202c; margin: 0; }
        .table thead th { background-color: #f7fafc; color: #4a5568; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #e2e8f0; padding: 13px 16px; }
        .table tbody td { padding: 13px 16px; font-size: 13.5px; color: #2d3748; vertical-align: middle; border-bottom: 1px solid #f0f4f8; }
        .table tbody tr:last-child td { border-bottom: none; }
        .table tbody tr:hover { background-color: #fafbfc; }
        .btn-primary-custom { background: linear-gradient(135deg, #e83e8c, #c2185b); border: none; color: white !important; padding: 9px 22px; border-radius: 8px; font-size: 13px; font-weight: 500; transition: all 0.2s; box-shadow: 0 3px 10px rgba(232,62,140,0.3); text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }
        .btn-primary-custom:hover { transform: translateY(-1px); box-shadow: 0 5px 15px rgba(232,62,140,0.4); color: white; }
        .alert { border: none; border-radius: 10px; font-size: 14px; }
        .main-footer { background: #fff; border-top: 2px solid #e83e8c; padding: 14px 25px; font-size: 13px; color: #4a5568; flex-shrink: 0; box-shadow: 0 -2px 10px rgba(0,0,0,0.05); }
        @media (max-width: 768px) { #sidebar { margin-left: -260px; } #sidebar.active { margin-left: 0; } #content { margin-left: 0; } }
    </style>
</head>
<body>
<nav id="sidebar">
    <div class="sidebar-header">
        <div class="shop-icon"><i class="bi bi-shop"></i></div>
        <h4>Boutique</h4>
        <p>Management System</p>
    </div>
    <div class="sidebar-nav">
        <ul class="components">
            <li><a href="{% url "dashboard" %}" class="{% if request.resolver_match.url_name == "dashboard" %}active{% endif %}"><i class="bi bi-speedometer2"></i> Dashboard</a></li>
            <div class="sidebar-label">Catalog</div>
            <li><a href="{% url "category_list" %}" class="{% if request.resolver_match.url_name == "category_list" %}active{% endif %}"><i class="bi bi-tags"></i> Categories</a></li>
            <li><a href="{% url "subcategory_list" %}" class="{% if request.resolver_match.url_name == "subcategory_list" %}active{% endif %}"><i class="bi bi-diagram-3"></i> Sub Categories</a></li>
            <li><a href="{% url "manufacturer_list" %}" class="{% if request.resolver_match.url_name == "manufacturer_list" %}active{% endif %}"><i class="bi bi-building"></i> Manufacturers</a></li>
            <div class="sidebar-label">Inventory</div>
            <li><a href="{% url "product_list" %}" class="{% if request.resolver_match.url_name == "product_list" %}active{% endif %}"><i class="bi bi-box-seam"></i> Products</a></li>
            <li><a href="{% url "supplier_list" %}" class="{% if request.resolver_match.url_name == "supplier_list" %}active{% endif %}"><i class="bi bi-person-lines-fill"></i> Suppliers</a></li>
            <li><a href="{% url "purchase_list" %}" class="{% if request.resolver_match.url_name == "purchase_list" %}active{% endif %}"><i class="bi bi-receipt"></i> Purchases</a></li>
            <div class="sidebar-label">Sales</div>
            <li><a href="{% url "sale_list" %}" class="{% if request.resolver_match.url_name == "sale_list" %}active{% endif %}"><i class="bi bi-cart3"></i> Sales</a></li>
            <li><a href="{% url "customer_list" %}" class="{% if request.resolver_match.url_name == "customer_list" %}active{% endif %}"><i class="bi bi-people"></i> Customers</a></li>
            <div class="sidebar-label">Stitching</div>
            <li><a href="{% url "stitching_list" %}" class="{% if request.resolver_match.url_name == "stitching_list" %}active{% endif %}"><i class="bi bi-scissors"></i> Stitching Orders</a></li>
            <div class="sidebar-label">Finance</div>
            <li><a href="{% url "expense_list" %}" class="{% if request.resolver_match.url_name == "expense_list" %}active{% endif %}"><i class="bi bi-cash-stack"></i> Expenses</a></li>
            <li><a href="{% url "reports_home" %}" class="{% if request.resolver_match.url_name == "reports_home" %}active{% endif %}"><i class="bi bi-bar-chart-line"></i> Reports</a></li>
        </ul>
    </div>
</nav>
<div id="content">
    <div class="top-navbar">
        <div class="d-flex align-items-center">
            <button id="sidebarCollapse" class="btn btn-sm btn-outline-secondary me-3 d-md-none"><i class="bi bi-list"></i></button>
            <h5 class="page-heading">{% block page_title %}Dashboard{% endblock %}</h5>
        </div>
        <div class="d-flex align-items-center gap-3">
            <div class="user-badge"><i class="bi bi-person-circle me-1"></i>{{ request.user.username }}</div>
            <a href="{% url "logout" %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-box-arrow-right"></i> Logout</a>
        </div>
    </div>
    <div class="page-content">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <footer class="main-footer">
        <div class="d-flex justify-content-between align-items-center">
            <div><i class="bi bi-shop me-1" style="color:#e83e8c;"></i><strong style="color:#1a202c;">Boutique</strong> Management System</div>
            <div>Developed by <strong style="color:#e83e8c;">Rabia Muneeb</strong></div>
            <div style="color:#a0aec0;">&copy; 2026 All Rights Reserved</div>
        </div>
    </footer>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const sidebarBtn = document.getElementById("sidebarCollapse");
    if(sidebarBtn) { sidebarBtn.addEventListener("click", function() { document.getElementById("sidebar").classList.toggle("active"); }); }
</script>
{% block extra_js %}{% endblock %}
</body>
</html>'''

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('base.html fixed!')