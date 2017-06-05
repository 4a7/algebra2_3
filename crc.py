#                          The MIT License (MIT)
#
#                     Copyright (c) 2016 Nicco Kunzmann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
"""The crc8 module.
The crc8 module provides the same interface as the hashlib module.
	https://docs.python.org/2/library/hashlib.html
Some code was copied from here:
	https://dzone.com/articles/crc8py
and gave credit "From the PyPy project" and the link
	http://snippets.dzone.com/posts/show/3543
"""
'''
import sys

__author__="Nicco Kunzmann"
__version__="0.0.4"

PY2 = sys.version_info[0] == 2


class crc8(object):

	digest_size = 1
	block_size = 1

	_table = [	0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
				0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
				0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
				0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
				0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
				0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
				0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
				0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
				0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
				0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
				0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
				0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
				0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
				0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
				0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
				0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
				0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
				0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
				0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
				0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
				0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
				0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
				0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
				0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
				0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
				0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
				0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
				0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
				0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
				0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
				0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
				0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3]

	def __init__(self, initial_string=b''):
		"""Create a new crc8 hash instance."""
		self._sum = 0x00
		self._update(initial_string)

	def update(self, bytes_):
		"""Update the hash object with the string arg.
		Repeated calls are equivalent to a single call with the concatenation
		of all the arguments: m.update(a); m.update(b) is equivalent
		to m.update(a+b).
		"""
		self._update(bytes_)

	def digest(self):
		"""Return the digest of the bytes passed to the update() method so far.
		This is a string of digest_size bytes which may contain non-ASCII
		characters, including null bytes.
		"""
		return self._digest()

	def hexdigest(self):
		"""Return digest() as hexadecimal string.
		Like digest() except the digest is returned as a string of double
		length, containing only hexadecimal digits. This may be used to
		exchange the value safely in email or other non-binary environments.
		"""
		return hex(self._sum)[2:].zfill(2)
		
	if PY2:
		def _update(self, bytes_):
			if isinstance(bytes_, unicode):
				bytes_ = bytes_.encode()
			elif not isinstance(bytes_, str):
				raise TypeError("must be string or buffer")
			table = self._table
			_sum = self._sum
			for byte in bytes_:
				_sum = table[_sum^ord(byte)]
			self._sum = _sum

		def _digest(self):
			return chr(self._sum)
	else:
		def _update(self, bytes_):
			if isinstance(bytes_, str):
				raise TypeError("Unicode-objects must be encoded before"\
								" hashing")
			elif not isinstance(bytes_, (bytes, bytearray)):
				raise TypeError("object supporting the buffer API required")
			table = self._table
			_sum = self._sum
			for byte in bytes_:
				_sum = table[_sum^byte]
			self._sum = _sum
			
		def _digest(self):
			return bytes([self._sum])
	
	def copy(self):
		"""Return a copy ("clone") of the hash object.
		
		This can be used to efficiently compute the digests of strings that
		share a common initial substring.
		"""
		crc = crc8()
		crc._sum = self._sum
		return crc

__all__ = ['crc8']

'''
import matplotlib.pyplot as plt
import time

_table = [	0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
			0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
			0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
			0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
			0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
			0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
			0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
			0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
			0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
			0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
			0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
			0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
			0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
			0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
			0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
			0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
			0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
			0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
			0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
			0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
			0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
			0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
			0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
			0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
			0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
			0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
			0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
			0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
			0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
			0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
			0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
			0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3]



def generarCRC(arregloDeBytes):
	suma = 0x00
	table = _table
	for byte in arregloDeBytes:
		suma = table[suma^byte]
	return  hex(suma)[2:].zfill(2)
	
