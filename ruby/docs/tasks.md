# Ruby Interview Tasks

## Overview
This directory contains Ruby interview tests focused on implementing a message queue system and XML/DOM parsing functionality.

## Test 1: Message Queue Implementation

### Core Requirements

#### 1. SimpleMessageQueue Class
- [ ] Implement [`SimpleMessageQueue`](../message_queue/message_queue.rb) class
- [ ] Include the `MessageQueue` module
- [ ] Implement `subscribe` method
- [ ] Implement `publish` method
- [ ] Handle multiple message types
- [ ] Support block-based receivers

#### 2. Subscribe Method
- [ ] Accept one or more message types (string or array of strings)
- [ ] Accept a block as the receiver/handler
- [ ] Store subscriptions for later notification
- [ ] Support multiple subscribers for same message type
- [ ] Handle edge cases (nil types, empty arrays)

#### 3. Publish Method
- [ ] Accept message type as parameter
- [ ] Accept optional data parameter
- [ ] Notify all subscribers for the given type
- [ ] Pass data to receiver blocks
- [ ] Handle receiver errors gracefully (one bad receiver shouldn't affect others)
- [ ] Continue processing even if a receiver raises an exception

#### 4. Testing with Runner
- [ ] Run [`runner.rb`](../message_queue/runner.rb) to test implementation
- [ ] Pass all basic assertions
- [ ] Pass increasingly complex assertions
- [ ] Verify error handling works correctly
- [ ] Test multiple subscribers
- [ ] Test with and without data

### Implementation Details

#### Data Structures
- [ ] Choose appropriate structure for storing subscriptions
  - Hash with message type as key?
  - Array of subscription objects?
  - Consider lookup performance
- [ ] Handle multiple subscribers per message type
- [ ] Store blocks/procs for later execution

#### Error Handling
- [ ] Wrap receiver calls in begin/rescue blocks
- [ ] Log or handle receiver exceptions
- [ ] Ensure one failing receiver doesn't stop others
- [ ] Consider what to do with exceptions (log, ignore, collect?)

### Extra Credit: Map Reduce
- [ ] Review [`map_reduce.rb`](../message_queue/map_reduce.rb)
- [ ] Implement map-reduce functionality using message queue
- [ ] Apply functional programming concepts
- [ ] Handle data transformation pipeline
- [ ] Test with sample data

## Test 2: DOM/XML Parsing

### Core Requirements

#### 1. XML Parser Implementation
- [ ] Implement parser in [`runner.rb`](../dom/runner.rb)
- [ ] Parse [`books.xml`](../dom/books.xml)
- [ ] Support finding elements by tag name
- [ ] Support finding elements by attribute
- [ ] Support filtering by attribute value

#### 2. Required Operations
- [ ] Find all `<book>` elements
- [ ] Find all `<author>` elements
- [ ] Find the book with `id` of `bk103`
- [ ] Find all book elements in the "Fantasy" genre

#### 3. Parser Design Considerations
- [ ] Choose parsing approach:
  - DOM parsing (load entire tree)
  - SAX parsing (event-based)
  - XPath queries
  - Custom parser
- [ ] Document why you chose your approach
- [ ] Discuss trade-offs of your approach
- [ ] Consider performance implications
- [ ] Consider memory usage

### Implementation Options

#### Option 1: REXML (Built-in)
- [ ] Use Ruby's built-in REXML library
- [ ] Parse XML document
- [ ] Use XPath or element traversal
- [ ] Handle namespaces if present

#### Option 2: Nokogiri (Gem)
- [ ] Install Nokogiri gem
- [ ] Use CSS selectors or XPath
- [ ] Leverage performance benefits
- [ ] Handle malformed XML

#### Option 3: Custom Parser
- [ ] Build simple XML parser from scratch
- [ ] Use regular expressions or string parsing
- [ ] Handle basic XML structure
- [ ] Demonstrate understanding of parsing concepts

### Testing with Nutrition XML
- [ ] Also test with [`nutrition.xml`](../dom/nutrition.xml)
- [ ] Verify parser works with different XML structures
- [ ] Handle different element types
- [ ] Test attribute extraction

## Files to Modify/Create

### Message Queue
- [`message_queue/message_queue.rb`](../message_queue/message_queue.rb) - Main implementation
- [`message_queue/runner.rb`](../message_queue/runner.rb) - Test runner (review/modify as needed)
- [`message_queue/map_reduce.rb`](../message_queue/map_reduce.rb) - Extra credit implementation

### DOM Parsing
- [`dom/runner.rb`](../dom/runner.rb) - Main implementation and tests
- Create additional files as needed for organization
- Consider creating separate parser class

### Supporting Files
- [`test_support.rb`](../test_support.rb) - Test utilities (already provided)

## Testing Strategy

### Message Queue Tests
- [ ] Test basic subscribe and publish
- [ ] Test multiple subscribers
- [ ] Test with data parameter
- [ ] Test without data parameter
- [ ] Test error handling (bad receiver)
- [ ] Test multiple message types
- [ ] Test unsubscribed message types
- [ ] Use assertions from `test_support.rb`

### DOM Parser Tests
- [ ] Test finding all elements of a type
- [ ] Test finding element by ID
- [ ] Test filtering by attribute value
- [ ] Test with different XML files
- [ ] Test edge cases (empty results, malformed XML)
- [ ] Use assertions from `test_support.rb`

## Running the Tests

```bash
# Message Queue
cd message_queue
./runner.rb

# DOM Parsing
cd dom
./runner.rb
```

## Code Quality Guidelines

### Ruby Best Practices
- [ ] Follow Ruby style guide
- [ ] Use meaningful variable names
- [ ] Keep methods small and focused
- [ ] Use appropriate Ruby idioms
- [ ] Leverage blocks and procs effectively
- [ ] Handle nil cases gracefully

### Documentation
- [ ] Add comments explaining complex logic
- [ ] Document method parameters and return values
- [ ] Explain design decisions
- [ ] Note any assumptions made
- [ ] Discuss trade-offs in approach

### Error Handling
- [ ] Use begin/rescue appropriately
- [ ] Don't swallow exceptions silently
- [ ] Provide meaningful error messages
- [ ] Handle edge cases gracefully

## Discussion Points

### Message Queue
- [ ] Why did you choose your data structure?
- [ ] How does your implementation handle errors?
- [ ] What are the performance characteristics?
- [ ] How would you extend this for production use?
- [ ] What thread-safety concerns exist?

### DOM Parsing
- [ ] Why did you choose your parsing approach?
- [ ] What are the pros and cons of your method?
- [ ] How does it handle malformed XML?
- [ ] What are the performance implications?
- [ ] When would you use a different approach?
- [ ] How does it compare to other parsing methods?

## Time Estimate

### Message Queue
- Basic implementation: 30-45 minutes
- Error handling: 15-20 minutes
- Testing and refinement: 15-20 minutes
- Map reduce (extra credit): 30-45 minutes
- **Subtotal: 1-2 hours**

### DOM Parsing
- Parser implementation: 30-45 minutes
- Testing with both XML files: 15-20 minutes
- Documentation and discussion prep: 15-20 minutes
- **Subtotal: 1-1.5 hours**

### Total Time
- **Combined: 2-3.5 hours**

## Success Criteria

### Message Queue
- [ ] All assertions in runner.rb pass
- [ ] Multiple subscribers work correctly
- [ ] Error handling prevents cascade failures
- [ ] Code is clean and well-organized
- [ ] Design decisions are documented

### DOM Parsing
- [ ] All required operations implemented
- [ ] Works with both XML files
- [ ] Approach is well-reasoned
- [ ] Trade-offs are understood and documented
- [ ] Code is readable and maintainable

## Extra Credit Opportunities

### Message Queue
- [ ] Implement map-reduce functionality
- [ ] Add unsubscribe capability
- [ ] Add priority levels for messages
- [ ] Implement message filtering
- [ ] Add async message handling
- [ ] Create thread-safe version

### DOM Parsing
- [ ] Support CSS selectors
- [ ] Add XPath support
- [ ] Handle namespaces
- [ ] Implement element modification
- [ ] Add XML generation/serialization
- [ ] Create fluent API for queries

## Resources
- [Ruby Documentation](https://ruby-doc.org/)
- [REXML Tutorial](https://www.tutorialspoint.com/ruby/ruby_xml_xslt_xpath.htm)
- [Nokogiri Documentation](https://nokogiri.org/)
- [Ruby Blocks and Procs](https://www.rubyguides.com/2016/02/ruby-procs-and-lambdas/)

## Interview Preparation
- [ ] Be ready to explain your code
- [ ] Prepare to discuss alternative approaches
- [ ] Think about edge cases and limitations
- [ ] Consider how to extend functionality
- [ ] Be ready to refactor if needed
- [ ] Practice explaining trade-offs