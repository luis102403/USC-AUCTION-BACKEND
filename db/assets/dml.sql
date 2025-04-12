-- Insertar usuarios
INSERT INTO users (username, email, password, role, phone, address, created_by, created_at, updated_by, updated_at)
VALUES
  ('admin_user', 'admin@example.com', 'admin_password_hash', 'admin', '1234567890', '123 Admin St, Admin City', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  ('seller_user', 'seller@example.com', 'seller_password_hash', 'seller', '9876543210', '456 Seller Ave, Seller Town', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  ('bidder_user', 'bidder@example.com', 'bidder_password_hash', 'bidder', '1122334455', '789 Bidder Rd, Bidder City', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

-- Insertar categorías
INSERT INTO auction_category (name, description, created_by, created_at, updated_by, updated_at)
VALUES
  ('Electrónica', 'Categoría de productos electrónicos', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  ('Arte', 'Categoría de artículos artísticos', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

-- Insertar productos subastados
INSERT INTO auction_item (title, description, starting_price, reserve_price, buy_now_price, auction_start, auction_end, status, seller_id, image_url, created_by, created_at, updated_by, updated_at)
VALUES
  ('Laptop HP', 'Laptop HP con procesador Intel i7 y 16GB de RAM', 500.00, 400.00, 800.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '7 day', 'active', 2, 'http://example.com/laptop.jpg', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  ('Pintura Abstracta', 'Obra de arte moderna, pintada en 2020', 300.00, 250.00, 600.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '7 day', 'active', 2, 'http://example.com/pintura.jpg', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

-- Insertar ofertas (pujas)
INSERT INTO bid (auction_item_id, bidder_id, bid_amount, bid_time, created_by, created_at, updated_by, updated_at)
VALUES
  (1, 3, 550.00, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  (1, 3, 600.00, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  (2, 3, 350.00, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

-- Insertar transacciones de subasta
INSERT INTO auction_transaction (auction_item_id, winner_id, final_price, transaction_date, created_by, created_at, updated_by, updated_at)
VALUES
  (1, 3, 600.00, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  (2, 3, 350.00, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

-- Insertar pagos de subasta
INSERT INTO auction_payment (auction_transaction_id, amount, payment_date, payment_method, status, created_by, created_at, updated_by, updated_at)
VALUES
  (1, 600.00, CURRENT_TIMESTAMP, 'card', 'completed', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  (2, 350.00, CURRENT_TIMESTAMP, 'cash', 'completed', 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

-- Insertar relaciones entre productos y categorías
INSERT INTO auction_item_category (auction_item_id, category_id, created_by, created_at, updated_by, updated_at)
VALUES
  (1, 1, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),  -- Laptop HP en la categoría de Electrónica
  (2, 2, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);  -- Pintura Abstracta en la categoría de Arte

-- Insertar en la lista de seguimiento de subastas
INSERT INTO auction_watchlist (user_id, auction_item_id, created_by, created_at, updated_by, updated_at)
VALUES
  (3, 1, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  (3, 2, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

-- Insertar comentarios en subastas
INSERT INTO auction_comment (auction_item_id, user_id, comment, comment_date, created_by, created_at, updated_by, updated_at)
VALUES
  (1, 3, '¡Excelente laptop, estoy interesado!', CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
  (2, 3, 'Una obra de arte única, me encanta!', CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);
