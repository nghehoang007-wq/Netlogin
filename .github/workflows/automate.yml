name: Manual Convert Cookie

on:
  push:
    paths:
      - 'input_cookies/**'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Python Converter
        shell: python
        run: |
          import os, re, json
          
          input_folder = 'input_cookies'
          output_file = 'script.js'
          cookie_pool = []
          
          if os.path.exists(input_folder):
              for filename in os.listdir(input_folder):
                  filepath = os.path.join(input_folder, filename)
                  if os.path.isfile(filepath):
                      with open(filepath, 'r', encoding='utf-8') as f:
                          content = f.read()
                          # Regex siêu cấp: Chỉ lấy mã nếu dài trên 20 ký tự (tránh lấy nhầm dấu phẩy)
                          n_match = re.search(r'NetflixId["\s=|\t]+((?:ct|v%3D)[^\s"|;]{20,})', content)
                          s_match = re.search(r'SecureNetflixId["\s=|\t]+(v%3D3%26mac%3D[^\s"|;]{20,})', content)
                          
                          if n_match and s_match:
                              cookie_pool.append({"n": n_match.group(1).strip(), "s": s_match.group(1).strip()})
          
          if not cookie_pool:
              print("❌ Khong tim thay acc hop le!")
              exit(1)

          # JS Payload Integration with safe brace escapes for YAML blocks
          js_code = f"""
          const pool = {json.dumps(cookie_pool)};
          const pick = pool[Math.floor(Math.random() * pool.length)];
          document.cookie = "NetflixId=" + pick.n + ";domain=.netflix.com;path=/;secure";
          document.cookie = "SecureNetflixId=" + pick.s + ";domain=.netflix.com;path=/;secure";
          
          alert("Nạp acc thành công! Kho đang có: {len(cookie_pool)} acc.");
          
          if (typeof completion === "function") {{
              completion();
          }}
          
          window.location.reload();
          """
          with open(output_file, 'w', encoding='utf-8') as f:
              f.write(js_code)
          print(f"✅ Da xu ly xong {len(cookie_pool)} acc.")

      - name: Push Result
        run: |
          git config --global user.name "Netflix-Bot"
          git config --global user.email "bot@github.com"
          git add script.js
          git commit -m "🚀 Auto Update [$(date)]" || exit 0
          git push
