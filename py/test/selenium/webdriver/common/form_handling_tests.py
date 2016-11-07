# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TestFormHandling(object):

    @pytest.mark.xfail_marionette(reason="https://bugzilla.mozilla.org/show_bug.cgi?id=1291320")
    def testShouldClickOnSubmitInputElements(self, driver, pages):
        pages.load("formPage.html")
        driver.find_element_by_id("submitButton").click()
        assert driver.title == "We Arrive Here"

    def testClickingOnUnclickableElementsDoesNothing(self, driver, pages):
        pages.load("formPage.html")
        driver.find_element_by_xpath("//body").click()

    def testShouldBeAbleToClickImageButtons(self, driver, pages):
        pages.load("formPage.html")
        driver.find_element_by_id("imageButton").click()
        WebDriverWait(driver, 3).until(EC.title_is("We Arrive Here"))


    def testShouldBeAbleToSubmitForms(self, driver, pages):
        pages.load("formPage.html")
        driver.find_element_by_name("login").submit()
        assert driver.title == "We Arrive Here"

    def testShouldSubmitAFormWhenAnyInputElementWithinThatFormIsSubmitted(self, driver, pages):
        pages.load("formPage.html")
        driver.find_element_by_id("checky").submit()
        assert driver.title == "We Arrive Here"

    def testShouldSubmitAFormWhenAnyElementWihinThatFormIsSubmitted(self, driver, pages):
        pages.load("formPage.html")
        driver.find_element_by_xpath("//form/p").submit()
        assert driver.title == "We Arrive Here"

    def testShouldNotBeAbleToSubmitAFormThatDoesNotExist(self, driver, pages):
        pages.load("formPage.html")
        with pytest.raises(NoSuchElementException):
            driver.find_element_by_name("there is no spoon").submit()

    def testShouldBeAbleToEnterTextIntoATextAreaBySettingItsValue(self, driver, pages):
        pages.load("javascriptPage.html")
        textarea = driver.find_element_by_id("keyUpArea")
        cheesey = "Brie and cheddar"
        textarea.send_keys(cheesey)
        assert textarea.get_attribute("value") == cheesey

    def testShouldEnterDataIntoFormFields(self, driver, pages):
        pages.load("xhtmlTest.html")
        element = driver.find_element_by_xpath("//form[@name='someForm']/input[@id='username']")
        originalValue = element.get_attribute("value")
        assert originalValue == "change"

        element.clear()
        element.send_keys("some text")

        element = driver.find_element_by_xpath("//form[@name='someForm']/input[@id='username']")
        newFormValue = element.get_attribute("value")
        assert newFormValue == "some text"

    def testShouldBeAbleToSelectACheckBox(self, driver, pages):
        pages.load("formPage.html")
        checkbox = driver.find_element_by_id("checky")
        assert checkbox.is_selected() is False
        checkbox.click()
        assert checkbox.is_selected() is True
        checkbox.click()
        assert checkbox.is_selected() is False

    def testShouldToggleTheCheckedStateOfACheckbox(self, driver, pages):
        pages.load("formPage.html")
        checkbox = driver.find_element_by_id("checky")
        assert checkbox.is_selected() is False
        checkbox.click()
        assert checkbox.is_selected() is True
        checkbox.click()
        assert checkbox.is_selected() is False

    def testTogglingACheckboxShouldReturnItsCurrentState(self, driver, pages):
        pages.load("formPage.html")
        checkbox = driver.find_element_by_id("checky")
        assert checkbox.is_selected() is False
        checkbox.click()
        assert checkbox.is_selected() is True
        checkbox.click()
        assert checkbox.is_selected() is False

    def testShouldBeAbleToSelectARadioButton(self, driver, pages):
        pages.load("formPage.html")
        radioButton = driver.find_element_by_id("peas")
        assert radioButton.is_selected() is False
        radioButton.click()
        assert radioButton.is_selected() is True

    def testShouldBeAbleToSelectARadioButtonByClickingOnIt(self, driver, pages):
        pages.load("formPage.html")
        radioButton = driver.find_element_by_id("peas")
        assert radioButton.is_selected() is False
        radioButton.click()
        assert radioButton.is_selected() is True

    def testShouldReturnStateOfRadioButtonsBeforeInteration(self, driver, pages):
        pages.load("formPage.html")
        radioButton = driver.find_element_by_id("cheese_and_peas")
        assert radioButton.is_selected() is True

        radioButton = driver.find_element_by_id("cheese")
        assert radioButton.is_selected() is False

    # [ExpectedException(typeof(NotImplementedException))]
    # def testShouldThrowAnExceptionWhenTogglingTheStateOfARadioButton(self, driver, pages):
    #    pages.load("formPage.html")
    #    radioButton = driver.find_element_by_id("cheese"))
    #    radioButton.click()

    # [IgnoreBrowser(Browser.IE, "IE allows toggling of an option not in a multiselect")]
    # [ExpectedException(typeof(NotImplementedException))]
    # def testTogglingAnOptionShouldThrowAnExceptionIfTheOptionIsNotInAMultiSelect(self, driver, pages):
    #    pages.load("formPage.html")
    #    select = driver.find_element_by_name("selectomatic"))
    #    option = select.find_elements_by_tag_name("option"))[0]
    #    option.click()

    def testTogglingAnOptionShouldToggleOptionsInAMultiSelect(self, driver, pages):
        pages.load("formPage.html")

        select = driver.find_element_by_name("multi")
        option = select.find_elements_by_tag_name("option")[0]

        selected = option.is_selected()
        option.click()
        assert not selected == option.is_selected()

        option.click()
        assert selected == option.is_selected()

    def testShouldThrowAnExceptionWhenSelectingAnUnselectableElement(self, driver, pages):
        pages.load("formPage.html")
        element = driver.find_element_by_xpath("//title")
        with pytest.raises(WebDriverException):
            element.click()

    def testSendingKeyboardEventsShouldAppendTextInInputs(self, driver, pages):
        pages.load("formPage.html")
        element = driver.find_element_by_id("working")
        element.send_keys("Some")
        value = element.get_attribute("value")
        assert value == "Some"

        element.send_keys(" text")
        value = element.get_attribute("value")
        assert value == "Some text"

    def testShouldBeAbleToClearTextFromInputElements(self, driver, pages):
        pages.load("formPage.html")
        element = driver.find_element_by_id("working")
        element.send_keys("Some text")
        value = element.get_attribute("value")
        assert len(value) > 0

        element.clear()
        value = element.get_attribute("value")
        assert len(value) == 0

    def testEmptyTextBoxesShouldReturnAnEmptyStringNotNull(self, driver, pages):
        pages.load("formPage.html")
        emptyTextBox = driver.find_element_by_id("working")
        assert emptyTextBox.get_attribute("value") == ""

        emptyTextArea = driver.find_element_by_id("emptyTextArea")
        assert emptyTextArea.get_attribute("value") == ""

    def testShouldBeAbleToClearTextFromTextAreas(self, driver, pages):
        pages.load("formPage.html")
        element = driver.find_element_by_id("withText")
        element.send_keys("Some text")
        value = element.get_attribute("value")
        assert len(value) > 0

        element.clear()
        value = element.get_attribute("value")
        assert len(value) == 0

    def testRadioShouldNotBeSelectedAfterSelectingSibling(self, driver, pages):
        pages.load("formPage.html")
        cheese = driver.find_element_by_id("cheese")
        peas = driver.find_element_by_id("peas")

        cheese.click()
        assert cheese.is_selected() is True
        assert peas.is_selected() is False

        peas.click()
        assert cheese.is_selected() is False
        assert peas.is_selected() is True
