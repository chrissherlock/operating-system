#!/usr/bin/env python3
import os
import urllib.request
import hashlib
import re

def main():
    # 1. Create assets directory and download image
    asset_dir = "week09-memory-management/assets"
    os.makedirs(asset_dir, exist_ok=True)

    img_filename = "peter-denning.jpg"
    img_path = os.path.join(asset_dir, img_filename)

    wiki_filename = "Peter_J._Denning.jpg"
    digest = hashlib.md5(wiki_filename.encode('utf-8')).hexdigest()
    img_url = f"https://upload.wikimedia.org/wikipedia/commons/{digest[0]}/{digest[0]}{digest[1]}/{wiki_filename}"

    print("Downloading Peter Denning image from Wikimedia Commons...")
    try:
        req = urllib.request.Request(img_url, headers={"User-Agent": "COSC240-Student-Project/1.0"})
        with urllib.request.urlopen(req) as response, open(img_path, "wb") as out_file:
            out_file.write(response.read())
        print(f"Successfully downloaded image to {img_path}")
    except Exception as e:
        print(f"Warning: Download failed ({e}). Ensure 'peter-denning.jpg' is placed in '{asset_dir}' manually if offline.")

    # 2. Update 09-working-set.html sidebar and styling
    target_html = "week09-memory-management/09-working-set.html"
    if os.path.exists(target_html):
        with open(target_html, "r", encoding="utf-8") as f:
            content = f.read()

        # Inject sidebar image & photo credit CSS rules if not present
        img_css = """
    .bio-sidebar img {
      width: 100%;
      height: auto;
      border-radius: 4px;
      margin-bottom: 6px;
      border: 1px solid var(--border);
    }
    .photo-credit {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-style: italic;
      margin-bottom: 8px;
    }"""
        if ".bio-sidebar img" not in content:
            content = content.replace("</style>", f"{img_css}\n  </style>")

        # New sidebar markup with the image and attribution
        new_sidebar = """        <aside class="bio-sidebar">
          <h3>Pioneer Profile</h3>
          <img src="assets/peter-denning.jpg" alt="Dr. Peter J. Denning">
          <div class="photo-credit">Photo by Louis Fabian Bachrach</div>
          <p><strong>Dr. Peter J. Denning</strong> (often referenced as Peter Jenning in informal notes) is an American computer scientist renowned for his foundational work on virtual memory.</p>
          <p>In 1968, while at MIT, he formulated the <strong>Working Set Model</strong> and program locality principles. Read more on his <a href="https://en.wikipedia.org/wiki/Peter_J._Denning" target="_blank">Wikipedia page</a>.</p>
        </aside>"""

        # Replace existing bio-sidebar block
        content = re.sub(r'<aside class="bio-sidebar">.*?</aside>', new_sidebar, content, flags=re.DOTALL)

        with open(target_html, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully updated {target_html} with floating sidebar, image, and photo credit.")
    else:
        print(f"Error: {target_html} not found.")

if __name__ == "__main__":
    main()
