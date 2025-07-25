# Vendor Lights Classes Implementation TODOs

## High Priority - Testing

- [ ] **Update existing tests to validate new vendor Lights classes functionality** 
  - Ensure existing test suite continues to pass with new vendor classes
  - Update any tests that may be affected by the new import structure

- [ ] **Add comprehensive tests for vendor-specific all_lights() and first_light() methods**
  - Test `EmbravaLights.all_lights()` returns only Embrava devices
  - Test `KuandoLights.first_light()` returns first Kuando device
  - Test all vendor Lights classes have working methods

- [ ] **Create tests to verify vendor Lights classes return only their vendor's devices**
  - Mock multiple vendor devices and ensure isolation
  - Test that EmbravaLights doesn't return Luxafor devices, etc.
  - Verify vendor filtering works correctly

- [ ] **Verify backward compatibility with existing Light.all_lights() usage**
  - Ensure `Light.all_lights()` still returns all devices from all vendors
  - Verify `Light.first_light()` still works as before
  - Test that existing code patterns continue to work

## Medium Priority - Documentation

- [ ] **Update device capabilities documentation with vendor Lights class examples**
  - Replace current examples in device-capabilities.md
  - Show vendor-specific access patterns
  - Update usage examples for each vendor section

- [ ] **Update quickstart guide examples to show vendor-specific access patterns**
  - Add examples of `EmbravaLights.first_light()`
  - Show both unified and vendor-specific approaches
  - Demonstrate practical use cases

- [ ] **Update README examples to demonstrate new vendor Lights class usage**
  - Add vendor-specific examples to README
  - Show how to work with specific vendor collections
  - Update documentation links section

## Low Priority - Integration

- [ ] **Add vendor Lights classes to mkdocs API reference navigation**
  - Ensure new classes appear in generated API docs
  - Update navigation structure if needed
  - Verify proper cross-linking

---

## Implementation Notes

### New Capability Examples:
```python
# Vendor-specific access (new)
embrava_lights = EmbravaLights.all_lights()
first_kuando = KuandoLights.first_light()

# Unified access (unchanged)
all_lights = Light.all_lights()
first_light = Light.first_light()
```

### Available Vendor Classes:
- `AgileInnovativeLights`
- `CompuLabLights` 
- `EmbravaLights`
- `EPOSLights`
- `KuandoLights`
- `LuxaforLights`
- `MuteMeLights`
- `PlantronicsLights`
- `ThingMLights`