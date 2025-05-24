from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
import time

class RichTextEditorComponent(BasePage):
    """Page Object Model for Rich Text Editor (Summernote) Component"""

    # =======================
    # MAIN CONTAINER LOCATORS
    # =======================

    # Main editor container
    EDITOR_CONTAINER = (By.CSS_SELECTOR, ".note-editor.note-frame")
    EDITOR_CARD = (By.CSS_SELECTOR, "nb-card.nb-card.inline-form-card")
    CARD_HEADER = (By.CSS_SELECTOR, "nb-card-header.nb-card-header")

    # =======================
    # TOOLBAR BUTTON LOCATORS
    # =======================

    # Code view and basic controls
    CODE_VIEW_BTN = (By.CSS_SELECTOR, ".note-btn.btn-codeview")
    UNDO_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label*='Undo']")
    REDO_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label*='Redo']")

    # Text formatting buttons
    BOLD_BTN = (By.CSS_SELECTOR, ".note-btn.note-btn-bold")
    ITALIC_BTN = (By.CSS_SELECTOR, ".note-btn.note-btn-italic")
    UNDERLINE_BTN = (By.CSS_SELECTOR, ".note-btn.note-btn-underline")
    STRIKETHROUGH_BTN = (By.CSS_SELECTOR, ".note-btn.note-btn-strikethrough")
    SUPERSCRIPT_BTN = (By.CSS_SELECTOR, ".note-btn.note-btn-superscript")
    SUBSCRIPT_BTN = (By.CSS_SELECTOR, ".note-btn.note-btn-subscript")
    REMOVE_FORMAT_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label*='Remove Font Style']")

    # Font controls
    FONT_FAMILY_DROPDOWN = (By.CSS_SELECTOR, ".note-btn.dropdown-toggle[aria-label='Font Family']")
    FONT_SIZE_DROPDOWN = (By.CSS_SELECTOR, ".note-btn.dropdown-toggle[aria-label='Font Size']")
    COLOR_BTN = (By.CSS_SELECTOR, ".note-current-color-button")
    COLOR_DROPDOWN = (By.CSS_SELECTOR, ".note-btn.dropdown-toggle[aria-label='More Color']")

    # Style and paragraph controls
    STYLE_DROPDOWN = (By.CSS_SELECTOR, ".note-btn.dropdown-toggle[aria-label='Style']")
    UNORDERED_LIST_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label*='Unordered list']")
    ORDERED_LIST_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label*='Ordered list']")
    ALIGN_DROPDOWN = (By.CSS_SELECTOR, ".note-btn.dropdown-toggle[aria-label='Paragraph']")
    LINE_HEIGHT_DROPDOWN = (By.CSS_SELECTOR, ".note-btn.dropdown-toggle[aria-label='Line Height']")

    # Insert controls
    TABLE_BTN = (By.CSS_SELECTOR, ".note-btn.dropdown-toggle[aria-label='Table']")
    LINK_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label*='Link']")
    VIDEO_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label='Video']")
    HR_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label*='Horizontal Rule']")
    GALLERY_BTN = (By.CSS_SELECTOR, ".note-btn[aria-label='Gallery']")

    # =======================
    # EDITOR AREA LOCATORS
    # =======================

    # Main editing areas
    WYSIWYG_EDITOR = (By.CSS_SELECTOR, ".note-editable[contenteditable='true']")
    CODE_EDITOR = (By.CSS_SELECTOR, ".note-codable")
    EDITOR_STATUS = (By.CSS_SELECTOR, ".note-status-output")

    # =======================
    # DROPDOWN MENU LOCATORS
    # =======================

    # Font family options
    FONT_HELVETICA = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='Helvetica']")
    FONT_ARIAL = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='Arial']")
    FONT_COMIC_SANS = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='Comic Sans MS']")
    FONT_TIMES = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='Times']")

    # Font size options
    FONT_SIZE_8 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='8']")
    FONT_SIZE_12 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='12']")
    FONT_SIZE_18 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='18']")
    FONT_SIZE_24 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='24']")

    # Style options
    STYLE_NORMAL = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='p']")
    STYLE_H1 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='h1']")
    STYLE_H2 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='h2']")
    STYLE_H3 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='h3']")
    STYLE_QUOTE = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='blockquote']")
    STYLE_CODE = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='pre']")

    # Color palette
    COLOR_RED = (By.CSS_SELECTOR, ".note-color-btn[data-value='#FF0000']")
    COLOR_BLUE = (By.CSS_SELECTOR, ".note-color-btn[data-value='#0000FF']")
    COLOR_GREEN = (By.CSS_SELECTOR, ".note-color-btn[data-value='#00FF00']")
    COLOR_YELLOW = (By.CSS_SELECTOR, ".note-color-btn[data-value='#FFFF00']")

    # Alignment options
    ALIGN_LEFT = (By.CSS_SELECTOR, ".note-btn[aria-label*='Align left']")
    ALIGN_CENTER = (By.CSS_SELECTOR, ".note-btn[aria-label*='Align center']")
    ALIGN_RIGHT = (By.CSS_SELECTOR, ".note-btn[aria-label*='Align right']")
    ALIGN_JUSTIFY = (By.CSS_SELECTOR, ".note-btn[aria-label*='Justify']")

    # Line height options
    LINE_HEIGHT_1_0 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='1.0']")
    LINE_HEIGHT_1_5 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='1.5']")
    LINE_HEIGHT_2_0 = (By.CSS_SELECTOR, ".note-dropdown-item[data-value='2.0']")

    # =======================
    # MODAL DIALOG LOCATORS
    # =======================

    # Link dialog
    LINK_DIALOG = (By.CSS_SELECTOR, ".note-modal.link-dialog")
    LINK_TEXT_INPUT = (By.CSS_SELECTOR, ".note-link-text")
    LINK_URL_INPUT = (By.CSS_SELECTOR, ".note-link-url")
    LINK_NEW_WINDOW_CHECKBOX = (By.CSS_SELECTOR, ".sn-checkbox-open-in-new-window input")
    LINK_INSERT_BTN = (By.CSS_SELECTOR, ".note-link-btn")
    LINK_CLOSE_BTN = (By.CSS_SELECTOR, ".note-modal .close")

    # Video dialog
    VIDEO_DIALOG = (By.CSS_SELECTOR, ".note-modal[aria-label='Insert Video']")
    VIDEO_URL_INPUT = (By.CSS_SELECTOR, ".note-video-url")
    VIDEO_INSERT_BTN = (By.CSS_SELECTOR, ".note-video-btn")

    # Image dialog
    IMAGE_DIALOG = (By.CSS_SELECTOR, ".note-modal[aria-label='Insert Image']")
    IMAGE_FILE_INPUT = (By.CSS_SELECTOR, ".note-image-input")
    IMAGE_URL_INPUT = (By.CSS_SELECTOR, ".note-image-url")
    IMAGE_INSERT_BTN = (By.CSS_SELECTOR, ".note-image-btn")

    # Table dimension picker
    TABLE_DIMENSION_PICKER = (By.CSS_SELECTOR, ".note-dimension-picker-mousecatcher")
    TABLE_DIMENSION_DISPLAY = (By.CSS_SELECTOR, ".note-dimension-display")

    # =======================
    # POPOVER LOCATORS
    # =======================

    # Link popover (appears when clicking on links)
    LINK_POPOVER = (By.CSS_SELECTOR, ".note-link-popover")
    LINK_EDIT_BTN = (By.CSS_SELECTOR, ".note-link-popover .note-btn[aria-label='Edit']")
    LINK_UNLINK_BTN = (By.CSS_SELECTOR, ".note-link-popover .note-btn[aria-label='Unlink']")

    # Image popover
    IMAGE_POPOVER = (By.CSS_SELECTOR, ".note-image-popover")
    IMAGE_RESIZE_100 = (By.CSS_SELECTOR, ".note-resize .note-btn:first-child")
    IMAGE_RESIZE_50 = (By.CSS_SELECTOR, ".note-resize .note-btn:nth-child(2)")
    IMAGE_FLOAT_LEFT = (By.CSS_SELECTOR, ".note-float .note-btn[aria-label='Float Left']")
    IMAGE_REMOVE = (By.CSS_SELECTOR, ".note-remove .note-btn")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)

    # =======================
    # NAVIGATION & SETUP METHODS
    # =======================

    def wait_for_editor_load(self):
        """Wait for the rich text editor to fully load"""
        try:
            self.wait.until(EC.presence_of_element_located(self.EDITOR_CONTAINER))
            self.wait.until(EC.presence_of_element_located(self.WYSIWYG_EDITOR))
            time.sleep(1)  # Additional wait for toolbar to be ready
            return True
        except TimeoutException:
            print("❌ Rich text editor did not load within timeout")
            return False

    def is_editor_ready(self):
        """Check if the editor is ready for interaction"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            return editor is not None and editor.is_enabled()
        except:
            return False

    def get_editor_title(self):
        """Get the editor card title"""
        try:
            header = self.find_element(self.CARD_HEADER)
            return header.text if header else ""
        except:
            return ""

    # =======================
    # TEXT INPUT METHODS
    # =======================

    def clear_editor_content(self):
        """Clear all content from the editor"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            if editor:
                editor.clear()
                # Alternative method using keyboard shortcut
                self.actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                self.actions.send_keys(Keys.DELETE).perform()
                return True
        except Exception as e:
            print(f"Failed to clear editor: {str(e)}")
            return False

    def enter_text(self, text):
        """Enter text into the editor"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            if editor:
                editor.click()  # Focus the editor
                editor.send_keys(text)
                return True
        except Exception as e:
            print(f"Failed to enter text: {str(e)}")
            return False

    def get_editor_content(self):
        """Get the current content of the editor"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            return editor.get_attribute('innerHTML') if editor else ""
        except:
            return ""

    def get_editor_text(self):
        """Get the plain text content of the editor"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            return editor.text if editor else ""
        except:
            return ""

    def select_all_text(self):
        """Select all text in the editor"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            if editor:
                editor.click()
                self.actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
                return True
        except:
            return False

    def select_text_range(self, start_text, end_text):
        """Select a range of text (simplified version)"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            if editor:
                # This is a simplified implementation
                # In practice, you'd need more complex logic for precise text selection
                editor.click()
                # Use JavaScript to select text range
                script = f"""
                var editor = arguments[0];
                var text = editor.textContent;
                var startIndex = text.indexOf('{start_text}');
                var endIndex = text.indexOf('{end_text}') + '{end_text}'.length;
                
                if (startIndex !== -1 && endIndex !== -1) {{
                    var range = document.createRange();
                    var textNode = editor.childNodes[0];
                    range.setStart(textNode, startIndex);
                    range.setEnd(textNode, endIndex);
                    
                    var selection = window.getSelection();
                    selection.removeAllRanges();
                    selection.addRange(range);
                    return true;
                }}
                return false;
                """
                return self.driver.execute_script(script, editor)
        except:
            return False

    # =======================
    # CODE VIEW METHODS
    # =======================

    def toggle_code_view(self):
        """Toggle between WYSIWYG and code view"""
        return self.click_element(self.CODE_VIEW_BTN)

    def is_in_code_view(self):
        """Check if currently in code view mode"""
        try:
            code_editor = self.find_element(self.CODE_EDITOR)
            return code_editor.is_displayed() if code_editor else False
        except:
            return False

    def enter_code(self, code_text):
        """Enter code when in code view mode"""
        try:
            if self.is_in_code_view():
                code_editor = self.find_element(self.CODE_EDITOR)
                if code_editor:
                    code_editor.clear()
                    code_editor.send_keys(code_text)
                    return True
        except:
            return False

    def get_code_content(self):
        """Get the code content when in code view"""
        try:
            if self.is_in_code_view():
                code_editor = self.find_element(self.CODE_EDITOR)
                return code_editor.get_attribute('value') if code_editor else ""
        except:
            return ""

    # =======================
    # BASIC FORMATTING METHODS
    # =======================

    def click_bold(self):
        """Apply bold formatting"""
        return self.click_element(self.BOLD_BTN)

    def click_italic(self):
        """Apply italic formatting"""
        return self.click_element(self.ITALIC_BTN)

    def click_underline(self):
        """Apply underline formatting"""
        return self.click_element(self.UNDERLINE_BTN)

    def click_strikethrough(self):
        """Apply strikethrough formatting"""
        return self.click_element(self.STRIKETHROUGH_BTN)

    def click_superscript(self):
        """Apply superscript formatting"""
        return self.click_element(self.SUPERSCRIPT_BTN)

    def click_subscript(self):
        """Apply subscript formatting"""
        return self.click_element(self.SUBSCRIPT_BTN)

    def click_remove_format(self):
        """Remove all formatting"""
        return self.click_element(self.REMOVE_FORMAT_BTN)

    def apply_multiple_formats(self, formats):
        """Apply multiple formats at once
        Args:
            formats (list): List of format names ['bold', 'italic', 'underline']
        """
        format_methods = {
            'bold': self.click_bold,
            'italic': self.click_italic,
            'underline': self.click_underline,
            'strikethrough': self.click_strikethrough,
            'superscript': self.click_superscript,
            'subscript': self.click_subscript
        }

        success = True
        for format_name in formats:
            if format_name in format_methods:
                if not format_methods[format_name]():
                    success = False
            time.sleep(0.2)  # Small delay between actions

        return success

    # =======================
    # UNDO/REDO METHODS
    # =======================

    def click_undo(self):
        """Click undo button"""
        return self.click_element(self.UNDO_BTN)

    def click_redo(self):
        """Click redo button"""
        return self.click_element(self.REDO_BTN)

    def is_undo_enabled(self):
        """Check if undo button is enabled"""
        try:
            undo_btn = self.find_element(self.UNDO_BTN)
            return not undo_btn.get_attribute('disabled') if undo_btn else False
        except:
            return False

    def is_redo_enabled(self):
        """Check if redo button is enabled"""
        try:
            redo_btn = self.find_element(self.REDO_BTN)
            return not redo_btn.get_attribute('disabled') if redo_btn else False
        except:
            return False

    # =======================
    # FONT METHODS
    # =======================

    def open_font_family_dropdown(self):
        """Open font family dropdown"""
        return self.click_element(self.FONT_FAMILY_DROPDOWN)

    def select_font_family(self, font_name):
        """Select a specific font family"""
        font_locators = {
            'Helvetica': self.FONT_HELVETICA,
            'Arial': self.FONT_ARIAL,
            'Comic Sans MS': self.FONT_COMIC_SANS,
            'Times': self.FONT_TIMES
        }

        if self.open_font_family_dropdown():
            time.sleep(0.5)
            if font_name in font_locators:
                return self.click_element(font_locators[font_name])
        return False

    def open_font_size_dropdown(self):
        """Open font size dropdown"""
        return self.click_element(self.FONT_SIZE_DROPDOWN)

    def select_font_size(self, size):
        """Select a specific font size"""
        size_locators = {
            '8': self.FONT_SIZE_8,
            '12': self.FONT_SIZE_12,
            '18': self.FONT_SIZE_18,
            '24': self.FONT_SIZE_24
        }

        if self.open_font_size_dropdown():
            time.sleep(0.5)
            if str(size) in size_locators:
                return self.click_element(size_locators[str(size)])
        return False

    # =======================
    # COLOR METHODS
    # =======================

    def open_color_dropdown(self):
        """Open color dropdown"""
        return self.click_element(self.COLOR_DROPDOWN)

    def select_text_color(self, color_name):
        """Select text color"""
        color_locators = {
            'red': self.COLOR_RED,
            'blue': self.COLOR_BLUE,
            'green': self.COLOR_GREEN,
            'yellow': self.COLOR_YELLOW
        }

        if self.open_color_dropdown():
            time.sleep(0.5)
            if color_name.lower() in color_locators:
                return self.click_element(color_locators[color_name.lower()])
        return False

    def click_current_color(self):
        """Click current color button (applies last used color)"""
        return self.click_element(self.COLOR_BTN)

    # =======================
    # STYLE METHODS
    # =======================

    def open_style_dropdown(self):
        """Open style dropdown"""
        return self.click_element(self.STYLE_DROPDOWN)

    def select_style(self, style_name):
        """Select a specific style"""
        style_locators = {
            'normal': self.STYLE_NORMAL,
            'h1': self.STYLE_H1,
            'h2': self.STYLE_H2,
            'h3': self.STYLE_H3,
            'quote': self.STYLE_QUOTE,
            'code': self.STYLE_CODE
        }

        if self.open_style_dropdown():
            time.sleep(0.5)
            if style_name.lower() in style_locators:
                return self.click_element(style_locators[style_name.lower()])
        return False

    # =======================
    # LIST METHODS
    # =======================

    def click_unordered_list(self):
        """Create unordered list"""
        return self.click_element(self.UNORDERED_LIST_BTN)

    def click_ordered_list(self):
        """Create ordered list"""
        return self.click_element(self.ORDERED_LIST_BTN)

    def create_list_with_items(self, list_type, items):
        """Create a list with multiple items
        Args:
            list_type (str): 'ordered' or 'unordered'
            items (list): List of text items to add
        """
        try:
            # Click appropriate list button
            if list_type == 'ordered':
                self.click_ordered_list()
            else:
                self.click_unordered_list()

            # Add items
            for i, item in enumerate(items):
                if i > 0:
                    self.actions.send_keys(Keys.ENTER).perform()
                self.actions.send_keys(item).perform()

            return True
        except:
            return False

    # =======================
    # ALIGNMENT METHODS
    # =======================

    def open_align_dropdown(self):
        """Open alignment dropdown"""
        return self.click_element(self.ALIGN_DROPDOWN)

    def align_text(self, alignment):
        """Align text to specified alignment"""
        align_locators = {
            'left': self.ALIGN_LEFT,
            'center': self.ALIGN_CENTER,
            'right': self.ALIGN_RIGHT,
            'justify': self.ALIGN_JUSTIFY
        }

        if self.open_align_dropdown():
            time.sleep(0.5)
            if alignment.lower() in align_locators:
                return self.click_element(align_locators[alignment.lower()])
        return False

    # =======================
    # LINE HEIGHT METHODS
    # =======================

    def open_line_height_dropdown(self):
        """Open line height dropdown"""
        return self.click_element(self.LINE_HEIGHT_DROPDOWN)

    def set_line_height(self, height):
        """Set line height"""
        height_locators = {
            '1.0': self.LINE_HEIGHT_1_0,
            '1.5': self.LINE_HEIGHT_1_5,
            '2.0': self.LINE_HEIGHT_2_0
        }

        if self.open_line_height_dropdown():
            time.sleep(0.5)
            if str(height) in height_locators:
                return self.click_element(height_locators[str(height)])
        return False

    # =======================
    # TABLE METHODS
    # =======================

    def open_table_menu(self):
        """Open table insertion menu"""
        return self.click_element(self.TABLE_BTN)

    def insert_table(self, rows, cols):
        """Insert a table with specified dimensions"""
        try:
            if self.open_table_menu():
                time.sleep(0.5)
                # This is a simplified version - actual implementation would need
                # to interact with the dimension picker mouse catcher
                picker = self.find_element(self.TABLE_DIMENSION_PICKER)
                if picker:
                    # Simulate clicking at position for desired table size
                    # This is approximate and may need adjustment
                    cell_width = 10  # Approximate cell width in pixels
                    cell_height = 10  # Approximate cell height in pixels

                    x_offset = cols * cell_width
                    y_offset = rows * cell_height

                    self.actions.move_to_element_with_offset(picker, x_offset, y_offset).click().perform()
                    return True
        except:
            return False

    # =======================
    # LINK METHODS
    # =======================

    def open_link_dialog(self):
        """Open link insertion dialog"""
        return self.click_element(self.LINK_BTN)

    def insert_link(self, display_text, url, new_window=True):
        """Insert a link with specified text and URL"""
        try:
            if self.open_link_dialog():
                time.sleep(1)

                # Fill in link text
                text_input = self.find_element(self.LINK_TEXT_INPUT)
                if text_input:
                    text_input.clear()
                    text_input.send_keys(display_text)

                # Fill in URL
                url_input = self.find_element(self.LINK_URL_INPUT)
                if url_input:
                    url_input.clear()
                    url_input.send_keys(url)

                # Handle new window checkbox
                if new_window:
                    checkbox = self.find_element(self.LINK_NEW_WINDOW_CHECKBOX)
                    if checkbox and not checkbox.is_selected():
                        checkbox.click()

                # Click insert button
                insert_btn = self.find_element(self.LINK_INSERT_BTN)
                if insert_btn and insert_btn.is_enabled():
                    insert_btn.click()
                    return True
        except Exception as e:
            print(f"Failed to insert link: {str(e)}")
            return False

    def edit_link(self, new_display_text=None, new_url=None):
        """Edit an existing link (must be selected first)"""
        try:
            # Click link edit button in popover
            if self.click_element(self.LINK_EDIT_BTN):
                time.sleep(1)

                if new_display_text:
                    text_input = self.find_element(self.LINK_TEXT_INPUT)
                    if text_input:
                        text_input.clear()
                        text_input.send_keys(new_display_text)

                if new_url:
                    url_input = self.find_element(self.LINK_URL_INPUT)
                    if url_input:
                        url_input.clear()
                        url_input.send_keys(new_url)

                # Click insert button to save changes
                insert_btn = self.find_element(self.LINK_INSERT_BTN)
                if insert_btn and insert_btn.is_enabled():
                    insert_btn.click()
                    return True
        except:
            return False

    def unlink_selected_text(self):
        """Remove link from selected text"""
        return self.click_element(self.LINK_UNLINK_BTN)

    def close_link_dialog(self):
        """Close link dialog"""
        return self.click_element(self.LINK_CLOSE_BTN)

    # =======================
    # VIDEO METHODS
    # =======================

    def open_video_dialog(self):
        """Open video insertion dialog"""
        return self.click_element(self.VIDEO_BTN)

    def insert_video(self, video_url):
        """Insert a video with specified URL"""
        try:
            if self.open_video_dialog():
                time.sleep(1)

                url_input = self.find_element(self.VIDEO_URL_INPUT)
                if url_input:
                    url_input.clear()
                    url_input.send_keys(video_url)

                insert_btn = self.find_element(self.VIDEO_INSERT_BTN)
                if insert_btn and insert_btn.is_enabled():
                    insert_btn.click()
                    return True
        except:
            return False

    # =======================
    # IMAGE METHODS
    # =======================

    def open_image_dialog(self):
        """Open image insertion dialog"""
        return self.click_element(self.GALLERY_BTN)

    def insert_image_from_url(self, image_url):
        """Insert image from URL"""
        try:
            if self.open_image_dialog():
                time.sleep(1)

                url_input = self.find_element(self.IMAGE_URL_INPUT)
                if url_input:
                    url_input.clear()
                    url_input.send_keys(image_url)

                insert_btn = self.find_element(self.IMAGE_INSERT_BTN)
                if insert_btn and insert_btn.is_enabled():
                    insert_btn.click()
                    return True
        except:
            return False

    def upload_image_file(self, file_path):
        """Upload image file"""
        try:
            if self.open_image_dialog():
                time.sleep(1)

                file_input = self.find_element(self.IMAGE_FILE_INPUT)
                if file_input:
                    file_input.send_keys(file_path)

                    insert_btn = self.find_element(self.IMAGE_INSERT_BTN)
                    if insert_btn and insert_btn.is_enabled():
                        insert_btn.click()
                        return True
        except:
            return False

    # =======================
    # UTILITY METHODS
    # =======================

    def insert_horizontal_rule(self):
        """Insert horizontal rule"""
        return self.click_element(self.HR_BTN)

    def has_content(self):
        """Check if editor has any content"""
        content = self.get_editor_text().strip()
        return len(content) > 0

    def get_content_length(self):
        """Get the length of editor content"""
        return len(self.get_editor_text())

    def is_formatting_applied(self, format_type):
        """Check if specific formatting is applied to selected text"""
        try:
            # This would need to be implemented based on checking CSS classes
            # or computed styles of the selected text
            editor = self.find_element(self.WYSIWYG_EDITOR)
            if editor:
                # Use JavaScript to check formatting
                script = f"""
                var selection = window.getSelection();
                if (selection.rangeCount > 0) {{
                    var range = selection.getRangeAt(0);
                    var element = range.commonAncestorContainer;
                    if (element.nodeType === Node.TEXT_NODE) {{
                        element = element.parentElement;
                    }}
                    
                    var styles = window.getComputedStyle(element);
                    switch ('{format_type}') {{
                        case 'bold':
                            return styles.fontWeight === 'bold' || styles.fontWeight >= '700';
                        case 'italic':
                            return styles.fontStyle === 'italic';
                        case 'underline':
                            return styles.textDecoration.includes('underline');
                        default:
                            return false;
                    }}
                }}
                return false;
                """
                return self.driver.execute_script(script)
        except:
            return False

    def take_editor_screenshot(self, filename="rich_text_editor"):
        """Take screenshot of the editor component"""
        return self.take_screenshot(filename)

    def get_editor_html(self):
        """Get the HTML content of the editor"""
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            return editor.get_attribute('innerHTML') if editor else ""
        except:
            return ""

    def simulate_keyboard_shortcut(self, shortcut_keys):
        """Simulate keyboard shortcuts
        Args:
            shortcut_keys (str): Like 'ctrl+b', 'ctrl+i', etc.
        """
        try:
            editor = self.find_element(self.WYSIWYG_EDITOR)
            if editor:
                editor.click()  # Focus editor

                # Parse shortcut
                keys = shortcut_keys.lower().split('+')
                modifiers = []
                key = None

                for k in keys:
                    if k in ['ctrl', 'control']:
                        modifiers.append(Keys.CONTROL)
                    elif k in ['shift']:
                        modifiers.append(Keys.SHIFT)
                    elif k in ['alt']:
                        modifiers.append(Keys.ALT)
                    else:
                        key = k

                # Execute shortcut
                for modifier in modifiers:
                    self.actions.key_down(modifier)

                if key:
                    self.actions.send_keys(key)

                for modifier in reversed(modifiers):
                    self.actions.key_up(modifier)

                self.actions.perform()
                return True
        except:
            return False