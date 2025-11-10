# Module 5: Sentinel Values vs Exceptions; Logging Basics - Extra Exercises

## Overview

These extra exercises provide additional practice with sentinel values, exceptions, and logging patterns. They range from basic reinforcement exercises to advanced scenarios that challenge you to make sophisticated design decisions.

## Basic Reinforcement Exercises

### Exercise 1: Cache Manager
Implement a `CacheManager` class that demonstrates both sentinel and exception patterns:

**Requirements:**
- `get(key)` → Returns cached value or None (sentinel)
- `get_required(key)` → Returns cached value or raises `CacheError` (exception)
- `set(key, value, ttl=None)` → Cache with optional time-to-live
- `clear_expired()` → Remove expired entries, return count removed

**Error Handling Strategy:**
- Missing optional cache entries → None (sentinel)
- Missing required cache entries → CacheError (exception)
- Invalid TTL values → ValueError (exception)
- Cache size limits exceeded → automatic eviction (no error)

**Logging Strategy:**
- INFO: Cache hits, successful sets, cleanup operations
- WARNING: Cache misses on required keys, near-capacity warnings
- DEBUG: Individual cache operations and TTL calculations

### Exercise 2: Feature Flag Manager
Create a `FeatureFlagManager` that handles application feature toggles:

**Requirements:**
- `is_enabled(flag_name, default=False)` → Boolean or default (sentinel pattern)
- `require_flag(flag_name)` → Boolean or raises `FeatureFlagError` (exception pattern)
- `set_flag(flag_name, enabled, metadata=None)` → Set flag with metadata
- `get_flag_metadata(flag_name)` → Return metadata or empty dict (sentinel)

**Challenge:** Implement different error handling for user vs system flags.

### Exercise 3: Connection Pool Manager
Implement a `ConnectionPoolManager` for database connections:

**Requirements:**
- `get_connection()` → Return connection or None (sentinel)
- `get_connection_required()` → Return connection or raise `PoolExhaustedError`
- `return_connection(conn)` → Return connection to pool
- `health_check()` → Return pool statistics

**Advanced Challenge:** Implement connection health checking and automatic retry logic.

## Intermediate Challenge Exercises

### Exercise 4: Multi-Source Configuration
Extend your configuration manager to load from multiple sources with precedence:

**Sources (in precedence order):**
1. Environment variables (highest priority)
2. Command line arguments
3. Configuration files
4. Default values (lowest priority)

**Requirements:**
- `get_from_source(key, source)` → Value or None per source
- `get_effective(key)` → Final value after precedence resolution
- `get_source_chain(key)` → List showing value source precedence
- `validate_required_config()` → Validate all required settings exist

**Error Handling Strategy:**
- Missing optional config → Use next source in chain → Default → None
- Missing required config → ConfigurationError with source information
- Invalid config format → Warning + skip source
- Source unavailable → Debug log + skip source

### Exercise 5: Batch Data Processor
Create a robust batch processing system with sophisticated error handling:

**Requirements:**
- `process_batch(items, processor_func)` → (successes, failures, stats)
- `process_with_retry(items, max_retries=3)` → Retry failed items
- `process_parallel(items, worker_count=4)` → Parallel processing
- `get_processing_report()` → Detailed processing statistics

**Error Handling Strategy:**
- Individual item failures → Collect in failures list (continue processing)
- Temporary failures → Add to retry queue
- Permanent failures → Log error + add to permanent failures
- System failures → Raise ProcessingError (stop processing)

**Logging Strategy:**
- INFO: Batch start/completion, statistics
- WARNING: Individual item failures, retry attempts
- ERROR: System failures, retry exhaustion
- DEBUG: Individual item processing traces

### Exercise 6: API Response Handler
Design an API client that handles various response scenarios:

**Requirements:**
- `get_data(endpoint)` → Data or None for optional endpoints
- `get_required_data(endpoint)` → Data or raise APIError for critical endpoints
- `post_data(endpoint, data)` → Success boolean for fire-and-forget
- `put_data_required(endpoint, data)` → Data or raise for critical updates

**Status Code Handling:**
- 200-299: Success (return data)
- 404 on optional endpoint: None (sentinel)
- 404 on required endpoint: APIError (exception)
- 429 (rate limit): Automatic retry with backoff
- 500-599: APIError (server error)

## Advanced Integration Exercises

