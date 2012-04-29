"""
squnch.py
    Some routines for fuzzing data.

Written by Jesse Burns (jesse@isecpartners.com)

Copyright (C) 2006, Information Security Partners, LLC.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import random

class Squncher:
  """ create it with a random and have it manipulate data for you. """
  DENOM = 50 # change at most 0-2 % of the binary with each fuzz
  r = None
  int_slide_position = 0
  slide_step = 1
  ALL_CHARS = ''.join([chr(n) for n in xrange(256)])
  
  
  def __init__(self, random_object, demoninator = 50):
    self.DENOM = demoninator
    self.r = random_object
    self.PERCENT_N = '\x25\x6e\x25\x6e\x25\x6e\x25\x6e'

  def random_string(self, size, char_set = ALL_CHARS):
    num = self.r.choice("123456789")
    string = ""
    if int(num) % 3 == 0 and size > 8:
        new_size = size - 8
        string = ''.join([self.r.choice(char_set) for n in xrange(new_size)])
        string = string + self.PERCENT_N
        return string
    elif int(num) % 7 == 0 and size > 8:
        new_size = size - 8
        string = ''.join([self.r.choice(char_set) for n in xrange(new_size)])
        string = string + self.PERCENT_N
        return string
    elif size % 8 == 0 and size > 8:
        new_size = size/8
        return ''.join([self.PERCENT_N for n in xrange(new_size)])
    return ''.join([self.r.choice(char_set) for n in xrange(size)])
  
  def eliminate_random(self, original):
    size = len(original)
    cut_size = max(1, self.r.randint(1, max(1, size/self.DENOM)))
    cut_pos = self.r.randint(0, size - cut_size)
    result = original[:cut_pos] + original[cut_pos + cut_size:]
    assert len(original) > len(result), "elmination failed to reduce size %d %d" % (len(original), len(result))
    return result

  def add_random(self, original):
    size = len(original)
    add_size = max(1, self.r.randint(1, max(1, size/self.DENOM)))
    cut_pos = self.r.randint(0, size - add_size)
    result = ''.join([original[:cut_pos], self.random_string(add_size), original[cut_pos:]])
    assert len(original) < len(result), "adding failed to increase size  %d %d" % (len(original), len(result))
    return result
  
  def change_random(self, original):
    size = len(original)
    add_size = max(1, self.r.randint(1, max(1, size/self.DENOM)))
    cut_pos = self.r.randint(0, size - add_size)
    result = ''.join([original[:cut_pos], self.random_string(add_size), original[cut_pos + add_size:]])
    assert len(original) == len(result), "size changed on a random change %d %d" % (len(original), len(result))
    return result
  
  def single_change_random(self, original):
    changes = self.r.randint(1, 100)
    size = len(original)
    for a in xrange(changes):
      cut_pos = self.r.randint(1, size)
      original = ''.join([original[:cut_pos - 1], chr(self.r.randint(1, 255)), original[cut_pos:]])
    assert len(original) == size, "size changed on a random tweak %d %d" % (len(original), size)
    return original
  
  def lower_single_random(self, original):
    changes = self.r.randint(1, 100)
    size = len(original)
    result = original
    for a in xrange(changes):
      cut_pos = self.r.randint(1, size)
      result = ''.join([result[:cut_pos - 1], chr(max(0, ord(result[cut_pos - 1]) - 1)), result[cut_pos:]])
    assert len(result) == size, "size changed on a random tweak %d %d" % (len(original), size)
    # assert result != original, "nothing changed in lower_single_random %d - actually this can happen due to max above" % changes
    return result
  
  def raise_single_random(self, original):
    changes = self.r.randint(1, 100)
    size = len(original)
    result = original
    for a in xrange(changes):
      cut_pos = self.r.randint(1, size)
      result = result[:cut_pos - 1] + chr(min(255, ord(result[cut_pos - 1]) + 1)) + result[cut_pos:]
    assert len(result) == size, "size changed on a random tweak %d %d" % (len(original), size)
    #assert result != original, "nothing changed in lower_single_random %d - actually this can happen due to min above" % changes
    return result
  
  def eliminate_null(self, original, replacement = 'A'):
    size = len(original)
    cut_pos = original.find('\0', self.r.randint(0, size))
    if (cut_pos != -1):
      result = ''.join([original[:cut_pos], replacement, original[cut_pos + 1:]])
    else:
      return original
    assert len(original) == len(result), "size changed on a null elmination change %d %d" % (len(original), len(result))
    return result
  
  def eliminate_double_null(self, original, replacement = 'AA'):
    size = len(original) - 1
    cut_pos = original.find('\0\0', self.r.randint(0, size))
    if (cut_pos != -1):
      result = ''.join([original[:cut_pos], replacement, original[cut_pos + 2:]])
    else:
      return original
    assert len(original) == len(result), "size changed on a null elmination change %d %d" % (len(original), len(result))
    return result
  
  def totally_random(self, original):
    return self.random_string(self.r.randint(10, 1000))

  def int_slide(self, original):
    size = len(original)
    value = self.r.choice(['\xFF\xFF\xFF\xFF', '\x80\x00\x00\x00', '\x00\x00\x00\x00', '\xAA\xAA\xAA\xAA', '\x41\x41\x41\x41'])
    if size < 4 : return value[:size]
    start = self.int_slide_position % size
    if start > size - 4: 
      result = original[:start] + value
    else:
      result = ''.join([original[:start], value, original[start + 4:]])
    self.int_slide_position += self.slide_step
    return result

  def double_fuzz(self, original):
    """ runs two fuzzers (one or more of which could be double_fuzz itself! """
    result = self.r.choice(self.mutators)(self, original)
    return self.r.choice(self.mutators)(self, result)

  mutators = [eliminate_random, add_random, change_random, single_change_random, lower_single_random, raise_single_random, eliminate_null, eliminate_double_null, totally_random, int_slide, double_fuzz]
  
  def mutate(self, original):
    while True:
      yield self.r.choice(self.mutators)(self, original)
