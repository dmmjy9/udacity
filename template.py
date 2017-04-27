import os

import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *arg, **kwargs):
        self.response.out.write(*arg, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))


class MainPage(Handler):
    def get(self):
        items = self.request.get("text")
        self.render("index.html", items=items)

    def post(self):
        unicode_text = str(self.request.get("text"))
        input_text = unicode_text.encode("utf-8")
        trans_list = list(input_text)
        encrypted_list = self.encrypt(trans_list)
        encrypted_str = ''.join(encrypted_list)
        self.render("index.html", items=encrypted_str)

    def encrypt(self, trans_list):
        list_len = len(trans_list)
        encrypted_list = []
        for encrypting_text in trans_list:
            if ord(encrypting_text)+13 <= 122 and ord(encrypting_text)+13 >= 97:
                encrypted_list.append(chr(ord(encrypting_text)+13))
            elif ord(encrypting_text)+13 > 122 and ord(encrypting_text) <= 122:
                encrypted_list.append(chr(ord(encrypting_text)+13-122+96))
            else:
                return "Input Error!"
        return encrypted_list


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)