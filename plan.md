# Refactoring Plan for busylight-core

Based on my comprehensive analysis of the codebase, here's a prioritized
refactoring plan to improve maintainability and functionality:

## Executive Summary

The busylight-core codebase is well-structured with solid abstractions but has
accumulated technical debt through organic growth. Key areas for improvement
include reducing code duplication across vendors, standardizing color handling,
and improving the mixin architecture.

## Priority 1: High Impact, Low Risk

### 1.1 Add Human-Readable Word Representation (src/busylight_core/word.py)
- **Problem**: Word objects display as hex values, making debugging difficult
  when working with complex bit layouts
- **Solution**: Enhanced `__str__` method that uses introspection to show
  BitField names, ranges, and current values
- **Impact**: Easier debugging of vendor state objects without changing
  existing APIs or adding complexity

## Priority 2: Medium Impact, Medium Risk  

### 2.1 Create Vendor Base Classes
- **Problem**: Inconsistent inheritance patterns and naming
- **Solution**: Establish vendor-specific base classes:
  ```python
  class EmbravaLight(Light):
      vendor_name = "Embrava"
      
  class BlynclightBase(EmbravaLight):
      # Common Blynclight functionality
  ```
- **Impact**: Consistent hierarchy, easier to add new devices

### 2.2 Extract Common State Management Patterns
- **Problem**: Three different state management approaches across vendors
- **Solution**: Create template classes for common device types:
  - `SimpleRGBLight` - Basic color-only devices
  - `AudioEnabledLight` - Devices with sound capabilities  
  - `MultiLEDLight` - Devices with multiple controllable LEDs
- **Impact**: Faster new device implementation, consistent behavior

### 2.3 Standardize Async Task Management (mixins/taskable.py)
- **Enhancement**: Add task prioritization, better error handling
- **Problem**: Basic task management could be more robust
- **Impact**: More reliable light animations and effects

## Priority 3: Lower Impact, Higher Risk

### 3.1 Address Naming Inconsistencies
- **Problem**: Mix of `PascalCase`/`snake_case` in class names
- **Examples**: `Busylight_Alpha`, `Fit_StatUSB` vs `Blynclight`
- **Risk**: Breaking API changes for consumers
- **Approach**: Deprecation path with aliases

### 3.2 Platform-Specific Logic Refactoring (light.py:411-418)
- **Current**: Platform detection in `update()` method
- **Enhancement**: Extract to platform-specific strategy pattern
- **Impact**: Cleaner separation of concerns, easier testing

## Implementation Strategy

### Phase 1: Low-Risk Foundation
1. Add human-readable Word representation (`__str__` method)
2. Address naming inconsistencies across vendor classes
3. Create vendor base class hierarchy

### Phase 2: State Management Templates
1. Create device type templates (SimpleRGBLight, AudioEnabledLight,
   MultiLEDLight)
2. Migrate 1-2 vendors to new patterns as proof of concept
3. Update tests and documentation for new patterns

### Phase 3: Async and Platform Improvements
1. Standardize async task management (prioritization, error handling)
2. Extract platform-specific logic to strategy pattern
3. Add better diagnostics for Windows USB I/O issues

## Risk Mitigation

- **Backward Compatibility**: All changes maintain existing public APIs
- **Incremental Approach**: Each phase can be released independently
- **Test Coverage**: Maintain >90% coverage throughout refactoring
- **Documentation**: Update examples and docs with each phase

## Key Benefits

1. **Maintainability**: ~30% reduction in duplicated code
2. **Extensibility**: Faster new device support (template-based)
3. **Consistency**: Unified patterns across all vendors
4. **Developer Experience**: Better error messages, clearer abstractions
5. **Performance**: More efficient bit operations and state management

The plan prioritizes changes with high impact and low risk first, ensuring the
codebase remains stable while systematically improving its structure.