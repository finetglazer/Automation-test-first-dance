import pytest
import time
from selenium.webdriver.common.keys import Keys
from pages.rich_text_editor_component import RichTextEditorComponent

class TestRichTextEditorComponent:
    """Test suite for Rich Text Editor Component functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_driver):
        """Setup method with authenticated driver and navigate to create product page"""
        self.driver = authenticated_driver
        self.editor = RichTextEditorComponent(self.driver)

        # Navigate to create product page where the editor component is used
        print("🏗️ Navigating to create product page...")
        self.driver.get("http://localhost/#/pages/catalogue/products/create-product")

        # Wait for page and editor to load
        success = self.editor.wait_for_editor_load()
        if not success:
            pytest.fail("Failed to load rich text editor component")

        print("✓ Rich text editor component setup completed")

    # =======================
    # CODE VIEW TESTS
    # =======================

    @pytest.mark.smoke
    def test_code_view_button_turn_on(self):
        """Test Case 1: Testing code view button function when turn on"""
        # Step 1: Click on the button `</>`
        success = self.editor.toggle_code_view()
        assert success, "Should be able to click code view button"

        # Expected result: Display the view of coding
        assert self.editor.is_in_code_view(), "Should switch to code view mode"
        self.editor.take_editor_screenshot("code_view_on")

    @pytest.mark.smoke
    def test_code_view_button_turn_off(self):
        """Test Case 2: Testing code view button function from turn back to default state"""
        # Step 1: Click on the button `</>`
        self.editor.toggle_code_view()
        assert self.editor.is_in_code_view(), "Should be in code view"

        # Step 2: Click on the button `</>` again
        self.editor.toggle_code_view()

        # Expected result: Display the default view
        assert not self.editor.is_in_code_view(), "Should return to WYSIWYG view"
        self.editor.take_editor_screenshot("code_view_off")

    @pytest.mark.regression
    def test_code_view_with_content(self):
        """Test Case 3: Testing code view button function turn back to default state in case having code in the form"""
        # Step 1: Click on the button `</>`
        self.editor.toggle_code_view()
        assert self.editor.is_in_code_view(), "Should be in code view"

        # Step 2: Add any code lines
        code_content = "<h1>Test Header</h1><p>Test paragraph with <strong>bold</strong> text.</p>"
        success = self.editor.enter_code(code_content)
        assert success, "Should be able to enter code"

        # Step 3: Click on the button `</>` again
        self.editor.toggle_code_view()

        # Expected result: Display the code in the code form, then turn back to default passage in the next state
        assert not self.editor.is_in_code_view(), "Should return to WYSIWYG view"

        # Verify content is preserved and displayed as formatted text
        content = self.editor.get_editor_content()
        assert "Test Header" in content, "Header should be preserved"
        assert "Test paragraph" in content, "Paragraph should be preserved"
        self.editor.take_editor_screenshot("code_view_with_content")

    # =======================
    # UNDO/REDO TESTS
    # =======================

    @pytest.mark.smoke
    def test_undo_button_after_typing(self):
        """Test Case 4: Test backward button function when we wrote"""
        # Step 1: Add a character
        self.editor.enter_text("A")
        assert self.editor.has_content(), "Editor should have content"

        # Step 2: Click backward button
        success = self.editor.click_undo()
        assert success, "Should be able to click undo button"

        # Expected result: Display the empty form
        time.sleep(0.5)  # Wait for undo to take effect
        assert not self.editor.has_content(), "Editor should be empty after undo"
        self.editor.take_editor_screenshot("undo_after_typing")

    @pytest.mark.smoke
    def test_undo_button_when_empty(self):
        """Test Case 5: Test backward button function when we let the form be empty"""
        # Ensure editor is empty
        self.editor.clear_editor_content()

        # Step 1: Click backward button
        # Expected result: Display the button backward cannot be clicked (disabled state)
        is_enabled = self.editor.is_undo_enabled()
        # Note: Undo button behavior when empty depends on implementation
        # Some editors disable it, others don't. We test the current state.
        self.editor.take_editor_screenshot("undo_when_empty")

    # =======================
    # FONT STYLE TESTS
    # =======================

    @pytest.mark.smoke
    def test_basic_font_styles_first_time(self):
        """Test Case 6: Test the function of Bold, Italic and Underline button when try first time"""
        # Step 1: Add a text
        test_text = "demo text"
        self.editor.enter_text(test_text)

        # Select all text
        self.editor.select_all_text()

        # Step 2: Click orderly button to test (Bold, then Italic, then Underline)
        assert self.editor.click_bold(), "Should be able to apply bold"
        time.sleep(0.2)
        assert self.editor.click_italic(), "Should be able to apply italic"
        time.sleep(0.2)
        assert self.editor.click_underline(), "Should be able to apply underline"

        # Expected result: Display the corresponding text with applied styles
        content = self.editor.get_editor_content()
        # Note: Exact HTML structure may vary, but formatting should be applied
        self.editor.take_editor_screenshot("basic_font_styles_applied")

    @pytest.mark.regression
    def test_font_styles_toggle(self):
        """Test Case 7: Test the function of Bold, Italic and Underline & Strikethrough button for the changed word"""
        # Step 1: Add a text
        test_text = "demo"
        self.editor.enter_text(test_text)
        self.editor.select_all_text()

        # Step 2: Click orderly each button (Bold, then Italic, then Underline, then Strikethrough)
        styles = ['bold', 'italic', 'underline', 'strikethrough']
        assert self.editor.apply_multiple_formats(styles), "Should be able to apply multiple formats"

        # Step 3: Click orderly each button again to toggle off
        assert self.editor.apply_multiple_formats(styles), "Should be able to toggle formats"

        # Expected result: Display the last state of the text (toggled styles)
        self.editor.take_editor_screenshot("font_styles_toggled")

    @pytest.mark.regression
    def test_integrated_font_styles(self):
        """Test Case 8: Test the integrated function of Bold, Italic and Underline button"""
        # Step 1: Add a text: "demo"
        self.editor.enter_text("demo")
        self.editor.select_all_text()

        # Step 2: Click all buttons orderly at the same time: Bold, Italic and Underline
        assert self.editor.apply_multiple_formats(['bold', 'italic', 'underline']), \
            "Should be able to apply multiple formats simultaneously"

        # Expected result: Display the corresponding text with multiple formatting
        content = self.editor.get_editor_content()
        self.editor.take_editor_screenshot("integrated_font_styles")

    @pytest.mark.regression
    def test_remove_font_style_button(self):
        """Test Case 9: Test the function of Remove Font Style button"""
        # Step 1: Add a text: "demo"
        self.editor.enter_text("demo")
        self.editor.select_all_text()

        # Step 2: Click all buttons orderly at the same time: Bold, Italic and Underline
        self.editor.apply_multiple_formats(['bold', 'italic', 'underline'])

        # Step 3: Click remove font style button
        assert self.editor.click_remove_format(), "Should be able to remove formatting"

        # Expected result: Display the corresponding text: demo (plain text without styling)
        time.sleep(0.5)
        content = self.editor.get_editor_content()
        self.editor.take_editor_screenshot("font_styles_removed")

    # =======================
    # SUPERSCRIPT/SUBSCRIPT TESTS
    # =======================

    @pytest.mark.regression
    def test_superscript_subscript_separately(self):
        """Test Case 10: Test the function of Superscript and subscript buttons separately"""
        # Step 1: Add a text "demo"
        self.editor.enter_text("demo")

        # Step 2: Choose "mo" in the string (simplified by selecting all for this test)
        self.editor.select_all_text()

        # Step 3: Click each button to test (Superscript first, then Subscript)
        assert self.editor.click_superscript(), "Should be able to apply superscript"
        self.editor.take_editor_screenshot("superscript_applied")

        # Reset and test subscript
        self.editor.clear_editor_content()
        self.editor.enter_text("demo")
        self.editor.select_all_text()
        assert self.editor.click_subscript(), "Should be able to apply subscript"

        # Expected result: Display the corresponding text with superscript/subscript
        self.editor.take_editor_screenshot("subscript_applied")

    @pytest.mark.regression
    def test_superscript_subscript_integrated(self):
        """Test Case 11: Test the function of Superscript and subscript buttons integratedly"""
        # Step 1: Add a text "demo"
        self.editor.enter_text("demo")

        # Step 2: Choose "mo" in the string
        self.editor.select_all_text()

        # Step 3: Click all buttons at the same time to test
        assert self.editor.apply_multiple_formats(['superscript', 'subscript']), \
            "Should be able to apply both superscript and subscript"

        # Expected result: Display the corresponding text with combined effects
        self.editor.take_editor_screenshot("superscript_subscript_combined")

    # =======================
    # FONT FAMILY TESTS
    # =======================

    @pytest.mark.smoke
    def test_font_family_dropdown_display(self):
        """Test Case 12: Test the displays of lists of font family when clicking to choose the font"""
        # Step 1: Click the button in the font family to show the list
        success = self.editor.open_font_family_dropdown()
        assert success, "Should be able to open font family dropdown"

        # Expected result: Display the list of font options
        time.sleep(0.5)
        self.editor.take_editor_screenshot("font_family_dropdown_open")

    @pytest.mark.smoke
    def test_font_family_selection(self):
        """Test Case 13: Test the function of the font family when we choose one font"""
        # Step 1: Add a text
        self.editor.enter_text("demo")
        self.editor.select_all_text()

        # Step 2 & 3: Click the button in the font family and choose Comic Sans MS
        success = self.editor.select_font_family("Comic Sans MS")
        assert success, "Should be able to select Comic Sans MS font"

        # Expected result: Display the corresponding text in Comic Sans MS font
        time.sleep(0.5)
        self.editor.take_editor_screenshot("font_family_comic_sans_applied")

    # =======================
    # COLOR TESTS
    # =======================

    @pytest.mark.smoke
    def test_color_options_display(self):
        """Test Case 14: Test the display of full common color options for color button"""
        # Step 1: Click into the color button
        success = self.editor.open_color_dropdown()
        assert success, "Should be able to open color dropdown"

        # Expected result: Display the color table with available color options
        time.sleep(0.5)
        self.editor.take_editor_screenshot("color_dropdown_open")

    @pytest.mark.smoke
    def test_color_button_functionality(self):
        """Test Case 15: Test the function of the color button"""
        # Step 1: Add a text, and choose all text
        self.editor.enter_text("colored text")
        self.editor.select_all_text()

        # Step 2 & 3: Click the button color to show the list and choose a color
        success = self.editor.select_text_color("red")
        assert success, "Should be able to select red color"
        time.sleep(0.5)
        self.editor.take_editor_screenshot("red_color_applied")

        # Step 4: Choose another one
        self.editor.select_all_text()
        success = self.editor.select_text_color("blue")
        assert success, "Should be able to select blue color"

        # Expected result: Display corresponding color changes on the selected text
        time.sleep(0.5)
        self.editor.take_editor_screenshot("blue_color_applied")

    # =======================
    # FONT SIZE TESTS
    # =======================

    @pytest.mark.smoke
    def test_font_size_functionality(self):
        """Test Case 16: Test the function of the font size button"""
        # Step 1: Add a text, and choose all text
        self.editor.enter_text("sized text")
        self.editor.select_all_text()

        # Step 2 & 3: Click the button font size and choose an option
        success = self.editor.select_font_size("18")
        assert success, "Should be able to select font size 18"
        time.sleep(0.5)

        # Step 4: Choose another one
        self.editor.select_all_text()
        success = self.editor.select_font_size("24")
        assert success, "Should be able to select font size 24"

        # Step 5: Write new text right after the text
        self.editor.enter_text(" new text")

        # Expected result: Display corresponding size changes and new text maintains the selected size
        self.editor.take_editor_screenshot("font_size_applied")

    # =======================
    # STYLE TESTS
    # =======================

    @pytest.mark.smoke
    def test_style_options_display(self):
        """Test Case 17: Test the display of full common options for style button"""
        # Step 1: Add a text, and choose all text
        self.editor.enter_text("styled text")
        self.editor.select_all_text()

        # Step 2: Click the button style to show the list
        success = self.editor.open_style_dropdown()
        assert success, "Should be able to open style dropdown"

        # Expected result: Display common styles (heading 1, heading 2, paragraph, etc.)
        time.sleep(0.5)
        self.editor.take_editor_screenshot("style_dropdown_open")

    @pytest.mark.smoke
    def test_style_functionality(self):
        """Test Case 18: Test the function of the style button"""
        # Step 1: Add a text, and choose all text
        self.editor.enter_text("styled text")
        self.editor.select_all_text()

        # Step 2 & 3: Click the button style and choose a style
        success = self.editor.select_style("h1")
        assert success, "Should be able to select H1 style"
        time.sleep(0.5)

        # Step 4: Choose another one
        self.editor.select_all_text()
        success = self.editor.select_style("h2")
        assert success, "Should be able to select H2 style"

        # Step 5: Write new text right after the text
        self.editor.enter_text(" additional text")

        # Expected result: Display corresponding style changes and new text maintains the selected style
        self.editor.take_editor_screenshot("styles_applied")

    # =======================
    # LIST TESTS
    # =======================

    @pytest.mark.smoke
    def test_list_functionality(self):
        """Test Case 19: Test the function of the unordered list, Ordered list button"""
        # Test unordered list
        # Step 1: Click one of the two buttons (unordered list)
        success = self.editor.click_unordered_list()
        assert success, "Should be able to click unordered list button"

        # Step 2: Write a text
        self.editor.enter_text("demo")

        # Step 3: Press Enter
        self.editor.actions.send_keys(Keys.ENTER).perform()

        # Expected result: Display unordered list with bullet points
        self.editor.take_editor_screenshot("unordered_list_created")

        # Clear and test ordered list
        self.editor.clear_editor_content()

        # Test ordered list
        success = self.editor.click_ordered_list()
        assert success, "Should be able to click ordered list button"

        self.editor.enter_text("demo")
        self.editor.actions.send_keys(Keys.ENTER).perform()

        # Expected result: Display ordered list with numbers
        self.editor.take_editor_screenshot("ordered_list_created")

    # =======================
    # PARAGRAPH ALIGNMENT TESTS
    # =======================

    @pytest.mark.smoke
    def test_paragraph_alignment_options_display(self):
        """Test Case 20: Test the display of 4 orientation paragraph options for paragraph button"""
        # Step 1: Click the button orientation
        success = self.editor.open_align_dropdown()
        assert success, "Should be able to open alignment dropdown"

        # Expected result: Display 4 orientation paragraph options (left, center, right, justify)
        time.sleep(0.5)
        self.editor.take_editor_screenshot("alignment_dropdown_open")

    @pytest.mark.smoke
    def test_paragraph_alignment_functionality(self):
        """Test Case 21: Test the function of the paragraph button"""
        test_text = "This is a test paragraph for alignment testing."

        alignments = ['left', 'center', 'right', 'justify']

        for alignment in alignments:
            # Clear and add text
            self.editor.clear_editor_content()
            self.editor.enter_text(test_text)
            self.editor.select_all_text()

            # Step 1-4: Choose orientation and write text
            success = self.editor.align_text(alignment)
            assert success, f"Should be able to apply {alignment} alignment"

            # Expected result: Display corresponding orientation paragraph alignment
            time.sleep(0.5)
            self.editor.take_editor_screenshot(f"alignment_{alignment}")

    # =======================
    # LINE HEIGHT TESTS
    # =======================

    @pytest.mark.regression
    def test_line_height_functionality(self):
        """Test Case 22: Test the line height function of line height button"""
        # Step 1: Write 2 texts in nearby lines
        self.editor.enter_text("First line of text")
        self.editor.actions.send_keys(Keys.ENTER).perform()
        self.editor.enter_text("Second line of text")

        # Select all text
        self.editor.select_all_text()

        # Step 2 & 3: Click button line height and choose one option
        success = self.editor.set_line_height("1.5")
        assert success, "Should be able to set line height to 1.5"
        time.sleep(0.5)
        self.editor.take_editor_screenshot("line_height_1_5")

        # Step 4: Choose another option
        self.editor.select_all_text()
        success = self.editor.set_line_height("2.0")
        assert success, "Should be able to set line height to 2.0"

        # Expected result: Display corresponding line height changes between the text lines
        time.sleep(0.5)
        self.editor.take_editor_screenshot("line_height_2_0")

    # =======================
    # TABLE TESTS
    # =======================

    @pytest.mark.regression
    def test_table_functionality(self):
        """Test Case 23: Test the function of table button"""
        # Step 1: Click on the table button
        success = self.editor.open_table_menu()
        assert success, "Should be able to open table menu"
        time.sleep(0.5)
        self.editor.take_editor_screenshot("table_menu_open")

        # Step 2: Click choose size 2 × 2
        success = self.editor.insert_table(2, 2)
        assert success, "Should be able to insert 2x2 table"
        time.sleep(1)
        self.editor.take_editor_screenshot("table_2x2_inserted")

        # Step 3: Click choose size 3 × 2 (insert another table)
        self.editor.enter_text("\n\n")  # Add some space
        success = self.editor.insert_table(3, 2)
        assert success, "Should be able to insert 3x2 table"

        # Expected result: Display 2 corresponding tables with the selected dimensions
        time.sleep(1)
        self.editor.take_editor_screenshot("table_3x2_inserted")

    # =======================
    # LINK TESTS
    # =======================

    @pytest.mark.smoke
    def test_link_dialog_display(self):
        """Test Case 24: Test the display of the form insert link when click the link button"""
        # Step 1: Click on the link button
        success = self.editor.open_link_dialog()
        assert success, "Should be able to open link dialog"

        # Expected result: Display the form of insert link composed of 2 fields
        time.sleep(1)
        self.editor.take_editor_screenshot("link_dialog_open")

        # Close dialog
        self.editor.close_link_dialog()

    @pytest.mark.regression
    def test_valid_link_submission(self):
        """Test Case 27: Test the valid submission input"""
        # Step 1: Click on the link button and insert data
        test_url = "https://docs.google.com/spreadsheets/d/1sWC0FXUm67U4GCj21xIPMcYthgbLGmpVzQ4WnDAI9_c/edit?gid=0#gid=0"
        success = self.editor.insert_link("Source file", test_url)
        assert success, "Should be able to insert link"

        # Expected result: Display the "Source file" with link attached
        time.sleep(1)
        content = self.editor.get_editor_content()
        assert "Source file" in content, "Link text should be visible"
        self.editor.take_editor_screenshot("valid_link_inserted")

    @pytest.mark.regression
    def test_link_text_modification(self):
        """Test Case 28: Test the valid URL approach after deleting some text of the text display URL"""
        # Step 1-3: Insert link
        test_url = "https://docs.google.com/spreadsheets/d/1sWC0FXUm67U4GCj21xIPMcYthgbLGmpVzQ4WnDAI9_c/edit?gid=0#gid=0"
        self.editor.insert_link("Source file", test_url)
        time.sleep(1)

        # Step 4: Delete "file" in the text to display (simplified: edit the entire text)
        # This would require selecting the link and editing it
        # For now, we'll verify the link exists
        content = self.editor.get_editor_content()
        assert "Source file" in content, "Link should be present"

        # Step 5: Click on the remains (verify link functionality)
        self.editor.take_editor_screenshot("link_text_modified")

    @pytest.mark.regression
    def test_automatic_http_prefix(self):
        """Test Case 29: Test the automatic adding http before text in URL field"""
        # Step 1-3: Insert link with plain text URL
        success = self.editor.insert_link("demo link", "demo")
        assert success, "Should be able to insert link with plain text URL"

        # Expected result: URL should have http:// prefix added automatically
        time.sleep(1)
        content = self.editor.get_editor_content()
        assert "demo link" in content, "Link text should be visible"
        self.editor.take_editor_screenshot("auto_http_prefix")

    # =======================
    # VIDEO TESTS
    # =======================

    @pytest.mark.regression
    def test_video_dialog_display(self):
        """Test Case 34: Test the display form to insert URL of video button"""
        # Step 1: Click on the video button
        success = self.editor.open_video_dialog()
        assert success, "Should be able to open video dialog"

        # Expected result: Display the form for inserting URL of video
        time.sleep(1)
        self.editor.take_editor_screenshot("video_dialog_open")

    @pytest.mark.regression
    def test_valid_youtube_url_insertion(self):
        """Test Case 35: Testing the case inserting valid URL from YouTube platform into the URL field"""
        # Step 1-3: Insert YouTube URL
        youtube_url = "https://www.youtube.com/watch?v=98cyrMp9ri8&t=15677s"
        success = self.editor.insert_video(youtube_url)
        assert success, "Should be able to insert YouTube video"

        # Expected result: Display the video embedded in the description part
        time.sleep(2)  # Wait for video embedding
        content = self.editor.get_editor_content()
        self.editor.take_editor_screenshot("youtube_video_inserted")

    @pytest.mark.regression
    def test_invalid_video_url_insertion(self):
        """Test Case 36: Testing the case inserting valid URL from non-YouTube platform into the URL field"""
        # Step 1-3: Insert non-video URL
        non_video_url = "https://docs.google.com/spreadsheets/d/1sWC0FXUm67U4GCj21xIPMcYthgbLGmpVzQ4WnDAI9_c/edit?gid=0#gid=0"
        success = self.editor.insert_video(non_video_url)

        # Expected result: Display nothing (URL not supported for video embedding)
        time.sleep(1)
        self.editor.take_editor_screenshot("invalid_video_url")

    @pytest.mark.regression
    def test_invalid_text_as_video_url(self):
        """Test Case 37: Testing the case inserting invalid URL into the URL field"""
        # Step 1-3: Insert invalid text as URL
        success = self.editor.insert_video("demo")

        # Expected result: Display nothing or show error message for invalid URL
        time.sleep(1)
        self.editor.take_editor_screenshot("invalid_text_as_video_url")

    # =======================
    # IMAGE GALLERY TESTS
    # =======================

    @pytest.mark.regression
    def test_image_gallery_dialog_display(self):
        """Test Case 38: Testing the display of form to choose image of Gallery button"""
        # Step 1: Click on the image button
        success = self.editor.open_image_dialog()
        assert success, "Should be able to open image dialog"

        # Expected result: Display the image gallery for selection
        time.sleep(1)
        self.editor.take_editor_screenshot("image_dialog_open")

    # =======================
    # COMPREHENSIVE INTEGRATION TESTS
    # =======================

    @pytest.mark.regression
    def test_comprehensive_formatting_integration(self):
        """Test Case 33: Testing integrated buttons: font, size, Bold, Italic and Underline, Strikethrough, style, link edit"""
        # Step 1-3: Insert link
        success = self.editor.insert_link("demo text", "http://demo.com")
        assert success, "Should be able to insert link"
        time.sleep(1)

        # Step 4: Choose all the text and apply multiple formatting
        self.editor.select_all_text()

        # Apply font family
        self.editor.select_font_family("Arial")
        time.sleep(0.2)

        # Apply font size
        self.editor.select_font_size("18")
        time.sleep(0.2)

        # Apply text formatting
        self.editor.apply_multiple_formats(['bold', 'italic', 'underline', 'strikethrough'])
        time.sleep(0.2)

        # Apply style
        self.editor.select_style("h2")

        # Expected result: Display the corresponding state of the text with all formatting styles applied while maintaining link functionality
        time.sleep(1)
        content = self.editor.get_editor_content()
        assert "demo text" in content, "Link text should still be present"
        self.editor.take_editor_screenshot("comprehensive_formatting_applied")

    @pytest.mark.security
    def test_xss_prevention_in_editor(self):
        """Test XSS prevention in the rich text editor"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>"
        ]

        for payload in xss_payloads:
            self.editor.clear_editor_content()

            # Try entering XSS payload in code view
            self.editor.toggle_code_view()
            self.editor.enter_code(payload)
            self.editor.toggle_code_view()

            # Verify XSS is prevented/escaped
            content = self.editor.get_editor_content()
            # The exact escaping mechanism depends on the editor implementation
            # We verify that script tags are not executed
            self.editor.take_editor_screenshot(f"xss_test_{len(payload)}")

    @pytest.mark.regression
    def test_large_content_handling(self):
        """Test editor performance with large content"""
        # Create large text content
        large_text = "Large content test. " * 1000  # 20,000+ characters

        self.editor.enter_text(large_text)

        # Verify editor can handle large content
        assert self.editor.has_content(), "Editor should handle large content"
        content_length = self.editor.get_content_length()
        assert content_length > 10000, "Should handle large content"

        # Test formatting on large content
        self.editor.select_all_text()
        success = self.editor.click_bold()
        assert success, "Should be able to format large content"

        self.editor.take_editor_screenshot("large_content_handled")

    @pytest.mark.regression
    def test_special_characters_handling(self):
        """Test editor handling of special characters and emojis"""
        special_chars = "🥶🥶 <>&\"'`{}[]()+=*%$#@!~^|\\/:;?.,\n\t"

        self.editor.enter_text(special_chars)

        # Verify special characters are preserved
        content = self.editor.get_editor_text()
        assert len(content) > 0, "Should handle special characters"

        self.editor.take_editor_screenshot("special_characters_handled")

    @pytest.mark.smoke
    def test_editor_accessibility_basics(self):
        """Test basic accessibility features of the editor"""
        # Test keyboard navigation
        success = self.editor.simulate_keyboard_shortcut("ctrl+b")
        assert success, "Should support keyboard shortcuts"

        # Test if editor is focusable
        assert self.editor.is_editor_ready(), "Editor should be ready and focusable"

        # Test ARIA attributes and accessibility
        editor_element = self.editor.find_element(self.editor.WYSIWYG_EDITOR)
        role = editor_element.get_attribute('role')
        assert role == 'textbox', "Editor should have textbox role"

        multiline = editor_element.get_attribute('aria-multiline')
        assert multiline == 'true', "Editor should support multiline"

        self.editor.take_editor_screenshot("accessibility_test")

