# Ruby Interview Tests - Implementation Notes

## Overview
This document summarizes the implementation approach and key decisions for both Ruby interview tests: the message queue system and the DOM parser.

## Test 1: Message Queue Implementation

### Approach
Implemented a pub/sub (publish-subscribe) message queue system that allows:
- Multiple subscribers to listen to specific message types
- Broadcasting messages to all registered listeners
- Graceful error handling (one subscriber's failure doesn't affect others)
- Support for subscribing to multiple message types with a single handler

### Implementation Details

#### Data Structure
- Used a `Hash` with default value of empty array: `Hash.new { |hash, key| hash[key] = [] }`
- Keys are message types (strings)
- Values are arrays of subscriber blocks/procs

#### Key Methods

**`subscribe(*types, &block)`**
- Accepts variable number of message types (supports both single type and arrays)
- Flattens array to handle `["type1", "type2"]` syntax
- Stores the block for each type in the subscribers hash

**`publish(type, data = nil)`**
- Retrieves all subscribers for the given type
- Iterates through each subscriber and calls it with the data
- Wraps each call in `begin/rescue` to catch exceptions
- Silently continues if a subscriber fails (as per requirements)

### Design Decisions

**Why Hash with Array Values?**
- O(1) lookup for subscribers by type
- Supports multiple subscribers per type naturally
- Easy to iterate through all subscribers

**Error Handling Strategy**
- Used `begin/rescue` to catch all exceptions
- Silently swallows errors to prevent one bad subscriber from affecting others
- In production, would log these errors for debugging

**Flexibility**
- Supports both single type: `subscribe "foo"`
- And multiple types: `subscribe ["foo", "bar"]`
- Uses splat operator and flatten for maximum flexibility

## Test 2: DOM Parser Implementation

### Approach
Implemented an XML/DOM parser using Ruby's built-in REXML library that can:
- Find all elements by tag name
- Find elements by attribute value
- Find elements by child element value
- Demonstrate XPath-like querying capabilities

### Implementation Details

#### Parser Class: `SimpleDOMParser`

**`initialize(file)`**
- Creates REXML::Document from file
- Stores document for subsequent queries

**`find_all(tag_name)`**
- Uses XPath syntax: `//tag_name` to find all matching elements
- Returns array of REXML::Element objects
- Handles nested elements automatically

**`find_by_attribute(tag_name, attr_name, attr_value)`**
- Uses XPath attribute selector: `//tag[@attr='value']`
- Returns first matching element or nil
- Efficient for unique attribute queries (like IDs)

**`find_by_child_value(tag_name, child_name, child_value)`**
- Manually iterates through elements
- Checks child element text content
- Returns array of all matching elements
- More flexible than pure XPath for complex conditions

### Design Decisions

**Why REXML?**
- Built into Ruby standard library (no external dependencies)
- Well-documented and stable
- Supports XPath queries natively
- Good balance of simplicity and power

**Alternative Approaches Considered**
1. **Nokogiri**: More powerful but requires external gem
2. **Manual parsing**: More control but much more complex
3. **SAX parsing**: Better for large files but more complex API

**XPath vs Manual Iteration**
- Used XPath for simple queries (tag name, attributes)
- Used manual iteration for complex logic (child value matching)
- Provides good balance of readability and flexibility

### Demonstration Output
The runner script demonstrates all required capabilities:
1. ✅ Find all 12 book elements
2. ✅ Find all 12 author elements  
3. ✅ Find book with id="bk103" (Maeve Ascendant)
4. ✅ Find all 4 Fantasy genre books

## Extra Credit: Map/Reduce Implementation

### Approach
Used the message queue to implement a map/reduce pattern for calculating statistics on even/odd numbers.

### Implementation

**Map Phase**
- Iterate through all values
- Determine if each value is even or odd
- Publish to appropriate channel ("even" or "odd")

**Reduce Phase**
- Subscribe to both "even" and "odd" channels
- Accumulate sum and count for each type
- Calculate averages after all values processed

### Key Insight
The message queue naturally supports map/reduce:
- **Map**: Publishing partitions data
- **Reduce**: Subscribers aggregate results
- **Parallel-ready**: Could easily distribute subscribers across processes

### Results
Successfully processes 1000 values:
- Correctly partitions into even/odd
- Calculates accurate sums, counts, and averages
- Demonstrates practical use of the message queue

## Testing Approach

### Message Queue Tests
- 7 test cases covering:
  - Basic pub/sub
  - Multiple event types
  - Multiple subscribers
  - Error handling
  - Multi-type subscription
  - Order preservation

### DOM Parser Tests
- 4 assertions verifying:
  - Correct element counts
  - Attribute-based lookup
  - Child value filtering
  - Data accuracy

## Code Quality

### Ruby Best Practices
- Used blocks/procs for callbacks (idiomatic Ruby)
- Leveraged Hash default values
- Used splat operators for flexibility
- Clear, descriptive method names
- Minimal but sufficient error handling

### Documentation
- Inline comments for complex logic
- Clear method signatures
- Demonstration scripts with output
- Comprehensive test coverage

## Potential Improvements

### Message Queue
1. **Priority queues**: Support message priorities
2. **Async processing**: Thread pool for subscribers
3. **Message persistence**: Store messages for replay
4. **Dead letter queue**: Handle failed messages
5. **Metrics**: Track publish/subscribe statistics

### DOM Parser
1. **CSS selectors**: Support CSS-style queries
2. **Modification**: Add methods to modify/create elements
3. **Validation**: XML schema validation
4. **Streaming**: SAX-style parsing for large files
5. **Namespaces**: Better namespace handling

## Conclusion

Both implementations demonstrate:
- ✅ Clean, idiomatic Ruby code
- ✅ Proper use of Ruby's built-in features
- ✅ Solid understanding of design patterns
- ✅ Practical problem-solving approach
- ✅ Good balance of simplicity and functionality

The message queue is production-ready for simple use cases, and the DOM parser effectively demonstrates XML querying capabilities using Ruby's standard library.