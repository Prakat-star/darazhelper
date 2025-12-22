from flask import Flask, render_template_string
from main import scrape_rated_products

app = Flask(__name__)

@app.route("/")
def home():
    products = scrape_rated_products()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daraz 4 or more⭐ Products</title>
        <style>
            :root {
                --bg: #f5f5f5;
                --card: #ffffff;
                --text: #000000;
                --accent: #ff6f00;
            }

            body.dark {
                --bg: #121212;
                --card: #1e1e1e;
                --text: #ffffff;
                --accent: #ff9800;
            }

            body {
                margin: 0;
                padding: 20px;
                font-family: Arial, sans-serif;
                background: var(--bg);
                color: var(--text);
                transition: 0.3s;
            }

            h1 {
                text-align: center;
            }

            .top-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 900px;
                margin: auto;
                gap: 10px;
            }

            input {
                flex: 1;
                padding: 8px;
                border-radius: 5px;
                border: none;
                outline: none;
            }

            button {
                padding: 8px 12px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                background: var(--accent);
                color: white;
            }

            .product-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }

            .product-card {
                background: var(--card);
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
                text-align: center;
            }

            .product-card img {
                width: 100%;
                height: 180px;
                object-fit: contain;
                margin-bottom: 10px;
            }

            /* 🔥 Scrollable title */
            .product-title {
                font-size: 14px;
                font-weight: bold;
                height: 40px;
                overflow-y: auto;
                scrollbar-width: thin;
                margin-bottom: 8px;
            }

            .price {
                color: var(--accent);
                font-weight: bold;
            }

            .rating {
                color: gold;
                margin: 5px 0;
            }

            a {
                display: inline-block;
                margin-top: 8px;
                padding: 6px 10px;
                background: var(--accent);
                color: white;
                border-radius: 4px;
                text-decoration: none;
                font-size: 13px;
            }
        </style>
    </head>
    <body>

        <h1>⭐ 4-Star or more Rated Products</h1>

        <div class="top-bar">
            <input type="text" id="search" placeholder="Search product..." onkeyup="searchProducts()">
            <button onclick="toggleDark()">🌙</button>
        </div>

        <div class="product-grid" id="productGrid">
            {% for p in products %}
                <div class="product-card" data-title="{{ p.title | lower }}">
                    <img src="{{ p.image_url }}">
                    <div class="product-title">{{ p.title }}</div>
                    <div class="price">{{ p.price }} {{ p.currency }}</div>
                    <div class="rating">⭐ {{ p.rating }} ({{ p.review_count }})</div>
                    <a href="{{ p.product_url }}" target="_blank">View</a>
                </div>
            {% endfor %}
        </div>

        <script>
            function toggleDark() {
                document.body.classList.toggle("dark");
            }

            function searchProducts() {
                let value = document.getElementById("search").value.toLowerCase();
                let cards = document.querySelectorAll(".product-card");

                cards.forEach(card => {
                    let title = card.dataset.title;
                    card.style.display = title.includes(value) ? "block" : "none";
                });
            }
        </script>

    </body>
    </html>
    """

    return render_template_string(html, products=products)


if __name__ == "__main__":
    app.run(debug=True)