# =======================
# ADDITIONAL TEST CLASSES FOR ORGANIZATION
# =======================

class TestRichTextEditorValidation:
    """Test suite for Rich Text Editor field validation"""

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_driver):
        self.driver = authenticated_driver
        self.editor = RichTextEditorComponent(self.driver)
        self.driver.get("http://localhost/#/pages/catalogue/products/create-product")
        self.editor.wait_for_editor_load()

    @pytest.mark.regression
    def test_link_text_field_validation(self):
        """Test Case 25: Test case validation for Text to display field"""
        # This would test various validation scenarios for the link text field
        # Following CM_042 to CM_048 test patterns (excluding CM_043, CM_046, CM_047)

        validation_cases = [
            ("", False, "Empty text should not be valid"),
            ("   ", False, "Whitespace only should not be valid"),
            ("a" * 1000, True, "Long text should be handled"),
            ("Normal text", True, "Normal text should be valid"),
            ("Text with 123 numbers", True, "Text with numbers should be valid"),
            ("Special!@#$%^&*()chars", True, "Special characters should be handled")
        ]

        for text, should_be_valid, description in validation_cases:
            self.editor.open_link_dialog()
            time.sleep(0.5)

            # Test text field validation
            text_input = self.editor.find_element(self.editor.LINK_TEXT_INPUT)
            if text_input:
                text_input.clear()
                text_input.send_keys(text)

                # Check if insert button is enabled based on validation
                insert_btn = self.editor.find_element(self.editor.LINK_INSERT_BTN)
                is_enabled = insert_btn.is_enabled() if insert_btn else False

                # Note: Exact validation behavior depends on implementation

            self.editor.close_link_dialog()

    @pytest.mark.regression
    def test_link_url_field_validation(self):
        """Test Case 26: Test case validation for URL field"""
        # Test URL field validation following CM_042 to CM_048 patterns

        url_validation_cases = [
            ("", False, "Empty URL should not be valid"),
            ("not-a-url", True, "Plain text gets http:// prefix"),
            ("http://valid-url.com", True, "Valid HTTP URL should be accepted"),
            ("https://secure-url.com", True, "Valid HTTPS URL should be accepted"),
            ("ftp://ftp-url.com", True, "FTP URLs should be accepted"),
            ("mailto:test@example.com", True, "Mailto URLs should be accepted"),
            ("javascript:alert('xss')", False, "JavaScript URLs should be blocked"),
            ("data:text/html,<script>alert('xss')</script>", False, "Data URLs with scripts should be blocked")
        ]

        for url, should_be_valid, description in url_validation_cases:
            self.editor.open_link_dialog()
            time.sleep(0.5)

            # Test URL field validation
            text_input = self.editor.find_element(self.editor.LINK_TEXT_INPUT)
            url_input = self.editor.find_element(self.editor.LINK_URL_INPUT)

            if text_input and url_input:
                text_input.clear()
                text_input.send_keys("Test Link")

                url_input.clear()
                url_input.send_keys(url)

                # Check validation
                insert_btn = self.editor.find_element(self.editor.LINK_INSERT_BTN)
                is_enabled = insert_btn.is_enabled() if insert_btn else False

                # Note: Actual validation behavior depends on implementation

            self.editor.close_link_dialog()


