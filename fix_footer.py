with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        .main-footer { background: linear-gradient(135deg, #1a1a2e, #16213e); border-top: 3px solid #e83e8c; padding: 16px 25px; font-size: 13px; color: #a0aec0; flex-shrink: 0; box-shadow: 0 -4px 15px rgba(0,0,0,0.1); }'''

new = '''        .main-footer { background: linear-gradient(135deg, #1a1a2e, #16213e); border-top: 3px solid #e83e8c; padding: 18px 25px; font-size: 13px; color: #a0aec0; flex-shrink: 0; box-shadow: 0 -4px 15px rgba(0,0,0,0.1); }
        .main-footer .dev-name { color: #ffffff; font-size: 17px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; }'''

content = content.replace(old, new)

old_footer = '''            <div style="text-align:center;">
                <span style="color:#718096; font-size:12px;">Developed & Designed by</span><br>
                <strong style="color:#e83e8c; font-size:16px; letter-spacing:1px;">
                    <i class="bi bi-stars me-1"></i>Rabia Muneeb<i class="bi bi-stars ms-1"></i>
                </strong>
            </div>'''

new_footer = '''            <div style="text-align:center;">
                <span style="color:#718096; font-size:12px;">Developed & Designed by</span><br>
                <span class="dev-name">
                    ✦ Rabia Muneeb ✦
                </span>
            </div>'''

content = content.replace(old_footer, new_footer)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Footer updated!')