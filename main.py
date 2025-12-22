from playwright.sync_api import sync_playwright
import json

PRODUCTS = []


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
        except (TypeError, ValueError):
            continue

        if rating < 4.0:
            continue

        product["rating"] = rating

        # Remove None values
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
                parsed = parse_products(data)
                PRODUCTS.extend(parsed)
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


if __name__ == "__main__":
    products = scrape_rated_products()
    print(json.dumps(products, indent=2, ensure_ascii=False))
