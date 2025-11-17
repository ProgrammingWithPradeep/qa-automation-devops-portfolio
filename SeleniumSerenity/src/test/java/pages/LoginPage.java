package pages;

import net.serenitybdd.core.pages.PageObject;

public class LoginPage extends PageObject {

    public void openUrl() {
        this.openUrl("https://www.saucedemo.com/");
    }

    public void login(String username, String password) {
        $("#user-name").type(username);
        $("#password").type(password);
        $("#login-button").click();
    }

    public boolean isOnProductsPage() {
        return $("#inventory_container").isVisible();
    }

    public boolean isErrorDisplayed() {
        return $(".error-message-container").isVisible();
    }
}