#Empieza con 27 bytes, 100, 500, 1 000, 10 000, 100 000
pruebas = {27   :b"Lorem ipsum dolor sit amet.",
           100  :b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec id tincidunt neque. Nam neque nullam.",
           500  :b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur at congue ex, ac consectetur turpis. Suspendisse vehicula ligula eu feugiat suscipit. Morbi auctor, urna ut eleifend rutrum, leo quam auctor orci, finibus ornare sapien mauris id erat. Etiam non nisi id eros euismod tincidunt. Nulla facilisi. Fusce erat est, laoreet ac auctor vitae, luctus et quam. Fusce dapibus porttitor enim et dictum. Proin mollis neque tortor, nec varius nibh feugiat id. Integer eu imperdiet augue massa nunc.",
           1000 :b"Lorem ipsum dolor sit amet, consectetur adipiscing elit.Mauris in erat massa. Suspendisse quis est ligula. Fusce malesuada dolor massa. Vivamus risus ex, pretium in nibh quis, imperdiet convallis neque. Etiam quis risus turpis. Nullam condimentum fringilla aliquam. Proin quis nisl ligula. Mauris in fermentum urna. Fusce ultricies magna vitae ante condimentum, ac imperdiet magna consequat. In convallis finibus faucibus. In sed luctus sem. Duis et lorem lacus. Donec neque eros, varius sit amet venenatis in, rhoncus quis arcu. Aliquam faucibus lorem non varius fringilla. Maecenas vulputate lacus neque, at euismod ex pharetra sed. Sed venenatis augue eros, eget facilisis enim tristique molestie. Aenean quis volutpat mi. Interdum et malesuada fames ac ante ipsum primis in faucibus. Morbi eu felis id nisi sollicitudin cursus. Quisque ornare, nibh eu egestas aliquam, leo neque porttitor purus, id porttitor justo ex id erat. Integer euismod euismod blandit. Ut eu placerat metus. Donec posuere.",
           10000:b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras at diam non purus aliquam vestibulum. Donec aliquam urna ut efficitur consequat. Proin at maximus ante. Nulla elementum quam ut augue pulvinar dictum. Cras viverra odio quis lorem molestie, sed hendrerit ligula bibendum. Aliquam fermentum at leo ut scelerisque. Integer mattis risus id augue posuere aliquam. Praesent sit amet tincidunt metus, ac rutrum nibh. Pellentesque dictum consectetur nisi, nec suscipit sem tempus vel. Donec facilisis sem eu diam luctus ultricies eu at lectus. Praesent venenatis sapien diam, quis feugiat turpis vulputate a. Etiam vehicula, elit ac tempor mollis, neque elit dignissim ligula, at lobortis magna magna sit amet velit. Sed sollicitudin hendrerit mauris, et pulvinar lacus pharetra vitae. Aliquam blandit ultricies tellus, non vestibulum neque fermentum sed.Fusce consequat, dolor nec suscipit tempor, nulla lectus auctor libero, ac blandit tortor tortor a justo. Nulla facilisi. Vivamus nec varius mauris, sit amet pulvinar odio. Donec ut neque ut elit convallis facilisis in accumsan leo. Suspendisse ac nulla interdum, vehicula ligula in, commodo augue. Vivamus facilisis mauris et elit placerat, at ullamcorper sapien luctus. Vestibulum arcu arcu, vehicula at maximus eu, commodo eu magna. Sed vitae finibus eros.Cras hendrerit nec neque quis mollis. Nunc sed lorem elit. Aenean orci enim, elementum quis tellus et, iaculis ultrices quam. Aliquam eleifend nunc ac orci porttitor, a ullamcorper libero mattis. Cras auctor fermentum est, id consequat erat aliquam ac. Vivamus quis blandit lorem. Interdum et malesuada fames ac ante ipsum primis in faucibus. Phasellus ut ultrices sapien. Proin pellentesque lobortis leo, at consequat odio congue vel. Proin ac tortor pretium, varius orci quis, viverra est. Aenean cursus sapien eu tristique vehicula. Aenean enim dolor, blandit quis faucibus ut, posuere quis nulla. Sed in tempor massa.Suspendisse vel imperdiet justo. Phasellus scelerisque enim ac ante feugiat lacinia. Curabitur ex purus, tempus in est luctus, fringilla facilisis quam. Proin tincidunt vulputate placerat. Curabitur leo tortor, eleifend nec vestibulum id, tempor vitae sem. Curabitur id elit vel mi varius mattis. Mauris at sagittis enim. Vivamus a tincidunt risus. Cras consequat, metus sed dictum vulputate, sapien erat auctor ex, et volutpat risus eros maximus quam. Duis sit amet velit ac augue varius accumsan. Phasellus vitae dui euismod, pharetra nulla non, rhoncus ante. Proin felis dolor, aliquam vehicula lorem in, dapibus consectetur leo. Proin dolor tellus, consequat quis venenatis eget, porta ut urna. Nulla quis pellentesque nisi, et malesuada eros. Donec ut magna semper, mollis mi et, vulputate felis. Proin viverra aliquet varius.Nam et ligula a risus lobortis condimentum. Nulla quis tempus neque. Etiam metus lectus, posuere vel enim eget, egestas pellentesque tortor. Pellentesque ac nisl vitae neque blandit pharetra eget sit amet sapien. Nunc maximus, nibh sed gravida venenatis, dui nisl feugiat dolor, quis sollicitudin dui dui vel erat. Phasellus ac odio et ante lobortis commodo ornare at metus. In mattis magna felis, ac congue velit tincidunt ut. Donec blandit tempus purus et bibendum. Aenean bibendum ullamcorper euismod. Suspendisse potenti. Mauris dictum blandit nisi quis malesuada. Aenean suscipit consectetur orci, sit amet pretium magna ullamcorper id.Nam et auctor arcu. Maecenas dignissim in enim vel dapibus. Donec aliquet, quam at gravida sagittis, neque nisl tincidunt neque, sed elementum augue nibh et libero. Vestibulum placerat, magna quis imperdiet congue, neque leo placerat nisi, nec lobortis ex sapien ac magna. Curabitur dictum faucibus enim a dignissim. Praesent luctus convallis urna eu lacinia. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean maximus diam sit amet augue mollis, tempor maximus turpis pellentesque. Proin fermentum luctus ligula, quis faucibus massa varius ut. Donec eu tincidunt neque. Maecenas tincidunt mattis tortor eu ultricies. Mauris ut lobortis nisl. Vivamus non justo urna. Nam a mi interdum, ullamcorper elit vitae, maximus ligula. Integer tempor gravida diam, vel tincidunt felis rutrum sed. Nunc eu luctus elit.Aliquam porta et lacus sed vestibulum. Proin porttitor, nisi a tincidunt bibendum, turpis purus tempus justo, at vehicula risus ante ut massa. Aliquam maximus, magna non lobortis viverra, augue tortor consectetur mauris, pharetra sodales velit ex tincidunt justo. Sed tempor vehicula lectus, vitae feugiat diam tincidunt sit amet. Suspendisse tincidunt sed lacus sed scelerisque. Aliquam at ex malesuada, pretium nunc ac, gravida ligula. Sed pulvinar diam sed interdum fringilla. Suspendisse in condimentum risus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nunc ut enim leo. Integer urna nulla, semper ac magna vel, aliquet facilisis lorem. Nulla fringilla dui nec dui lacinia mollis. Nulla malesuada, ipsum quis dictum placerat, massa massa egestas tortor, non accumsan ipsum nisi dapibus turpis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nunc venenatis, diam a sodales consequat, mauris odio interdum est, eget blandit purus sem vitae erat.Suspendisse aliquet molestie magna et aliquet. Aliquam mattis pulvinar massa. Nunc et condimentum eros, ut sagittis odio. Sed porttitor metus non mauris porta, sit amet vehicula enim porta. Praesent varius dignissim nibh ac hendrerit. Integer vel rhoncus augue. Fusce ut augue interdum, blandit orci quis, ultricies orci. Duis fermentum massa orci. Integer sodales odio dui, nec scelerisque urna sagittis ut. Ut volutpat sodales augue vel finibus. Fusce ornare, ex eu pellentesque pharetra, mauris nunc fermentum nibh, id tempus dolor massa commodo sapien. Morbi feugiat, elit vel blandit finibus, dolor libero condimentum arcu, eget tincidunt turpis lectus id elit. Cras consectetur rutrum mattis. Curabitur augue dui, semper at sagittis eget, aliquet quis nisi.Integer rhoncus vestibulum mi, et scelerisque lectus vestibulum vel. Praesent nec elementum velit. Cras tincidunt metus commodo, placerat neque vel, mattis nibh. Morbi tellus nisi, malesuada mollis aliquet ut, aliquet at lorem. Nulla facilisi. Suspendisse potenti. Pellentesque elementum tempus blandit. Aliquam mauris justo, condimentum a pharetra ac, placerat et enim. Duis sollicitudin suscipit neque, nec sollicitudin lectus tempus at. In feugiat aliquam enim id finibus. Phasellus hendrerit augue eget orci placerat, non ultrices felis vulputate. Mauris et lorem est. Donec euismod a urna non vulputate.Ut at ipsum sed dui tristique pulvinar pretium sed lectus. Integer eget sapien in sapien faucibus venenatis. Praesent egestas, leo et iaculis condimentum, metus massa congue tortor, vel suscipit enim odio non mauris. Etiam mattis diam a mi consequat, ac hendrerit enim dapibus. Vivamus sit amet vestibulum arcu. Praesent sodales massa sit amet malesuada accumsan. Etiam convallis commodo commodo. Sed a ipsum in purus semper dapibus. In a egestas elit, sit amet vehicula nisl. Quisque sit amet diam sed arcu porttitor tristique. Nunc iaculis auctor dictum. Praesent venenatis massa ut erat varius, nec ultricies magna placerat. In imperdiet pharetra velit, id sodales enim suscipit ut. Vestibulum in elementum sem.Cras nec nibh ultricies, bibendum dui iaculis, iaculis arcu. In faucibus libero eget odio rhoncus lobortis vel varius metus. Maecenas eu ante sed velit maximus placerat. Suspendisse rutrum molestie tellus, eget facilisis libero lobortis eget. Fusce tempor nulla nec risus hendrerit, eu vehicula tellus feugiat. Nam tortor eros, egestas eget erat a, commodo posuere augue. In nisi urna, lacinia vel ipsum et, dignissim fringilla velit. Vivamus sodales ante eget ipsum commodo, et hendrerit turpis sagittis. Suspendisse feugiat scelerisque pharetra. Nulla eget nunc vitae mauris bibendum semper eu in dolor. Quisque porttitor lacinia hendrerit. Praesent tincidunt egestas cursus. Morbi tincidunt ipsum eget aliquam gravida.Nullam at orci id nisi volutpat luctus. Cras a eros quis justo convallis vehicula. Cras quis felis a dui lacinia faucibus. Mauris sodales lorem ac felis lobortis egestas consequat quis ex. Pellentesque placerat nisi nisi, vitae tristique est rhoncus a. Fusce egestas bibendum iaculis. Pellentesque viverra, nunc at iaculis pretium, lectus quam posuere tellus, quis scelerisque mi sem a urna. Maecenas consequat justo eu massa cursus aliquet.Sed lacinia suscipit tortor. Phasellus id finibus tortor, eget sollicitudin elit. Proin euismod vitae lacus sit amet ullamcorper. Etiam auctor nunc nec massa finibus faucibus. Aenean interdum blandit velit quis volutpat. Sed varius sed dui a pretium. Proin id sapien lacus. Ut elementum felis eget nulla condimentum rhoncus. Nullam odio nunc, mollis non faucibus in, dignissim id quam. Nunc interdum sem urna, eu bibendum nisi fringilla id. Integer vitae tortor in ante euismod blandit ac et nunc. Praesent quis ipsum sodales, eleifend nisi eu, suscipit felis.Sed venenatis est ante, id tristique diam pretium sed. Pellentesque rhoncus arcu dolor, eu faucibus urna egestas at. Etiam eu viverra augue, vel porttitor augue. Aenean in molestie velit. Mauris et porta dolor. Nulla eget est ut lorem consequat faucibus. Proin in nibh non ipsum congue ultrices. Curabitur lacinia massa sed hendrerit bibendum. Ut vel pulvinar ipsum. Morbi libero ex, ultrices vel erat a, pellentesque sollicitudin nibh. Phasellus egestas, massa vel posuere sollicitudin, ipsum nulla ultrices neque, quis facilisis arcu sem et nisi. Nam mollis porttitor dui quis porttitor. Aliquam at placerat diam, vitae sodales nisi. Sed scelerisque metus ut dolor auctor, et pretium felis vestibulum. Pellentesque vitae diam erat.Nullam quis sem pellentesque, mollis magna ac, ullamcorper augue. Phasellus auctor erat sit amet augue commodo, eu sollicitudin orci malesuada. Nam sit amet fringilla enim. Maecenas nibh metus."}
 
pruebas[100000] = pruebas[10000]*10
pruebas[1000000] = pruebas[100000]*10

resultados = { 
			   27:0,
			   100:0,
			   500:0
			   1000:0,
			   10000:0,
			   100000:0,
			   1000000:0
			 }

for i in pruebas:
	start_time = time.time()
	print(str(i) + " bytes. ")
	print(generarCRC(pruebas[i]))
	resultados[i] = time.time() - start_time
	print("--- %s segundos ---" % (resultados[i]))


x = [27,              100,             500,             1000,             10000,             100000,             1000000]
y = [resultados[27],  resultados[100], resultados[500], resultados[1000], resultados[10000], resultados[100000], resultados[1000000]]


plt.plot(x,y, label = "Tiempo en generar CRC")
plt.xlabel("Numero de bytes")
plt.ylabel("Tiempo en segundos")
plt.title("Generacion de codigo CRC")
plt.legend()
plt.show()
