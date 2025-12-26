use spydx_productpulse;

CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    stock_quantity INT,
    price DECIMAL(10,2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reviews_sentiment (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    review_text TEXT,
    rating INT,
    sentiment_score FLOAT,
    sentiment_label VARCHAR(20),
    demand_score FLOAT
);

CREATE TABLE category_summary (
    category VARCHAR(100) PRIMARY KEY,
    avg_rating FLOAT,
    avg_demand_score FLOAT,
    total_reviews INT,
    positive_share FLOAT
);