### Exercise 7: Event-Driven System Monitor
Build a system monitoring service with event-driven architecture:

**Components:**
- `EventCollector` → Collects system events
- `EventProcessor` → Processes events with rules
- `AlertManager` → Manages alert generation and delivery
- `MetricsAggregator` → Aggregates metrics over time windows

**Error Handling Strategies:**
- Missing optional metrics → Use default values (sentinel)
- Critical system metrics missing → Raise AlertError (exception)
- Event processing failures → Dead letter queue (hybrid)
- Alert delivery failures → Retry with exponential backoff

**Logging Integration:**
- Structured logging with event correlation IDs
- Different log levels for different event severities
- Performance metrics logging
- Alert delivery status logging

### Exercise 8: Multi-Tenant Resource Manager
Create a resource management system for a multi-tenant application:

**Requirements:**
- `allocate_resource(tenant_id, resource_type, amount)` → Resource ID or None
- `require_resource(tenant_id, resource_type, amount)` → Resource ID or exception
- `release_resource(resource_id)` → Success boolean
- `get_tenant_usage(tenant_id)` → Usage statistics or empty dict

**Complex Error Handling:**
- Insufficient resources for optional allocation → None (sentinel)
- Insufficient resources for required allocation → ResourceError (exception)
- Tenant quota exceeded → QuotaExceededError (exception)
- Invalid tenant ID → ValidationError (exception)
- Resource cleanup failures → Warning logs (continue operation)

**Advanced Logging:**
- Tenant-specific log correlation
- Resource allocation/deallocation audit trails
- Quota monitoring and alerting
- Performance metrics by tenant

## Design Challenge Exercises

### Exercise 9: Smart Error Recovery System
Design a system that automatically chooses between sentinel values and exceptions based on context:

**Context Factors:**
- Operation criticality (optional vs required)
- User type (admin vs regular user)
- System load (graceful degradation)
- Error frequency (circuit breaker pattern)

**Implementation Challenge:**
Create a decorator that automatically applies appropriate error handling based on these factors.

### Exercise 10: Adaptive Logging Framework
Build a logging system that adapts its behavior based on system conditions:

**Adaptive Behaviors:**
- Log level adjustment based on error rates
- Automatic log rotation based on disk space
- Performance-based log sampling (log every Nth operation under load)
- Context-aware log formatting (detailed for errors, concise for info)

**Integration Challenge:**
Integrate this with all your previous exercises to demonstrate adaptive logging in various scenarios.

## Evaluation Guidelines

### Basic Exercises (1-3)
- **Correctness (40%):** Proper implementation of required methods
- **Pattern Usage (30%):** Appropriate choice of sentinel vs exception patterns
- **Code Quality (20%):** Clean, readable code under 50 lines
- **Logging Integration (10%):** Basic logging at appropriate levels

### Intermediate Exercises (4-6)
- **Design Quality (35%):** Well-thought-out error handling strategies
- **Pattern Consistency (25%):** Consistent application of chosen patterns
- **Error Recovery (20%):** Robust error handling and recovery mechanisms
- **Logging Strategy (20%):** Comprehensive logging with appropriate levels

### Advanced Exercises (7-10)
- **Architectural Quality (30%):** Well-designed system architecture
- **Error Handling Sophistication (25%):** Advanced error handling techniques
- **Integration Complexity (25%):** Complex component interactions
- **Innovation (20%):** Creative solutions and adaptive behaviors

## Learning Reflection

After completing these exercises, reflect on:

1. **Pattern Selection:** When did you choose sentinel values vs exceptions? Why?
2. **Consistency:** How did you maintain consistent error handling within classes?
3. **User Experience:** How do your error handling choices affect the user experience?
4. **Debugging:** How does your logging strategy help with debugging and monitoring?
5. **Evolution:** How would you modify your designs as requirements change?

## Real-World Applications

These exercises prepare you for real-world scenarios such as:

- **Microservice Communication:** Handling service failures gracefully
- **Data Pipeline Processing:** Robust batch processing with error recovery
- **Configuration Management:** Multi-environment configuration handling
- **Resource Management:** Cloud resource allocation and management
- **Monitoring Systems:** Event processing and alerting systems
- **API Development:** Client-friendly error handling and logging

The key insight is that defensive programming isn't just about preventing errors—it's about designing systems that handle errors gracefully, provide meaningful feedback, and maintain operational visibility through effective logging.