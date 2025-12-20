# A simple message queue that broadcasts published messages of a certain type to others listening to that type.
# NOTE: You don't need to change this module. Implement SimpleMessageQueue below.
module MessageQueue
  # Receiver will be called (with optional data) when an event of this type is received.
  # The method accepts one or more message types (either a string or an array of strings) followed by a block
  # NOTE: You can change method contract when you implement it
  def subscribe
    raise "implement!"
  end

  # Sends a notification to all registered listeners for the given type.
  # If a receiver acts badly, others should not be effected.
  def publish(type, data = nil)
    raise "implement!"
  end
end

# BEGIN CODE TO IMPLEMENT

# Implement this class
class SimpleMessageQueue
  include MessageQueue

  def initialize
    @subscribers = Hash.new { |hash, key| hash[key] = [] }
  end

  # Subscribe to one or more message types
  # Accepts either a single type (string) or array of types
  def subscribe(*types, &block)
    types = types.flatten
    types.each do |type|
      @subscribers[type] << block
    end
  end

  # Publish a message to all subscribers of that type
  # Handles exceptions in individual subscribers gracefully
  def publish(type, data = nil)
    return unless @subscribers[type]
    
    @subscribers[type].each do |subscriber|
      begin
        subscriber.call(data)
      rescue => e
        # Silently catch exceptions so other subscribers can continue
        # In production, you might want to log this
      end
    end
  end
end

# Extra credit!!! check out map_reduce.rb...

# END CODE TO IMPLEMENT
