Feature: Checkout functionality
  As a logged-in user
  I want to add products to the cart and checkout
  So that I can place an order or see an error

  Scenario: Successful checkout with valid information
    Given user is logged in with valid credentials
    When user adds a product to the cart
    And user proceeds to checkout
    And user enters valid shipping information
    Then order should be successfully placed

  Scenario: Unsuccessful checkout with missing information
    Given user is logged in with valid credentials
    When user adds a product to the cart
    And user proceeds to checkout
    And user leaves shipping information blank
    Then a checkout error message should be displayed