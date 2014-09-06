import string
import re
import jinja2
import os
from io import BytesIO
import png
import webapp2

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

characters = {
	' ': [0,0,0,0,0,0,0,0,0,0,0,0],
	'0': [0,0,1,0,0,0,0,0,0,0,0,0],
	'1': [0,0,0,1,0,0,0,0,0,0,0,0],
	'2': [0,0,0,0,1,0,0,0,0,0,0,0],
	'3': [0,0,0,0,0,1,0,0,0,0,0,0],
	'4': [0,0,0,0,0,0,1,0,0,0,0,0],
	'5': [0,0,0,0,0,0,0,1,0,0,0,0],
	'6': [0,0,0,0,0,0,0,0,1,0,0,0],
	'7': [0,0,0,0,0,0,0,0,0,1,0,0],
	'8': [0,0,0,0,0,0,0,0,0,0,1,0],
	'9': [0,0,0,0,0,0,0,0,0,0,0,1],
	'A': [1,0,0,1,0,0,0,0,0,0,0,0],
	'B': [1,0,0,0,1,0,0,0,0,0,0,0],
	'C': [1,0,0,0,0,1,0,0,0,0,0,0],
	'D': [1,0,0,0,0,0,1,0,0,0,0,0],
	'E': [1,0,0,0,0,0,0,1,0,0,0,0],
	'F': [1,0,0,0,0,0,0,0,1,0,0,0],
	'G': [1,0,0,0,0,0,0,0,0,1,0,0],
	'H': [1,0,0,0,0,0,0,0,0,0,1,0],
	'I': [1,0,0,0,0,0,0,0,0,0,0,1],
	'J': [0,1,0,1,0,0,0,0,0,0,0,0],
	'K': [0,1,0,0,1,0,0,0,0,0,0,0],
	'L': [0,1,0,0,0,1,0,0,0,0,0,0],
	'M': [0,1,0,0,0,0,1,0,0,0,0,0],
	'N': [0,1,0,0,0,0,0,1,0,0,0,0],
	'O': [0,1,0,0,0,0,0,0,1,0,0,0],
	'P': [0,1,0,0,0,0,0,0,0,1,0,0],
	'Q': [0,1,0,0,0,0,0,0,0,0,1,0],
	'R': [0,1,0,0,0,0,0,0,0,0,0,1],
	'S': [0,0,1,0,1,0,0,0,0,0,0,0],
	'T': [0,0,1,0,0,1,0,0,0,0,0,0],
	'U': [0,0,1,0,0,0,1,0,0,0,0,0],
	'V': [0,0,1,0,0,0,0,1,0,0,0,0],
	'W': [0,0,1,0,0,0,0,0,1,0,0,0],
	'X': [0,0,1,0,0,0,0,0,0,1,0,0],
	'Y': [0,0,1,0,0,0,0,0,0,0,1,0],
	'Z': [0,0,1,0,0,0,0,0,0,0,0,1],
	'&': [1,0,0,0,1,0,0,0,0,0,1,0],
	'cent': [1,0,0,0,0,1,0,0,0,0,1,0],
	'.': [1,0,0,0,0,0,1,0,0,0,1,0],
	'<': [1,0,0,0,0,0,0,1,0,0,1,0],
	'(': [1,0,0,0,0,0,0,0,1,0,1,0],
	'+': [1,0,0,0,0,0,0,0,0,1,1,0],
	'-': [0,1,0,0,1,0,0,0,0,0,1,0],
	'!': [0,1,0,0,0,1,0,0,0,0,1,0],
	'$': [0,1,0,0,0,0,1,0,0,0,1,0],
	'*': [0,1,0,0,0,0,0,1,0,0,1,0],
	')': [0,1,0,0,0,0,0,0,1,0,1,0],
	';': [0,1,0,0,0,0,0,0,0,1,1,0],
	'/': [0,0,1,1,0,0,0,0,0,0,1,0],
	'??': [0,0,1,0,1,0,0,0,0,0,1,0],
	',': [0,0,1,0,0,1,0,0,0,0,1,0],
	'%': [0,0,1,0,0,0,1,0,0,0,1,0],
	'_': [0,0,1,0,0,0,0,1,0,0,1,0],
	'>': [0,0,1,0,0,0,0,0,1,0,1,0],
	'?': [0,0,1,0,0,0,0,0,0,1,1,0],
	':': [0,0,0,0,1,0,0,0,0,0,1,0],
	'#': [0,0,0,0,0,1,0,0,0,0,1,0],
	'@': [0,0,0,0,0,0,1,0,0,0,1,0],
	"'": [0,0,0,0,0,0,0,1,0,0,1,0],
	'=': [0,0,0,0,0,0,0,0,1,0,1,0],
	'"': [0,0,0,0,0,0,0,0,0,1,1,0]
}

block_no_punch = [
	'1111',
	'1111',
	'1111',
	'1111',
	'1111',
	'1111',
	'1111',
	'1111',
	'1111',
	'1111',
	'1111'
]

block_punch = [
	'0001',
	'0001',
	'0001',
	'0001',
	'0001',
	'0001',
	'0001',
	'0001',
	'1111',
	'1111',
	'1111'
]

def character_to_bits(character):
	if character in characters.keys():
		return characters[character]
	return characters[' ']

def bits_to_column(bits):
	column = []
	# printing row
	for row in block_no_punch:
		column.append(row)
	# punch rows
	for bit in bits:
		if bit == 0:
			for row in block_no_punch:
				column.append(row)
		if bit == 1:
			for row in block_punch:
				column.append(row)
	# bottom margin
	return column

def columns_to_card(columns):
	card = []
	left_margin = 6
	right_margin = 6
	card_width = left_margin + (len(columns) * len(columns[0])) + right_margin
	for i in xrange(len(columns[0])):
		row = '1' * left_margin
		for i2 in xrange(len(columns)):
			row = row + columns[i2][i]
		row = row + ('1' * right_margin)
		card.append(row)
	return card

def punch_card(text, out):
	columns = []
	spaces = ' ' * 80
	text = 'LOGIN 3004,11427 abcd' + spaces
	card_text = text[0:80]
	for c in card_text:
		columns.append(bits_to_column(character_to_bits(c)))

	card = columns_to_card(columns)

	io = BytesIO()
	w = png.Writer(len(card[0]), len(card), greyscale=True, bitdepth=1)
	w.write(io, card)
	out.write(io.getvalue())
	io.close()

class IndexPage(webapp2.RequestHandler):
	def get(self):
		template_values = { }
		template = jinja_environment.get_template('templates/index.html.jinja')
		self.response.out.write(template.render(template_values))

class PunchRequest(webapp2.RequestHandler):
	def get(self):
		card_text = self.request.get('text')
		self.response.headers['Content-Type'] = 'image/png'
		self.response.headers['Content-Transfer-Encoding'] = 'Binary'
		self.response.headers['Content-disposition'] = 'attachment; filename="card.png"'
		punch_card(card_text, self.response.out)

class NotFoundPage(webapp2.RequestHandler):
	def get(self):
		self.error(404)
		template_values = { }
		template = jinja_environment.get_template('templates/not-found.html.jinja')
		self.response.out.write(template.render(template_values))

application = webapp2.WSGIApplication(
	[
		('/', IndexPage),
		('/punch', PunchRequest),
		('/.*', NotFoundPage)
	],
	debug=False)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
