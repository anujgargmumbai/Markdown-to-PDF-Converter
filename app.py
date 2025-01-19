import streamlit as st
import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bs4 import BeautifulSoup
from io import BytesIO

# Register a font that supports Unicode
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))


class CheckboxFlowable(Flowable):
    def __init__(self, checked, text, font_size=12, space_after=10):
        super().__init__()
        self.checked = checked
        self.text = text
        self.font_size = font_size
        self.space_after = space_after

    def wrap(self, availWidth, availHeight):
        """Set the height of the checkbox item."""
        return availWidth, self.font_size + self.space_after

    def draw(self):
        # Draw the checkbox
        self.canv.setFont("DejaVuSans", self.font_size)
        checkbox = "☑" if self.checked else "☐"  # Unicode checkbox characters
        self.canv.drawString(0, 0, checkbox)

        # Draw the text next to the checkbox
        self.canv.drawString(20, 0, self.text)


class MarkdownToPDFConverter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()

    def create_custom_styles(self):
        """Create custom styles for different markdown elements."""
        self.styles['Heading1'].fontSize = 24
        self.styles['Heading1'].spaceAfter = 0
        self.styles['Heading2'].fontSize = 20
        self.styles['Heading2'].spaceAfter = 0
        self.styles['Heading3'].fontSize = 16
        self.styles['Heading3'].spaceAfter = 0

    def process_html_element(self, element):
        """Process HTML elements and return appropriate PDF elements."""
        if element.name is None:
            text = str(element).strip()
            if text:
                return [Paragraph(text, self.styles['Normal']), Spacer(1, 12)]
            return []

        elements = []

        if element.name in ['h1', 'h2', 'h3']:
            style_name = f'Heading{element.name[1]}'
            elements.append(Paragraph(element.get_text(), self.styles[style_name]))
            elements.append(Spacer(1, 12))
        elif element.name == 'p':
            text = element.get_text().strip()
            if text:
                elements.append(Paragraph(text, self.styles['Normal']))
                elements.append(Spacer(1, 12))
        elif element.name == 'ul':
            for li in element.find_all('li'):
                text = li.get_text().strip()
                # Check if the text starts with a checkbox indicator ([ ] or [x])
                if text.startswith('[ ]'):
                    elements.append(CheckboxFlowable(False, text[3:].strip()))
                elif text.startswith('[x]'):
                    elements.append(CheckboxFlowable(True, text[3:].strip()))
                else:
                    elements.append(Paragraph(f'• {text}', self.styles['Normal']))
                elements.append(Spacer(1, 1))  # Add spacing after each list item
        return elements

    def convert(self, markdown_text, page_size=letter):
        """Convert markdown text to PDF bytes."""
        try:
            # Convert markdown to HTML
            html = markdown.markdown(markdown_text, extensions=['sane_lists'])
            soup = BeautifulSoup(html, 'html.parser')

            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=page_size,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            elements = []
            for element in soup.children:
                elements.extend(self.process_html_element(element))

            if elements:
                doc.build(elements)
            else:
                raise Exception("No content to convert")

            return pdf_buffer.getvalue()

        except Exception as e:
            raise Exception(f"Error converting markdown to PDF: {str(e)}")


def main():
    st.set_page_config(page_title="Markdown to PDF Converter", page_icon="📄")

    st.title("Markdown to PDF Converter")
    st.markdown("Convert your Markdown text to a professionally formatted PDF document.")

    # Example markdown text with proper checkbox formatting
    example_text = """# 21. Performance Metrics

- [x] Conversion rate tracking
- [ ] Bounce rate analysis
- [ ] Time on page
- [ ] User flow analysis
- [ ] Exit page monitoring"""

    # Create tabs for input methods
    tab1, tab2 = st.tabs(["Enter Text", "Upload File"])

    with tab1:
        markdown_text = st.text_area(
            "Enter your Markdown text here:",
            value=example_text,
            height=300
        )

    with tab2:
        uploaded_file = st.file_uploader("Choose a markdown file", type=['md', 'txt'])
        if uploaded_file:
            markdown_text = uploaded_file.getvalue().decode()

    # Page size selection
    page_size = st.selectbox(
        "Select page size:",
        options=["Letter", "A4"],
        index=0
    )

    # Preview section
    st.subheader("Preview")
    st.markdown(markdown_text)

    # Convert button
    if st.button("Convert to PDF", type="primary"):
        try:
            converter = MarkdownToPDFConverter()
            page_size_map = {"Letter": letter, "A4": A4}
            pdf_bytes = converter.convert(markdown_text, page_size_map[page_size])

            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="converted_document.pdf",
                mime="application/pdf"
            )

            st.success("✅ PDF generated successfully!")

        except Exception as e:
            st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
