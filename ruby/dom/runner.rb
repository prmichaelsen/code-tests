#!/usr/bin/env ruby -w

# Run this script in order to see if your code is doing the right thing.
# Feel free to modify anything in here

require '../test_support'
require 'rexml/document'

# Simple DOM Parser using REXML (Ruby's built-in XML parser)
class SimpleDOMParser
  attr_reader :doc
  
  def initialize(file)
    @doc = REXML::Document.new(file)
  end
  
  # Find all elements by tag name
  def find_all(tag_name)
    elements = []
    @doc.elements.each("//#{tag_name}") do |element|
      elements << element
    end
    elements
  end
  
  # Find element by attribute
  def find_by_attribute(tag_name, attr_name, attr_value)
    @doc.elements.each("//#{tag_name}[@#{attr_name}='#{attr_value}']") do |element|
      return element
    end
    nil
  end
  
  # Find all elements with specific child element value
  def find_by_child_value(tag_name, child_name, child_value)
    elements = []
    @doc.elements.each("//#{tag_name}") do |element|
      child = element.elements[child_name]
      if child && child.text == child_value
        elements << element
      end
    end
    elements
  end
end

# Load and parse the XML file
file = File.new("books.xml")
parser = SimpleDOMParser.new(file)

puts "\n" + "=" * 70
puts "DOM PARSING DEMONSTRATION"
puts "=" * 70 + "\n"

# Task 1: Find all book elements
puts "1. Finding all book elements:"
books = parser.find_all("book")
puts "   Found #{books.length} books"
books.each do |book|
  title = book.elements["title"].text
  puts "   - #{title}"
end

# Task 2: Find all author elements
puts "\n2. Finding all author elements:"
authors = parser.find_all("author")
puts "   Found #{authors.length} authors"
authors.each do |author|
  puts "   - #{author.text}"
end

# Task 3: Find the book with id of bk103
puts "\n3. Finding book with id='bk103':"
book = parser.find_by_attribute("book", "id", "bk103")
if book
  title = book.elements["title"].text
  author = book.elements["author"].text
  genre = book.elements["genre"].text
  puts "   Found: '#{title}' by #{author} (#{genre})"
else
  puts "   Book not found"
end

# Task 4: Find all book elements in the Fantasy genre
puts "\n4. Finding all Fantasy books:"
fantasy_books = parser.find_by_child_value("book", "genre", "Fantasy")
puts "   Found #{fantasy_books.length} Fantasy books"
fantasy_books.each do |book|
  title = book.elements["title"].text
  author = book.elements["author"].text
  puts "   - '#{title}' by #{author}"
end

puts "\n" + "=" * 70 + "\n"

# Run assertions to verify correctness
it "finds all book elements" do
  assert books.length == 12
end

it "finds all author elements" do
  assert authors.length == 12
end

it "finds book with id bk103" do
  assert book != nil
  assert book.elements["title"].text == "Maeve Ascendant"
end

it "finds all Fantasy genre books" do
  assert fantasy_books.length == 4
  assert fantasy_books.all? { |b| b.elements["genre"].text == "Fantasy" }
end

puts "\nAll assertions passed! ✓\n"
