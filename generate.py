import os, re, json, sys

input_folder = 'input_cookies'
output_file = 'script.js'
cookie_pool = []

if os.path.exists(input_folder):
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Vẫn giữ Regex mới: Bắt mọi giá trị, đéo cần quan tâm nó bắt đầu bằng chữ gì
            n_match = re.search(r'NetflixId["\s=|\t]+([^\s"|;]{20,})', content, re.IGNORECASE)
            s_match = re.search(r'SecureNetflixId["\s=|\t]+([^\s"|;]{20,})', content, re.IGNORECASE)

            # ÉP BUỘC CÓ CẢ 2: Phục vụ riêng cho trình duyệt Web/iPhone
            if n_match and s_match:
                cookie_pool.append({
                    "n": n_match.group(1).strip(),
                    "s": s_match.group(1).strip()
                })

if not cookie_pool:
    print("Khong tim thay con cookie nao hop le!")
    sys.exit(1)

js_code = f"""
const pool = {json.dumps(cookie_pool)};
const pick = pool[Math.floor(Math.random() * pool.length)];

document.cookie = "NetflixId=" + pick.n + ";domain=.netflix.com;path=/;secure";
document.cookie = "SecureNetflixId=" + pick.s + ";domain=.netflix.com;path=/;secure";

console.log("Injected account. Total pool: {len(cookie_pool)}");
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_code)

print(f"Tao thanh cong script.js voi {len(cookie_pool)} cookie!")
