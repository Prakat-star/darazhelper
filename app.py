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
        <title>Daraz 4⭐+ Products</title>
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
                background: var(--bg);
                color: var(--text);
                font-family: Arial, sans-serif;
                padding: 20px;
                transition: 0.3s;
            }

            h1 {
                text-align: center;
            }

            .top-bar {
                max-width: 900px;
                margin: auto;
                display: flex;
                gap: 10px;
            }

            input {
                flex: 1;
                padding: 8px;
                border-radius: 5px;
                border: none;
            }

            button {
                padding: 8px 12px;
                border-radius: 5px;
                border: none;
                background: var(--accent);
                color: white;
                cursor: pointer;
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
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            }

            /* PRICE STATUS */
            .product-card.down {
                border: 2px solid #2ecc71;
                background: #eafaf1;
            }

            .product-card.up {
                border: 2px solid #e74c3c;
                background: #fdecea;
            }

            body.dark .product-card.down {
                background: #123d2a;
            }

            body.dark .product-card.up {
                background: #3d1c1c;
            }

            img {
                width: 100%;
                height: 180px;
                object-fit: contain;
            }

            .product-title {
                font-size: 14px;
                font-weight: bold;
                height: 40px;
                overflow-y: auto;
                margin: 8px 0;
            }

            .price {
                font-weight: bold;
                color: var(--accent);
            }

            .rating {
                color: gold;
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

        <h1>⭐ 4-Star or Higher Products</h1>

        <div class="top-bar">
            <input id="search" placeholder="Search..." onkeyup="searchProducts()">
            <button onclick="toggleDark()">🌙</button>
        </div>

        <div class="product-grid">
            {% for p in products %}
            <div class="product-card {{ p.price_status }}" data-title="{{ p.title | lower }}">
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
                document.querySelectorAll(".product-card").forEach(card => {
                    card.style.display = card.dataset.title.includes(value) ? "block" : "none";
                });
            }
        </script>

    </body>
    </html>
    """

    return render_template_string(html, products=products)


if __name__ == "__main__":
    app.run(debug=True)
