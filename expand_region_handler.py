import re

def expand(string, start, end):
  result = expand_to_word(string, start, end)
  if result:
    return result

  result = expand_to_quotes(string, start, end)
  if result:
    return result

  result = expand_to_word_with_dots(string, start, end)
  if result:
    return result

  result = expand_to_symbols(string, start, end)
  if result:
    return result

  print(None)

def expand_to_word(string, startIndex, endIndex):
  negativeWordRe = re.compile("^[a-zA-Z0-9_$]*$");
  positiveWordRe = re.compile("[a-zA-Z0-9_$]*$");

  return _expand_to_regex_rule(string, startIndex, endIndex, negativeWordRe, positiveWordRe, "word")

def expand_to_word_with_dots(string, startIndex, endIndex):
  negativeWordWithDots = re.compile("^[a-zA-Z0-9_$.]*$");
  positiveWordWithDots = re.compile("[a-zA-Z0-9_$.]*$");

  return _expand_to_regex_rule(string, startIndex, endIndex, negativeWordWithDots, positiveWordWithDots, "word_with_dots")

def _expand_to_regex_rule(string, startIndex, endIndex, negativeRe, positiveRe, type):
  if(startIndex != endIndex):
    selection = string[startIndex:endIndex]
    if positiveRe.match(selection) is None:
      return None

  searchIndex = startIndex - 1;
  while True:
    if searchIndex < 0:
      newStartIndex = searchIndex + 1
      break
    char = string[searchIndex:searchIndex+1]
    if negativeRe.match(char) is None:
      newStartIndex = searchIndex + 1
      break
    else:
      searchIndex -= 1

  searchIndex = endIndex;
  while True:
    if searchIndex > len(string) - 1:
      newEndIndex = searchIndex
      break
    char = string[searchIndex:searchIndex+1]
    if negativeRe.match(char) is None:
      newEndIndex = searchIndex
      break
    else:
      searchIndex += 1

  try:
    if startIndex == newStartIndex and endIndex == newEndIndex:
      return None
    else:
      return create_return_obj(newStartIndex, newEndIndex, string, type)
  except NameError:
    return None

def expand_to_quotes(string, startIndex, endIndex):
  quotesRe = re.compile(r'([\'"])(?:\1|.*?[^\\]\1)')

  for match in re.finditer(quotesRe, string):
    start = match.start(0)
    end = match.end(0)

    if end < startIndex:
      continue

    if(startIndex == start and endIndex == end):
      return None

    if(startIndex >= start and endIndex <= end):
      if(startIndex == start + 1 and endIndex == end - 1):
        if(startIndex == start and endIndex == end):
          return None
        else:
          return create_return_obj(start, end, string, "quotes")
      else:
        return create_return_obj(start + 1, end - 1, string, "quotes")

def expand_to_symbols(string, startIndex, endIndex):
  openingSymbols = "([{";
  closingSymbols = ")]}";
  symbolsRe = re.compile(r'(['+re.escape(openingSymbols + closingSymbols)+'])')

  counterparts = {
    "(":")",
    "{":"}",
    "[":"]",
    ")":"(",
    "}":"{",
    "]":"["
  }

  symbolStack = []

  searchIndex = startIndex - 1;
  while True:
    if(searchIndex < 0):
      return None
    char = string[searchIndex:searchIndex+1]
    result = symbolsRe.match(char)
    if result:
      symbol = result.group()
      if(symbol in openingSymbols and len(symbolStack) == 0):
        newStartIndex = searchIndex + 1
        break
      else:
        if len(symbolStack) > 0 and symbolStack[len(symbolStack) - 1] == counterparts[symbol]:
          symbolStack.pop()
        else:
          symbolStack.append(symbol)
    searchIndex -= 1


  symbolPairRe = re.compile(r'(['+re.escape(symbol + counterparts[symbol])+'])')

  symbolStack = [symbol]

  searchIndex = endIndex;
  while True:
    char = string[searchIndex:searchIndex+1]
    result = symbolPairRe.match(char)
    if result:
      symbol = result.group()

      if symbolStack[len(symbolStack) - 1] == counterparts[symbol]:
        symbolStack.pop()
      else:
        symbolStack.append(symbol)

      if len(symbolStack) == 0:
        newEndIndex = searchIndex;
        break

    if searchIndex == len(string):
      break

    searchIndex += 1

  try:
    if(startIndex == newStartIndex and endIndex == newEndIndex):
      return create_return_obj(newStartIndex - 1, newEndIndex + 1, string, "symbol")
    else:
      return create_return_obj(newStartIndex, newEndIndex, string, "symbol")
  except NameError:
    return None

def create_return_obj(start, end, string, type):
  return {"start": start, "end": end, "string": string[start:end], "type": type}