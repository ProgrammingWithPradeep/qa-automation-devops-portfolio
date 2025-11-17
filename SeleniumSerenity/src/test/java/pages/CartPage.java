package pages;

import net.serenitybdd.core.pages.PageObject;
import org.openqa.selenium.By;

public class CartPage extends PageObject {

    private By addToCartButton = By.cssSelector(".inventory_item button");
    private By cartIcon = By.id("shopping_cart_container");
    private By checkoutButton = By.id("checkout");

    public void addFirstProductToCart() {
        $(addToCartButton).click();
    }

    public boolean isProductInCart() {
        $(cartIcon).click();
        return $(checkoutButton).isDisplayed();
    }

    public void goToCheckout() {
        $(cartIcon).click();
        $(checkoutButton).click();
    }
}