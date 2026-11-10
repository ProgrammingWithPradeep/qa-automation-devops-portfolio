"""Browser end-to-end tests for the ShipShape Market storefront."""

import os
import re

import pytest
from playwright.sync_api import Page, expect


STORE_URL = os.environ.get(
    'STOREFRONT_BASE_URL',
    'http://127.0.0.1:8000',
).rstrip('/')


@pytest.fixture
def storefront(page: Page) -> Page:
    """Open the storefront using the isolated page supplied by pytest-playwright."""
    page.goto(STORE_URL + '/')
    return page


def sign_in(page: Page, username: str = 'admin', password: str = 'admin') -> None:
    page.get_by_label('Username').fill(username)
    page.get_by_label('Password').fill(password)
    page.get_by_role('button', name='Sign in').click()


def test_valid_login_opens_marketplace(storefront: Page) -> None:
    sign_in(storefront)

    expect(storefront).to_have_url(re.compile(r'/store$'))
    expect(storefront.get_by_role('heading', name='Tools for your daily deploy.')).to_be_visible()
    expect(storefront.get_by_role('heading', name='Shopping Basket')).to_be_visible()


def test_invalid_login_shows_error_and_stays_on_login(storefront: Page) -> None:
    sign_in(storefront, username='admin', password='wrong-password')

    expect(storefront.locator('#login-error')).to_be_visible()
    expect(storefront.locator('#login-error')).to_contain_text(
        'username or password was not recognized'
    )
    expect(storefront.locator('#login-view')).to_be_visible()
    expect(storefront.locator('#store-view')).to_be_hidden()


def test_marketplace_shows_products_in_their_categories(storefront: Page) -> None:
    sign_in(storefront)

    food_section = storefront.locator('section[aria-labelledby="food-heading"]')
    general_section = storefront.locator('section[aria-labelledby="general-heading"]')
    expect(food_section.locator('article')).to_have_count(2)
    expect(general_section.locator('article')).to_have_count(2)
    expect(food_section.get_by_role('heading', name='Gourmet DevOps Pizza')).to_be_visible()
    expect(food_section.get_by_role('heading', name='Automation Fuel Coffee Beans')).to_be_visible()
    expect(general_section.get_by_role('heading', name='Docker Whale Plushie')).to_be_visible()
    expect(
        general_section.get_by_role(
            'heading',
            name='Playwright TypeScript Cheat Sheet',
        )
    ).to_be_visible()
    expect(storefront.get_by_role('button', name='Proceed to Payment')).to_be_disabled()


def test_basket_updates_quantities_and_eight_percent_tax(storefront: Page) -> None:
    sign_in(storefront)
    storefront.locator('[data-product-id="gourmet-devops-pizza"]').click()
    storefront.locator('[data-product-id="gourmet-devops-pizza"]').click()
    storefront.locator('[data-product-id="automation-fuel-coffee"]').click()

    expect(storefront.locator('#cart-count')).to_have_text('3')
    expect(storefront.locator('#cart-subtotal')).to_have_text('$48.48')
    expect(storefront.locator('#cart-tax')).to_have_text('$3.88')
    expect(storefront.locator('#cart-total')).to_have_text('$52.36')

    storefront.get_by_role(
        'button',
        name='Remove one Gourmet DevOps Pizza',
    ).click()
    expect(storefront.locator('#cart-count')).to_have_text('2')
    expect(storefront.locator('#cart-subtotal')).to_have_text('$33.49')
    expect(storefront.locator('#cart-tax')).to_have_text('$2.68')
    expect(storefront.locator('#cart-total')).to_have_text('$36.17')


def test_removing_last_item_restores_empty_basket(storefront: Page) -> None:
    sign_in(storefront)
    storefront.locator('[data-product-id="docker-whale-plushie"]').click()
    storefront.get_by_role(
        'button',
        name='Remove one Docker Whale Plushie',
    ).click()

    expect(storefront.locator('#empty-cart')).to_be_visible()
    expect(storefront.locator('#cart-count')).to_have_text('0')
    expect(storefront.locator('#cart-subtotal')).to_have_text('$0.00')
    expect(storefront.get_by_role('button', name='Proceed to Payment')).to_be_disabled()


def test_customer_can_review_and_place_order(storefront: Page) -> None:
    sign_in(storefront)
    storefront.locator('[data-product-id="gourmet-devops-pizza"]').click()
    storefront.locator('[data-product-id="gourmet-devops-pizza"]').click()
    storefront.locator('[data-product-id="automation-fuel-coffee"]').click()
    storefront.get_by_role('button', name='Proceed to Payment').click()

    expect(storefront.locator('#payment-view')).to_be_visible()
    expect(storefront.locator('#payment-items')).to_contain_text('Gourmet DevOps Pizza × 2')
    expect(storefront.locator('#payment-items')).to_contain_text('Automation Fuel Coffee Beans × 1')
    expect(storefront.locator('#payment-subtotal')).to_have_text('$48.48')
    expect(storefront.locator('#payment-tax')).to_have_text('$3.88')
    expect(storefront.locator('#payment-total')).to_have_text('$52.36')

    storefront.get_by_role('button', name='Place order').click()

    expect(storefront.locator('#success-view')).to_be_visible()
    expect(storefront.locator('#ack-header')).to_have_text('Order Successfully Placed')
    expect(storefront.locator('#ack-order-id')).to_have_text(
        re.compile(r'^ORD-2026-[A-F0-9]{12}$')
    )
    expect(storefront.locator('#ack-summary')).to_have_text(
        'Order for 3 items placed successfully. '
        'Subtotal: $48.48. Tax: $3.88. Total: $52.36.'
    )

    storefront.get_by_role('button', name='Continue shopping').click()
    expect(storefront.locator('#store-view')).to_be_visible()
    expect(storefront.locator('#empty-cart')).to_be_visible()
    expect(storefront.locator('#cart-count')).to_have_text('0')


def test_customer_can_return_to_marketplace_from_payment(storefront: Page) -> None:
    sign_in(storefront)
    storefront.locator('[data-product-id="playwright-typescript-cheat-sheet"]').click()
    storefront.get_by_role('button', name='Proceed to Payment').click()
    storefront.get_by_role('button', name='Back to marketplace').click()

    expect(storefront.locator('#store-view')).to_be_visible()
    expect(storefront.locator('#cart-count')).to_have_text('1')
    expect(storefront.locator('#cart-subtotal')).to_have_text('$9.99')


def test_sign_out_returns_customer_to_login(storefront: Page) -> None:
    sign_in(storefront)
    storefront.get_by_role('button', name='Sign out').click()

    expect(storefront).to_have_url(re.compile(r'/login$'))
    expect(storefront.locator('#login-view')).to_be_visible()
    expect(storefront.locator('#store-view')).to_be_hidden()
