base = open('templates/base.html', 'r', encoding='utf-8').read()

# Fix sidebar font readability and footer
old_sidebar = '''        #sidebar ul li a { padding: 11px 20px; display: flex; align-items: center; color: #a0aec0; text-decoration: none; font-size: 13.5px; transition: all 0.2s; margin: 2px 10px; border-radius: 8px; }'''
new_sidebar = '''        #sidebar ul li a { padding: 11px 20px; display: flex; align-items: center; color: #cbd5e0; text-decoration: none; font-size: 14px; font-weight: 500; transition: all 0.2s; margin: 2px 10px; border-radius: 8px; }'''

old_label = '''        .sidebar-label { padding: 12px 20px 4px; font-size: 10px; color: #4a5568; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }'''
new_label = '''        .sidebar-label { padding: 12px 20px 4px; font-size: 10px; color: #718096; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700; }'''

old_footer = '''        .main-footer { background: #fff; border-top: 2px solid #e83e8c; padding: 14px 25px; font-size: 13px; color: #4a5568; flex-shrink: 0; box-shadow: 0 -2px 10px rgba(0,0,0,0.05); }'''
new_footer = '''        .main-footer { background: linear-gradient(135deg, #1a1a2e, #16213e); border-top: 3px solid #e83e8c; padding: 16px 25px; font-size: 13px; color: #a0aec0; flex-shrink: 0; box-shadow: 0 -4px 15px rgba(0,0,0,0.1); }'''

base = base.replace(old_sidebar, new_sidebar)
base = base.replace(old_label, new_label)
base = base.replace(old_footer, new_footer)

# Fix footer content
old_footer_content = '''    <footer class="main-footer">
        <div class="d-flex justify-content-between align-items-center">
            <div><i class="bi bi-shop me-1" style="color:#e83e8c;"></i><strong style="color:#1a202c;">Boutique</strong> Management System</div>
            <div>Developed by <strong style="color:#e83e8c;">Rabia Muneeb</strong></div>
            <div style="color:#a0aec0;">&copy; 2026 All Rights Reserved</div>
        </div>
    </footer>'''

new_footer_content = '''    <footer class="main-footer">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <i class="bi bi-shop me-1" style="color:#e83e8c;"></i>
                <strong style="color:#fff;">Boutique</strong>
                <span style="color:#718096;"> Management System</span>
            </div>
            <div style="color:#fff;">
                Developed by <strong style="color:#e83e8c;">Rabia Muneeb</strong>
            </div>
            <div>
                <i class="bi bi-c-circle me-1" style="color:#e83e8c;"></i>
                <span style="color:#718096;">2026 All Rights Reserved</span>
            </div>
        </div>
    </footer>'''

base = base.replace(old_footer_content, new_footer_content)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base)
print('base.html updated!')

