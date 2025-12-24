from playwright.sync_api import sync_playwright
import json
import os

PRODUCTS = []
PRICE_FILE = "prices.json"


def load_old_prices():
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_prices(prices):
    with open(PRICE_FILE, "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=2, ensure_ascii=False)


def parse_products(mtop_json):
    results = []

    try:
        items = (
            mtop_json["data"]["result"][0]
            ["resultValue"]["41701"]["data"]
        )
    except Exception:
        return results

    for item in items:

        if item.get("isAd") == "1":
            continue

        product = {
            "title": item.get("itemTitle"),
            "item_id": item.get("itemId"),
            "sku_id": item.get("skuId"),
            "category_id": item.get("categoryId"),
            "price": item.get("itemDiscountPrice") or item.get("promotion_price"),
            "original_price": item.get("utLogMap", {}).get("original_price"),
            "currency": item.get("currency"),
            "discount": item.get("itemDiscount"),
            "rating": item.get("itemRatingScore"),
            "review_count": item.get("reviewCount"),
            "product_url": "https:" + item.get("itemUrl", ""),
            "image_url": item.get("itemImg"),
            "seller_id": item.get("sellerId"),
            "shop_id": item.get("shopId"),
        }

        try:
            rating = float(product["rating"])
            price = float(product["price"])
        except (TypeError, ValueError):
            continue

        if rating < 4.0:
            continue

        product["rating"] = rating
        product["price"] = price

        product = {k: v for k, v in product.items() if v is not None}
        results.append(product)

    return results


def scrape_rated_products():
    global PRODUCTS
    PRODUCTS = []

    def handle_response(response):
        if "mtop.relationrecommend.lazadarecommend.recommend" in response.url:
            try:
                data = response.json()
                PRODUCTS.extend(parse_products(data))
            except Exception:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("response", handle_response)

        page.goto("https://www.daraz.com.np", timeout=60000)
        page.wait_for_timeout(10000)

        browser.close()

    return PRODUCTS


def print_products(products, old_prices):
    print("\n📦 SCRAPED PRODUCTS (Rating ≥ 4.0)")
    print("=" * 60)

    for idx, product in enumerate(products, 1):
        old_price = old_prices.get(product["item_id"])
        status = product["price_status"]

        arrow = "➖"
        if status == "down":
            arrow = "⬇️"
        elif status == "up":
            arrow = "⬆️"

        print(f"{idx}. {product['title']}")
        print(f"   ⭐ Rating: {product['rating']}")
        print(f"   💰 Price: {product['price']} {product.get('currency', '')} {arrow}")

        if old_price is not None:
            print(f"   🔁 Old price: {old_price}")

        print(f"   🛒 Reviews: {product.get('review_count', 'N/A')}")
        print(f"   🔗 Link: {product['product_url']}")
        print("-" * 60)


def check_price_changes(products):
    old_prices = load_old_prices()
    new_prices = {}

    for product in products:
        item_id = product["item_id"]
        new_price = product["price"]
        new_prices[item_id] = new_price

        old_price = old_prices.get(item_id)

        if old_price is None:
            product["price_status"] = "same"
        elif new_price < old_price:
            product["price_status"] = "down"
        elif new_price > old_price:
            product["price_status"] = "up"
        else:
            product["price_status"] = "same"

        if product["price_status"] == "down":
            print("\n🔔 PRICE DROP ALERT!")
            print(f"Product: {product['title']}")
            print(f"Old price: {old_price}")
            print(f"New price: {new_price}")
            print(f"Link: {product['product_url']}")
            print("-" * 60)

    save_prices(new_prices)
    return old_prices


if __name__ == "__main__":
    products = scrape_rated_products()

    old_prices = check_price_changes(products)
    print_products(products, old_prices)
