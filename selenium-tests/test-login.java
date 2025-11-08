// selenium-tests/test-login.java
WebDriver driver = new ChromeDriver();
driver.get("https://demo.smart-hub.io/");
driver.findElement(By.id("username")).sendKeys("demo");
driver.findElement(By.id("password")).sendKeys("demo123");
driver.findElement(By.cssSelector("button[type='submit']")).click();
Assert.assertTrue(driver.findElements(By.className("sensor-card")).size() > 0);