# Now fix dashboard template
dashboard = '''{% extends 'base.html' %}
{% block page_title %}Dashboard{% endblock %}
{% block content %}

<div class="row g-3 mb-4">
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #e83e8c, #c2185b);">
            <i class="bi bi-cart3 card-icon"></i>
            <div class="label">Today Sales</div>
            <div class="value">Rs. {{ today_revenue|floatformat:0 }}</div>
            <div class="sub">{{ today_orders }} Orders Today</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #2ecc71, #27ae60);">
            <i class="bi bi-graph-up card-icon"></i>
            <div class="label">Last 30 Days</div>
            <div class="value">Rs. {{ last30_revenue|floatformat:0 }}</div>
            <div class="sub">{{ last30_orders }} Orders</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #3498db, #2980b9);">
            <i class="bi bi-receipt card-icon"></i>
            <div class="label">This Month Purchases</div>
            <div class="value">Rs. {{ monthly_purchase_total|floatformat:0 }}</div>
            <div class="sub">{{ monthly_purchase_count }} Invoices</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #e74c3c, #c0392b);">
            <i class="bi bi-exclamation-triangle card-icon"></i>
            <div class="label">Stock Alerts</div>
            <div class="value">{{ low_stock }}</div>
            <div class="sub">Low Stock Items</div>
        </div>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #9b59b6, #8e44ad);">
            <i class="bi bi-scissors card-icon"></i>
            <div class="label">Stitching Orders</div>
            <div class="value">{{ pending_stitching }}</div>
            <div class="sub">Pending Orders</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #f39c12, #e67e22);">
            <i class="bi bi-cash-stack card-icon"></i>
            <div class="label">Today Expenses</div>
            <div class="value">Rs. {{ today_expense_total|floatformat:0 }}</div>
            <div class="sub">Total Spent Today</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #1abc9c, #16a085);">
            <i class="bi bi-box-seam card-icon"></i>
            <div class="label">Total Products</div>
            <div class="value">{{ total_products }}</div>
            <div class="sub">Active Products</div>
        </div>
    </div>
    <div class="col-xl-3 col-md-6">
        <div class="stat-card" style="background: linear-gradient(135deg, #34495e, #2c3e50);">
            <i class="bi bi-people card-icon"></i>
            <div class="label">Total Customers</div>
            <div class="value">{{ total_customers }}</div>
            <div class="sub">Registered</div>
        </div>
    </div>
</div>

<div class="row g-3 mb-4">
    <div class="col-lg-8">
        <div class="content-card">
            <div class="card-header-custom">
                <h6><i class="bi bi-bar-chart me-2 text-primary"></i>Last 30 Days Sales</h6>
                <span class="badge bg-primary">Monthly Overview</span>
            </div>
            <div class="p-3">
                <canvas id="salesChart" height="110"></canvas>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="content-card">
            <div class="card-header-custom">
                <h6><i class="bi bi-pie-chart me-2 text-danger"></i>Stitching Status</h6>
            </div>
            <div class="p-3">
                <canvas id="stitchingChart" height="220"></canvas>
            </div>
        </div>
    </div>
</div>

<div class="row g-3">
    <div class="col-lg-6">
        <div class="content-card">
            <div class="card-header-custom">
                <h6><i class="bi bi-clock-history me-2 text-success"></i>Recent Sales</h6>
                <span class="badge bg-success">Latest 5</span>
            </div>
            <table class="table table-hover mb-0">
                <thead>
                    <tr><th>Invoice</th><th>Customer</th><th>Amount</th><th>Date</th></tr>
                </thead>
                <tbody>
                    {% for sale in recent_sales %}
                    <tr>
                        <td><strong>{{ sale.invoice_number }}</strong></td>
                        <td>{{ sale.customer.name|default:"Walk-in" }}</td>
                        <td><span class="text-success fw-bold">Rs. {{ sale.net_total|floatformat:0 }}</span></td>
                        <td>{{ sale.sale_date|date:"d M" }}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="4" class="text-center text-muted py-4">
                        <i class="bi bi-inbox fs-4 d-block mb-2"></i>No sales yet
                    </td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    <div class="col-lg-6">
        <div class="content-card">
            <div class="card-header-custom">
                <h6><i class="bi bi-exclamation-triangle me-2 text-warning"></i>Low Stock Alerts</h6>
                <span class="badge bg-warning text-dark">{{ low_stock }} Items</span>
            </div>
            <table class="table table-hover mb-0">
                <thead>
                    <tr><th>Product</th><th>Stock</th><th>Alert Level</th></tr>
                </thead>
                <tbody>
                    {% for product in low_stock_products %}
                    <tr>
                        <td><strong>{{ product.name }}</strong></td>
                        <td><span class="badge bg-danger">{{ product.stock }}</span></td>
                        <td>{{ product.stock_alert }}</td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="3" class="text-center text-muted py-4">
                        <i class="bi bi-check-circle fs-4 d-block mb-2 text-success"></i>All stock levels fine
                    </td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<script>
const chartLabels = {{ chart_labels|safe }};
const chartData = {{ chart_data|safe }};

const salesCtx = document.getElementById('salesChart').getContext('2d');
new Chart(salesCtx, {
    type: 'bar',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Sales (Rs.)',
            data: chartData,
            backgroundColor: 'rgba(232, 62, 140, 0.8)',
            borderColor: '#e83e8c',
            borderWidth: 1,
            borderRadius: 6,
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.06)' },
                ticks: { callback: function(value) { return 'Rs. ' + value.toLocaleString(); } }
            },
            x: { grid: { display: false } }
        }
    }
});

const stitchCtx = document.getElementById('stitchingChart').getContext('2d');
new Chart(stitchCtx, {
    type: 'doughnut',
    data: {
        labels: ['Pending', 'In Progress', 'Completed'],
        datasets: [{
            data: [{{ stitching_pending }}, {{ stitching_progress }}, {{ stitching_completed }}],
            backgroundColor: ['#f39c12', '#3498db', '#2ecc71'],
            borderWidth: 0,
            hoverOffset: 8,
        }]
    },
    options: {
        responsive: true,
        cutout: '70%',
        plugins: { legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true } } }
    }
});
</script>
{% endblock %}'''

with open('templates/dashboard/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard)
print('Dashboard template updated!')