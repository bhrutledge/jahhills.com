from django.test import TestCase

from core.templatetags.markdown_tags import markdownify


class MarkdownifyTestCase(TestCase):

    def test_renders_markdown(self):
        md_str = '- one\n- two\n- three'
        html_str = '<ul>\n<li>one</li>\n<li>two</li>\n<li>three</li>\n</ul>'

        self.assertEqual(markdownify(md_str), html_str)

    def test_allows_html(self):
        html_str = '<p><a href="http://localhost">Foo</a></p>'

        self.assertEqual(markdownify(html_str), html_str)

    def test_converts_newline_to_br(self):
        md_str = 'one\ntwo\n\nthree\nfour'
        html_str = '<p>one<br />\ntwo</p>\n<p>three<br />\nfour</p>'

        self.assertEqual(markdownify(md_str), html_str)

    def test_uses_smartypants(self):
        md_str = 'foo -- bar'
        html_str = '<p>foo &ndash; bar</p>'

        self.assertEqual(markdownify(md_str), html_str)