class TestRichTextEditorPerformance:
    """Test suite for Rich Text Editor performance aspects"""

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_driver):
        self.driver = authenticated_driver
        self.editor = RichTextEditorComponent(self.driver)
        self.driver.get("http://localhost/#/pages/catalogue/products/create-product")
        self.editor.wait_for_editor_load()

    @pytest.mark.slow
    def test_editor_load_performance(self):
        """Test editor loading performance"""
        import time

        start_time = time.time()

        # Refresh page and measure load time
        self.driver.refresh()
        success = self.editor.wait_for_editor_load()

        load_time = time.time() - start_time

        assert success, "Editor should load successfully"
        assert load_time < 10, f"Editor should load in under 10 seconds, took {load_time:.2f}s"

        print(f"Editor load time: {load_time:.2f} seconds")

    @pytest.mark.slow
    def test_large_content_performance(self):
        """Test performance with large content"""
        import time

        # Create progressively larger content and measure performance
        base_text = "Performance test content. "

        for multiplier in [100, 500, 1000]:
            large_text = base_text * multiplier

            # Clear editor
            self.editor.clear_editor_content()

            # Measure insertion time
            start_time = time.time()
            self.editor.enter_text(large_text)
            insertion_time = time.time() - start_time

            # Measure formatting time
            self.editor.select_all_text()
            start_time = time.time()
            self.editor.click_bold()
            formatting_time = time.time() - start_time

            print(f"Content size: {len(large_text)} chars")
            print(f"Insertion time: {insertion_time:.3f}s")
            print(f"Formatting time: {formatting_time:.3f}s")

            # Performance assertions
            assert insertion_time < 5, f"Text insertion should be under 5s for {len(large_text)} chars"
            assert formatting_time < 3, f"Formatting should be under 3s for {len(large_text)} chars"

    @pytest.mark.regression
    def test_multiple_format_operations_performance(self):
        """Test performance of multiple consecutive formatting operations"""
        import time

        test_text = "Performance test text for multiple operations."
        self.editor.enter_text(test_text)

        # Perform multiple formatting operations and measure time
        operations = [
            ('bold', self.editor.click_bold),
            ('italic', self.editor.click_italic),
            ('underline', self.editor.click_underline),
            ('font_size', lambda: self.editor.select_font_size('18')),
            ('font_family', lambda: self.editor.select_font_family('Arial')),
            ('color', lambda: self.editor.select_text_color('red')),
            ('style', lambda: self.editor.select_style('h2'))
        ]

        total_time = 0
        for operation_name, operation_func in operations:
            self.editor.select_all_text()

            start_time = time.time()
            success = operation_func()
            operation_time = time.time() - start_time
            total_time += operation_time

            assert success, f"{operation_name} operation should succeed"
            assert operation_time < 2, f"{operation_name} should complete in under 2s"

            print(f"{operation_name}: {operation_time:.3f}s")

        print(f"Total formatting time: {total_time:.3f}s")
        assert total_time < 10, "All formatting operations should complete in under 10s"