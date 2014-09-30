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
	'\xa2': [1,0,0,0,1,0,0,0,0,0,1,0],
	'.': [1,0,0,0,0,1,0,0,0,0,1,0],
	'<': [1,0,0,0,0,0,1,0,0,0,1,0],
	'(': [1,0,0,0,0,0,0,1,0,0,1,0],
	'+': [1,0,0,0,0,0,0,0,1,0,1,0],
	'|': [1,0,0,0,0,0,0,0,0,1,1,0],
	'!': [0,1,0,0,1,0,0,0,0,0,1,0],
	'$': [0,1,0,0,0,1,0,0,0,0,1,0],
	'*': [0,1,0,0,0,0,1,0,0,0,1,0],
	')': [0,1,0,0,0,0,0,1,0,0,1,0],
	';': [0,1,0,0,0,0,0,0,1,0,1,0],
	'\xac': [0,1,0,0,0,0,0,0,0,1,1,0],
	'/': [0,0,1,1,0,0,0,0,0,0,1,0],
	'-': [0,0,1,0,1,0,0,0,0,0,1,0],
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
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111'
]

block_punch = [
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'00000011',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111',
	'11111111'
]

def legal_character(character):
	if character.upper() in characters.keys():
		return character.upper()
	return ' '

def legal_for_punchcard(text):
	legal_text = ''
	for c in text:
		legal_text += legal_character(c)
	return legal_text

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

def punch_card_svg(text):
	svg = []
	svg.append('<?xml version="1.0" standalone="no"?>')
	svg.append('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">')
	svg.append('<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="607pt" height="270pt" viewBox="0 0 607 270" preserveAspectRatio="xMidYMid meet">')
	svg.append('<metadata>Created by CardPunch on Google App Engine (cardpunch.appspot.com)</metadata>')
	svg.append('<rect x="1" y="1" width="605" height="268" fill="white" stroke="black" stroke-width="2"></rect>')
	column = 0
	for c in text:
		x = 10 + column * 7
		bits = character_to_bits(c)
		zone = 0
		for bit in bits:
			y = 16 + zone * 21
			if bit == 1:
				svg.append('<rect x="' + str(x) + '" y="' + str(y) + '" width="4" height="12" fill="black"></rect>')
			zone += 1
		column += 1
	svg.append('</svg>')
	return "".join(svg)
	
def punch_card_png(text, out):
	columns = []
	spaces = ' ' * 80
	text = text + spaces
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
		legal_text = legal_for_punchcard(card_text)
		format = self.request.get('format')
		if format == 'png':
			self.response.headers['Content-Type'] = 'image/png'
			self.response.headers['Content-Transfer-Encoding'] = 'Binary'
			punch_card_png(legal_text, self.response.out)
		else:
			self.response.headers['Content-Type'] = 'image/svg+xml'
			svg = punch_card_svg(legal_text)
			self.response.out.write(svg)

class LegalText(webapp2.RequestHandler):
	def get(self):
		card_text = self.request.get('text')
		legal_text = legal_for_punchcard(card_text)
		self.response.headers['Content-Type'] = 'image/plain'
		self.response.out.write(legal_text)
			
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
		('/legaltext', LegalText),
		('/.*', NotFoundPage)
	],
	debug=False)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
