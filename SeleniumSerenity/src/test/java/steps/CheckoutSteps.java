package steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import net.serenitybdd.annotations.Steps;
//import net.thucydides.*;
import org.testng.annotations.Test;
import pages.CartPage;
import pages.CheckoutPage;
import pages.LoginPage;
import org.testng.Assert;

public class CheckoutSteps {

    @Steps
    LoginPage loginPage;

    @Steps
    CartPage cartPage;

    @Steps
    CheckoutPage checkoutPage;

    @Test
    @Given("user is logged in with valid credentials")
    public void user_is_logged_in_with_valid_credentials() {
        loginPage.open();
        loginPage.login("standard_user", "secret_sauce");
        Assert.assertTrue(loginPage.isOnProductsPage());
    }

    @When("user adds a product to the cart")
    public void user_adds_a_product_to_the_cart() {
        cartPage.addFirstProductToCart();
      //  Assert.assertTrue(cartPage.isProductInCart());
    }

    @When("user proceeds to checkout")
    public void user_proceeds_to_checkout() {
        cartPage.goToCheckout();
    }

    @When("user enters valid shipping information")
    public void user_enters_valid_shipping_information() {
        checkoutPage.enterShippingInfo("John", "Doe", "12345");
        checkoutPage.finishCheckout();
    }

    @Then("order should be successfully placed")
    public void order_should_be_successfully_placed() {
     //   Assert.assertTrue(checkoutPage.isOrderComplete());
    }

    @When("user leaves shipping information blank")
    public void user_leaves_shipping_information_blank() {
        checkoutPage.enterShippingInfo("", "", "");
        checkoutPage.finishCheckout();
    }

    @Then("a checkout error message should be displayed")
    public void checkout_error_message_should_be_displayed() {
      Assert.assertTrue(checkoutPage.isErrorDisplayed());
    }
}