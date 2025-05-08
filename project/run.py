from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    services = [
        {
            "title": "Prescription Medicine Delivery",
            "description": "Get your prescription medicines delivered quickly and securely, ensuring you never miss a dose."
        },
        {
            "title": "OTC Medication",
            "description": "Shop for a wide range of health and wellness products, including vitamins, supplements, and personal care items."
        },
        {
            "title": "Special delivery types",
            "description": "Choose from a variety of delivery options, including temperature-controlled delivery."
        },
        {
            "title": "24/7 Customer support",
            "description": "Our support team is here round the clock for your orders, queries, and health-related needs."
        }
    ]

    products = [
        {
            "name": "Panadol Rapid 48 Caplets",
            "price": "10.00",
            "image": "panadol.jpg"
        },
        {
            "name": "Nurofen Zavance 96 pack",
            "price": "15.00",
            "image": "ibuprofen.jpg"
        },
        {
            "name": "Claratyne Allergy & Hayfever Relief",
            "price": "9.50",
            "image": "antihistamine.jpg"
        },
        {
            "name": "CeraVe Moisturising Cream",
            "price": "25.99",
            "image": "cerave cream.jpg"
        },
        {
            "name": "CeraVe Skin Renewing Night Cream",
            "price": "36.99",
            "image": "cerave night cream.jpg"
        },
        {
            "name": "Maybelline Lasting Fix Setting Loose Powder",
            "price": "9.99",
            "image": "maybelline powder.jpg"
        },
        {
            "name": "Maybelline Fit Me True-to-tone Blush",
            "price": "9.50",
            "image": "maybelline blush.jpg"
        },
        {
            "name": "Difflam Plus Sore Throat Anaesthetic Spray",
            "price": "8.45",
            "image": "sore throat.jpg"
        }
    ]

    return render_template("home.html", services=services, products=products)

if __name__ == '__main__':
    app.run(debug=True)
