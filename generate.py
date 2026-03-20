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

            # REGEX MỚI: Bắt mọi giá trị, đéo cần quan tâm nó bắt đầu bằng chữ gì
            n_match = re.search(r'NetflixId["\s=|\t]+([^\s"|;]{20,})', content, re.IGNORECASE)
            s_match = re.search(r'SecureNetflixId["\s=|\t]+([^\s"|;]{20,})', content, re.IGNORECASE)

            # CHỈ CẦN CÓ NETFLIX ID LÀ BẾ VÀO LUÔN (Nếu Secure thiếu thì để rỗng)
            if n_match:
                cookie_pool.append({
                    "n": n_match.group(1).strip(),
                    "s": s_match.group(1).strip() if s_match else ""
                })

if not cookie_pool:
    print("❌ Đéo tìm thấy con cookie nào hợp lệ!")
    sys.exit(1)

js_code = f"""
const pool = {json.dumps(cookie_pool)};
const pick = pool[Math.floor(Math.random() * pool.length)];

document.cookie = "NetflixId=" + pick.n + ";domain=.netflix.com;path=/;secure";
if (pick.s !== "") {{
    document.cookie = "SecureNetflixId=" + pick.s + ";domain=.netflix.com;path=/;secure";
}}

console.log("✅ Injected account. Total pool: {len(cookie_pool)}");
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_code)

print(f"🔥 Tạo thành công script.js với {len(cookie_pool)} cookie!")
