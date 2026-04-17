FILE = r"C:\home\jeon\api-health-monitor\frontend\app\page.tsx"

with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

# onMouseEnter/onMouseLeave 제거하고 CSS hover로 대체
old_link = """                    <Link href={href} style={{ fontSize: '13px', color: '#475569', textDecoration: 'none', transition: 'color 0.2s' }}
                      onMouseEnter={e => (e.currentTarget.style.color = '#00e5b4')}
                      onMouseLeave={e => (e.currentTarget.style.color = '#475569')}>
                      {label}
                    </Link>"""

new_link = """                    <Link href={href} className="footer-link">
                      {label}
                    </Link>"""

c = c.replace(old_link, new_link)

# style 태그에 footer-link 클래스 추가
old_style_end = "        .bar-chart-bar { border-radius: 3px 3px 0 0; transition: all 0.3s; }"
new_style_end = """        .bar-chart-bar { border-radius: 3px 3px 0 0; transition: all 0.3s; }
        .footer-link { font-size: 13px; color: #475569; text-decoration: none; transition: color 0.2s; }
        .footer-link:hover { color: #00e5b4; }"""

c = c.replace(old_style_end, new_style_end)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done!", "onMouseEnter" not in c)
