import html

user_input = "<script>alert('XSS');</script>"
escaped_input = html.escape(user_input)
print(escaped_input)
