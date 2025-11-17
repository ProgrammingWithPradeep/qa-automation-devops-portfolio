package pages;

import net.serenitybdd.core.pages.PageObject;
import org.openqa.selenium.By;

public class CheckoutPage extends PageObject {

    private By firstNameField = By.id("first-name");
    private By lastNameField = By.id("last-name");
    private By postalCodeField = By.id("postal-code");
    private By continueButton = By.id("continue");
    private By finishButton = By.id("finish");
    private By completeHeader = By.className("complete-header");
    private By errorMessage = By.cssSelector("h3[data-test='error']");

    public void enterShippingInfo(String firstName, String lastName, String postalCode) {
        $(firstNameField).sendKeys(firstName);
        $(lastNameField).sendKeys(lastName);
        $(postalCodeField).sendKeys(postalCode);
        $(continueButton).click();
    }

    public void finishCheckout() {
        $(finishButton).click();
    }

    public boolean isOrderComplete() {
        return $(completeHeader).getText().equals("THANK YOU FOR YOUR ORDER");
    }

    public boolean isErrorDisplayed() {
        return $(errorMessage).isDisplayed();
    }
}