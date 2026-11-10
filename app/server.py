#!/usr/bin/env python3
"""A small standard-library storefront server for QA automation practice."""

import json
import logging
import uuid
from decimal import Decimal, ROUND_HALF_UP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HOST = '0.0.0.0'
PORT = 8000
TAX_RATE = Decimal('0.08')
CENT = Decimal('0.01')
MAX_REQUEST_BYTES = 1024 * 1024
INDEX_FILE = Path(__file__).resolve().parent / 'index.html'

INVENTORY = {
    'Food Items': [
        {
            'id': 'gourmet-devops-pizza',
            'name': 'Gourmet DevOps Pizza',
            'price': '14.99',
            'description': 'A handcrafted classic for long release nights.',
            'icon': '🍕',
        },
        {
            'id': 'automation-fuel-coffee',
            'name': 'Automation Fuel Coffee Beans',
            'price': '18.50',
            'description': 'Small-batch beans to keep your test suite moving.',
            'icon': '☕',
        },
    ],
    'General Items': [
        {
            'id': 'docker-whale-plushie',
            'name': 'Docker Whale Plushie',
            'price': '24.99',
            'description': 'A soft desk companion for containerized adventures.',
            'icon': '🐳',
        },
        {
            'id': 'playwright-typescript-cheat-sheet',
            'name': 'Playwright TypeScript Cheat Sheet',
            'price': '9.99',
            'description': 'A quick-reference guide for confident browser tests.',
            'icon': '📘',
        },
    ],
}

PRODUCTS_BY_ID = {
    product['id']: product
    for category_products in INVENTORY.values()
    for product in category_products
}
PRODUCTS_BY_NAME = {
    product['name'].casefold(): product
    for product in PRODUCTS_BY_ID.values()
}


class StorefrontHandler(BaseHTTPRequestHandler):
    """Serve the storefront and its small JSON API."""

    server_version = 'ShipShapeStore/1.0'

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status, message):
        self._send_json(status, {'error': message})

    def _read_json_body(self):
        raw_length = self.headers.get('Content-Length')
        if raw_length is None:
            raise ValueError('Content-Length header is required.')
        try:
            length = int(raw_length)
        except ValueError as error:
            raise ValueError('Content-Length header must be an integer.') from error
        if length < 0:
            raise ValueError('Content-Length cannot be negative.')
        if length > MAX_REQUEST_BYTES:
            raise OverflowError('Request body is too large.')
        body = self.rfile.read(length)
        if len(body) != length:
            raise ValueError('Request body was incomplete.')
        try:
            return json.loads(body.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError('Request body must contain valid JSON.') from error

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path in ('/', '/login', '/store'):
            try:
                body = INDEX_FILE.read_bytes()
            except OSError:
                logging.exception('Unable to read storefront file: %s', INDEX_FILE)
                self._send_error_json(500, 'The storefront is temporarily unavailable.')
                return
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Referrer-Policy', 'same-origin')
            self.end_headers()
            self.wfile.write(body)
            return

        if path == '/api/products':
            catalog = {
                category: [
                    {
                        'id': product['id'],
                        'name': product['name'],
                        'price': float(product['price']),
                        'description': product['description'],
                        'icon': product['icon'],
                    }
                    for product in category_products
                ]
                for category, category_products in INVENTORY.items()
            }
            self._send_json(200, catalog)
            return

        self._send_error_json(404, 'Route not found.')

    def do_POST(self):
        path = self.path.split('?', 1)[0]
        if path not in ('/api/login', '/api/checkout'):
            self._send_error_json(404, 'Route not found.')
            return

        try:
            payload = self._read_json_body()
        except OverflowError as error:
            self._send_error_json(413, str(error))
            return
        except ValueError as error:
            self._send_error_json(400, str(error))
            return

        if path == '/api/login':
            self._handle_login(payload)
        else:
            self._handle_checkout(payload)

    def _handle_login(self, payload):
        if not isinstance(payload, dict):
            self._send_error_json(400, 'Login body must be a JSON object.')
            return
        username = payload.get('username')
        password = payload.get('password')
        if not isinstance(username, str) or not isinstance(password, str):
            self._send_error_json(400, 'Username and password must be strings.')
            return
        if username == 'admin' and password == 'admin':
            self._send_json(200, {'authenticated': True, 'message': 'Login successful.'})
            return
        self._send_error_json(401, 'Invalid username or password.')

    def _handle_checkout(self, payload):
        if not isinstance(payload, list) or not payload:
            self._send_error_json(400, 'Checkout body must be a non-empty JSON array of items.')
            return

        quantities = {}
        for item in payload:
            if not isinstance(item, dict):
                self._send_error_json(400, 'Each checkout item must be a JSON object.')
                return
            product_id = item.get('id', item.get('productId'))
            if product_id is None and isinstance(item.get('name'), str):
                product = PRODUCTS_BY_NAME.get(item['name'].casefold())
            else:
                product = PRODUCTS_BY_ID.get(product_id) if isinstance(product_id, str) else None
            if product is None:
                self._send_error_json(400, 'Checkout contains an unknown product.')
                return

            quantity = item.get('quantity', 1)
            if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 1 or quantity > 100:
                self._send_error_json(400, 'Item quantity must be an integer between 1 and 100.')
                return
            quantities[product['id']] = quantities.get(product['id'], 0) + quantity
            if quantities[product['id']] > 100:
                self._send_error_json(400, 'The total quantity of each product cannot exceed 100.')
                return

        line_items = []
        subtotal = Decimal('0.00')
        for product_id, quantity in quantities.items():
            product = PRODUCTS_BY_ID[product_id]
            unit_price = Decimal(product['price'])
            line_total = (unit_price * quantity).quantize(CENT, rounding=ROUND_HALF_UP)
            subtotal += line_total
            line_items.append({
                'id': product_id,
                'name': product['name'],
                'quantity': quantity,
                'unitPrice': float(unit_price),
                'lineTotal': float(line_total),
            })

        subtotal = subtotal.quantize(CENT, rounding=ROUND_HALF_UP)
        tax = (subtotal * TAX_RATE).quantize(CENT, rounding=ROUND_HALF_UP)
        total = (subtotal + tax).quantize(CENT, rounding=ROUND_HALF_UP)
        order_id = 'ORD-2026-' + uuid.uuid4().hex[:12].upper()
        item_count = sum(quantities.values())
        summary = 'Order for ' + str(item_count) + ' item' + ('' if item_count == 1 else 's') + ' placed successfully.'

        self._send_json(201, {
            'orderId': order_id,
            'items': line_items,
            'subtotal': float(subtotal),
            'taxRate': float(TAX_RATE),
            'tax': float(tax),
            'total': float(total),
            'summary': summary,
        })

    def log_message(self, format_string, *args):
        logging.info('%s - %s', self.address_string(), format_string % args)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    server = ThreadingHTTPServer((HOST, PORT), StorefrontHandler)
    logging.info('ShipShape Market listening on http://%s:%s', HOST, PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('Shutting down storefront server.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()