-- Crear tabla de usuarios
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL, -- Hash de la contraseña
  role VARCHAR(50) NOT NULL DEFAULT 'bidder', -- Roles: 'admin', 'seller', 'bidder'
  phone VARCHAR(20),
  address TEXT,
  created_by INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de productos subastados
CREATE TABLE auction_item (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  starting_price NUMERIC(10, 2) NOT NULL, -- Precio de inicio de la subasta
  reserve_price NUMERIC(10, 2), -- Precio de reserva (mínimo aceptable)
  buy_now_price NUMERIC(10, 2), -- Opción de "compra inmediata" (si aplica)
  auction_start TIMESTAMP NOT NULL, -- Fecha y hora de inicio de la subasta
  auction_end TIMESTAMP NOT NULL, -- Fecha y hora de finalización de la subasta
  status VARCHAR(20) NOT NULL DEFAULT 'active', -- Ej: 'active', 'closed', 'cancelled'
  seller_id INTEGER NOT NULL REFERENCES users(id), -- Usuario vendedor (role: 'seller')
  image_url VARCHAR(255),
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de pujas
CREATE TABLE bid (
  id SERIAL PRIMARY KEY,
  auction_item_id INTEGER NOT NULL REFERENCES auction_item(id), -- Referencia al ítem subastado
  bidder_id INTEGER NOT NULL REFERENCES users(id), -- Usuario que realiza la oferta (role: 'bidder')
  bid_amount NUMERIC(10, 2) NOT NULL, -- Monto ofertado
  bid_time TIMESTAMP NOT NULL, -- Fecha y hora en que se realizó la oferta
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de transacciones de subasta
CREATE TABLE auction_transaction (
  id SERIAL PRIMARY KEY,
  auction_item_id INTEGER NOT NULL REFERENCES auction_item(id), -- Ítem subastado
  winner_id INTEGER NOT NULL REFERENCES users(id), -- Usuario ganador de la subasta
  final_price NUMERIC(10, 2) NOT NULL, -- Precio final de la subasta
  transaction_date TIMESTAMP NOT NULL, -- Fecha de realización de la transacción
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de pagos de subasta
CREATE TABLE auction_payment (
  id SERIAL PRIMARY KEY,
  auction_transaction_id INTEGER NOT NULL REFERENCES auction_transaction(id), -- Transacción asociada
  amount NUMERIC(10, 2) NOT NULL, -- Monto pagado
  payment_date TIMESTAMP NOT NULL, -- Fecha y hora de pago
  payment_method VARCHAR(50), -- Ej: 'cash', 'card', etc.
  status VARCHAR(20) DEFAULT 'pending', -- Ej: 'pending', 'completed', 'failed'
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de categorías de subastas
CREATE TABLE auction_category (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL, -- Nombre de la categoría (Ej.: 'Electrónica', 'Arte', etc.)
  description TEXT,
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de relación entre productos subastados y categorías
CREATE TABLE auction_item_category (
  id SERIAL PRIMARY KEY,
  auction_item_id INTEGER NOT NULL REFERENCES auction_item(id),
  category_id INTEGER NOT NULL REFERENCES auction_category(id),
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de lista de seguimiento de subastas
CREATE TABLE auction_watchlist (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id), -- Usuario que sigue la subasta
  auction_item_id INTEGER NOT NULL REFERENCES auction_item(id), -- Ítem subastado que se sigue
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);

-- Crear tabla de comentarios en subastas
CREATE TABLE auction_comment (
  id SERIAL PRIMARY KEY,
  auction_item_id INTEGER NOT NULL REFERENCES auction_item(id), -- Ítem subastado
  user_id INTEGER NOT NULL REFERENCES users(id), -- Usuario que comenta
  comment TEXT NOT NULL, -- Contenido del comentario
  comment_date TIMESTAMP NOT NULL, -- Fecha y hora del comentario
  created_by INTEGER,
  created_at TIMESTAMP,
  updated_by INTEGER,
  updated_at TIMESTAMP
);
