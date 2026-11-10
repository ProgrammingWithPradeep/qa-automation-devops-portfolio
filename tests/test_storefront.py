"""Pytest workflow tests for the ShipShape storefront."""

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from app.server import INVENTORY, StorefrontHandler


@pytest.fixture(scope='module')
def storefront_url():
    """Run the real request handler on an ephemeral local port for this module."""
    server = ThreadingHTTPServer(('127.0.0.1', 0), StorefrontHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield 'http://127.0.0.1:' + str(server.server_address[1])
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def request_storefront(base_url, path, method='GET', payload=None, raw_body=None):
    """Send a JSON request and return status, headers, and response bytes."""
    if raw_body is not None:
        body = raw_body
    elif payload is not None:
        body = json.dumps(payload).encode('utf-8')
    else:
        body = None

    request = Request(base_url + path, data=body, method=method)
    if body is not None:
        request.add_header('Content-Type', 'application/json')

    try:
        response = urlopen(request, timeout=5)
    except HTTPError as error:
        response = error

    with response:
        return response.status, response.headers, response.read()


def response_json(body):
    return json.loads(body.decode('utf-8'))


@pytest.mark.parametrize('path', ['/', '/login', '/store'])
def test_storefront_pages_are_served(storefront_url, path):
    status, headers, body = request_storefront(storefront_url, path)

    assert status == 200
    assert headers.get_content_type() == 'text/html'
    assert b'ShipShape Market' in body
    assert b'id="login-view"' in body
    assert b'id="ack-header"' in body


def test_catalog_contains_expected_products_and_categories(storefront_url):
    status, headers, body = request_storefront(storefront_url, '/api/products')

    assert status == 200
    assert headers.get_content_type() == 'application/json'
    catalog = response_json(body)
    assert set(catalog) == {'Food Items', 'General Items'}
    assert {
        product['name']: product['price']
        for product in catalog['Food Items']
    } == {
        'Gourmet DevOps Pizza': 14.99,
        'Automation Fuel Coffee Beans': 18.50,
    }
    assert {
        product['name']: product['price']
        for product in catalog['General Items']
    } == {
        'Docker Whale Plushie': 24.99,
        'Playwright TypeScript Cheat Sheet': 9.99,
    }


def test_valid_login_is_accepted(storefront_url):
    status, _, body = request_storefront(
        storefront_url,
        '/api/login',
        method='POST',
        payload={'username': 'admin', 'password': 'admin'},
    )

    assert status == 200
    assert response_json(body)['authenticated'] is True


@pytest.mark.parametrize(
    'credentials',
    [
        {'username': 'admin', 'password': 'incorrect'},
        {'username': 'visitor', 'password': 'admin'},
        {'username': '', 'password': ''},
    ],
)
def test_invalid_login_credentials_are_rejected(storefront_url, credentials):
    status, _, body = request_storefront(
        storefront_url,
        '/api/login',
        method='POST',
        payload=credentials,
    )

    assert status == 401
    assert 'error' in response_json(body)


@pytest.mark.parametrize(
    'payload',
    [
        [],
        {'username': 'admin'},
        {'username': 123, 'password': 'admin'},
    ],
)
def test_malformed_login_payload_is_rejected(storefront_url, payload):
    status, _, body = request_storefront(
        storefront_url,
        '/api/login',
        method='POST',
        payload=payload,
    )

    assert status == 400
    assert 'error' in response_json(body)


def test_checkout_returns_receipt_and_calculates_totals_from_inventory(storefront_url):
    status, _, body = request_storefront(
        storefront_url,
        '/api/checkout',
        method='POST',
        payload=[
            {'id': 'gourmet-devops-pizza', 'quantity': 2, 'price': 0.01},
            {'id': 'docker-whale-plushie', 'quantity': 1},
        ],
    )

    receipt = response_json(body)
    assert status == 201
    assert receipt['orderId'].startswith('ORD-2026-')
    assert receipt['items'] == [
        {
            'id': 'gourmet-devops-pizza',
            'name': 'Gourmet DevOps Pizza',
            'quantity': 2,
            'unitPrice': 14.99,
            'lineTotal': 29.98,
        },
        {
            'id': 'docker-whale-plushie',
            'name': 'Docker Whale Plushie',
            'quantity': 1,
            'unitPrice': 24.99,
            'lineTotal': 24.99,
        },
    ]
    assert receipt['subtotal'] == pytest.approx(54.97)
    assert receipt['taxRate'] == pytest.approx(0.08)
    assert receipt['tax'] == pytest.approx(4.40)
    assert receipt['total'] == pytest.approx(59.37)
    assert receipt['summary'] == 'Order for 3 items placed successfully.'


def test_checkout_accepts_product_name_and_defaults_quantity_to_one(storefront_url):
    product_name = INVENTORY['Food Items'][0]['name']
    status, _, body = request_storefront(
        storefront_url,
        '/api/checkout',
        method='POST',
        payload=[{'name': product_name}],
    )

    receipt = response_json(body)
    assert status == 201
    assert receipt['items'][0]['quantity'] == 1
    assert receipt['subtotal'] == pytest.approx(14.99)
    assert receipt['tax'] == pytest.approx(1.20)
    assert receipt['total'] == pytest.approx(16.19)
    assert receipt['summary'] == 'Order for 1 item placed successfully.'


def test_checkout_merges_duplicate_product_lines(storefront_url):
    status, _, body = request_storefront(
        storefront_url,
        '/api/checkout',
        method='POST',
        payload=[
            {'id': 'playwright-typescript-cheat-sheet'},
            {'id': 'playwright-typescript-cheat-sheet', 'quantity': 2},
        ],
    )

    receipt = response_json(body)
    assert status == 201
    assert len(receipt['items']) == 1
    assert receipt['items'][0]['quantity'] == 3
    assert receipt['subtotal'] == pytest.approx(29.97)


def test_each_checkout_receipt_has_a_unique_order_id(storefront_url):
    payload = [{'id': 'automation-fuel-coffee'}]
    first_status, _, first_body = request_storefront(
        storefront_url, '/api/checkout', method='POST', payload=payload
    )
    second_status, _, second_body = request_storefront(
        storefront_url, '/api/checkout', method='POST', payload=payload
    )

    assert first_status == 201
    assert second_status == 201
    assert response_json(first_body)['orderId'] != response_json(second_body)['orderId']


@pytest.mark.parametrize(
    'payload',
    [
        [],
        {},
        ['not-an-item'],
        [{'id': 'not-a-product'}],
        [{'id': 'gourmet-devops-pizza', 'quantity': 0}],
        [{'id': 'gourmet-devops-pizza', 'quantity': True}],
        [{'id': 'gourmet-devops-pizza', 'quantity': 101}],
    ],
)
def test_invalid_checkout_orders_are_rejected(storefront_url, payload):
    status, _, body = request_storefront(
        storefront_url,
        '/api/checkout',
        method='POST',
        payload=payload,
    )

    assert status == 400
    assert 'error' in response_json(body)


def test_invalid_json_body_is_rejected(storefront_url):
    status, _, body = request_storefront(
        storefront_url,
        '/api/login',
        method='POST',
        raw_body=b'{"username":',
    )

    assert status == 400
    assert 'error' in response_json(body)


def test_unknown_route_returns_not_found(storefront_url):
    status, _, body = request_storefront(storefront_url, '/not-a-route')

    assert status == 404
    assert response_json(body)['error'] == 'Route not found.'
