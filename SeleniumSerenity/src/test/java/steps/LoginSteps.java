package steps;

import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import net.serenitybdd.annotations.Steps;
import pages.LoginPage;
import org.testng.Assert;

public class LoginSteps {

    @Steps
    LoginPage loginPage;

    @Given("user is on the login page")
    public void user_is_on_login_page() {
        loginPage.openUrl();
    }

    @When("user enters valid credentials")
    public void user_enters_valid_credentials() {
        loginPage.login("standard_user", "secret_sauce");
    }

    @When("user enters invalid credentials")
    public void user_enters_invalid_credentials() {
        loginPage.login("wrong_user", "wrong_pass");
    }

    @Then("user should be redirected to the products page")
    public void user_should_be_redirected_to_products_page() {
        Assert.assertTrue(loginPage.isOnProductsPage());
    }

    @Then("a login error message should be displayed")
    public void login_error_message_should_be_displayed() {
        Assert.assertTrue(loginPage.isErrorDisplayed());
    }
}