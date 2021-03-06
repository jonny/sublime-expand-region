import unittest
import expand_region_handler

class WordTest(unittest.TestCase):
  def setUp(self):
    with open ("test/word_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_word_with_whitespaces_around (self):
    self.assertEqual(expand_region_handler.expand_to_word(" hello ", 3, 3), {"start": 1, "end": 6, "string": "hello", "type": "word"})

  def test_dont_find_word (self):
    self.assertEqual(expand_region_handler.expand_to_word(self.string1, 1, 10), None)

  def test_dont_find_word2 (self):
    self.assertEqual(expand_region_handler.expand_to_word(" ee ee ", 2, 5), None)

  def test_string_is_only_word (self):
    self.assertEqual(expand_region_handler.expand_to_word("bar", 1, 1), {"start": 0, "end": 3, "string": "bar", "type": "word"})

  def test_dont_find_word3 (self):
    self.assertEqual(expand_region_handler.expand_to_word("foo.bar", 5, 5), {"start": 4, "end": 7, "string": "bar", "type": "word"})

  def test_dont_find_word3_and_dont_hang (self):
    self.assertEqual(expand_region_handler.expand_to_word("aaa", 0, 3), None)

class WordWithDotsTest(unittest.TestCase):
  def test (self):
    self.assertEqual(expand_region_handler.expand_to_word_with_dots("foo.bar", 6, 7), {"start": 0, "end": 7, "string": "foo.bar", "type": "word_with_dots"})

class QuoteTest(unittest.TestCase):
  def setUp(self):
    with open ("test/quote_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/quote_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_double_quotes_inner (self):
    self.assertEqual(expand_region_handler.expand_to_quotes(self.string1, 6, 12), {"start": 1, "end": 12, "string": "test string", "type": "quotes"})

  def test_double_quotes_outer (self):
    self.assertEqual(expand_region_handler.expand_to_quotes(self.string1, 1, 12), {"start": 0, "end": 13, "string": "\"test string\"", "type": "quotes"})

  def test_single_quotes_inner (self):
    self.assertEqual(expand_region_handler.expand_to_quotes(self.string2, 6, 12), {"start": 1, "end": 12, "string": "test string", "type": "quotes"})

  def test_single_quotes_outer (self):
    self.assertEqual(expand_region_handler.expand_to_quotes(self.string2, 1, 12), {"start": 0, "end": 13, "string": "'test string'", "type": "quotes"})

class SymbolTest(unittest.TestCase):
  def setUp(self):
    with open ("test/symbol_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/symbol_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_symbol_inner (self):
    self.assertEqual(expand_region_handler.expand_to_symbols(self.string1, 7, 10), {"start": 1, "end": 10, "string": "foo - bar", "type": "symbol"})

  def test_symbol_outer (self):
    self.assertEqual(expand_region_handler.expand_to_symbols(self.string1, 1, 10), {"start": 0, "end": 11, "string": "(foo - bar)", "type": "symbol"})

  def test_look_back_dont_hang (self):
    testString = "   "
    self.assertEqual(expand_region_handler.expand(testString, 1, 2), None)

  def test_look_ahead_dont_hang (self):
    testString = "(   "
    self.assertEqual(expand_region_handler.expand(testString, 2, 2), None)

  def test_fix_look_back (self):
    self.assertEqual(expand_region_handler.expand(self.string2, 32, 32), {"start": 12, "end": 35, "string": "foo.indexOf('bar') > -1", "type": "symbol"})

class IntegrationTest(unittest.TestCase):
  def setUp(self):
    with open ("test/integration_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/integration_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_word (self):
    self.assertEqual(expand_region_handler.expand(self.string1, 7, 7), {"start": 6, "end": 9, "string": "bar", "type": "word"})

  def test_quotes_inner (self):
    self.assertEqual(expand_region_handler.expand(self.string1, 6, 9), {"start": 2, "end": 9, "string": "foo bar", "type": "quotes"})

  def test_quotes_outer (self):
    self.assertEqual(expand_region_handler.expand(self.string1, 2, 9), {"start": 1, "end": 10, "string": "\"foo bar\"", "type": "quotes"})

  def test_symbol_inner (self):
    self.assertEqual(expand_region_handler.expand(self.string1, 1, 10), {"start": 1, "end": 16, "string": "\"foo bar\" + \"x\"", "type": "symbol"})

  def test_dont_expand_to_dots (self):
    self.assertEqual(expand_region_handler.expand(self.string2, 2, 5), {"start": 1, "end": 10, "string": " foo.bar ", "type": "quotes"})

# def suite():
  # unittest.makeSuite(WordTest, "test")
  # unittest.makeSuite(QuoteTest, "test")
  # return unittest

if __name__ == "__main__":
  unittest.main()