Feature: Login functionality
  As a user
  I want to log in with valid or invalid credentials
  So that I can access the application or see an error

  Scenario: Successful login with valid credentials
    Given user is on the login page
    When user enters valid credentials
    Then user should be redirected to the products page

  Scenario: Unsuccessful login with invalid credentials
    Given user is on the login page
    When user enters invalid credentials
    Then a login error message should be displayed