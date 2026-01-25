# Output Templates for {{Agent Name}}

**Purpose**: Standard structure for all outputs from this agent

---

## Template Hierarchy

```
{{Agent Output}}
├── {{Section 1}} (if {{mode_1}} or {{mode_both}})
│   ├── {{Subsection A}}
│   └── {{Subsection B}}
├── {{Section 2}} (if {{mode_2}} or {{mode_both}})
│   ├── {{Subsection C}}
│   └── {{Subsection D}}
└── {{Metadata Section}}
```

---

## Section Templates

### {{Section 1 Name}}

```yaml
{{section_1}}:
  {{field_1}}: "{{Description of what goes here}}"
  {{field_2}}: "{{Description}}"
  {{field_list}}:
    - "{{Item description}}"
    - "{{Item description}}"
    - "{{Item description}}"
  {{nested_object}}:
    {{subfield_1}}: "{{Description}}"
    {{subfield_2}}: "{{Description}}"
```

**Field Requirements**:
- `{{field_1}}`: Required. {{Validation rules}}
- `{{field_2}}`: Required. {{Validation rules}}
- `{{field_list}}`: 2-5 items. {{Content guidance}}
- `{{nested_object}}`: Optional. Include when {{condition}}

### {{Section 2 Name}}

```yaml
{{section_2}}:
  - {{item_name}}: "{{Name}}"
    {{item_type}}: {{enum_value_1}} | {{enum_value_2}} | {{enum_value_3}}
    {{item_description}}: "{{1-2 sentences}}"
    {{item_details}}:
      - "{{Detail 1}}"
      - "{{Detail 2}}"
      - "{{Detail 3}}"
    {{item_connections}}: ["{{Related item 1}}", "{{Related item 2}}"]
```

**Format Rules**:
- Each item has: {{required fields list}}
- Description limited to {{character/sentence count}}
- Details: {{min}}-{{max}} bullet points
- Connections reference other items by name

---

## Metadata Template

```yaml
{{metadata_section}}:
  {{meta_field_1}}:
    - "{{Description of metadata item}}"
  {{meta_field_2}}:
    - "{{Description}}"
  {{meta_field_3}}:
    - "{{Description}}"
```

---

## Complete Example

Below is a minimal but complete example showing proper structure:

```yaml
# {{Example Title}}
# {{Context}}: {{Brief context description}}

{{section_1}}:
  {{field_1}}: "Example Value"
  {{field_2}}: "example"
  {{field_list}}:
    - "First item example"
    - "Second item example"
    - "Third item example"
  {{nested_object}}:
    {{subfield_1}}: "Nested value"
    {{subfield_2}}: "Another nested value"

{{section_2}}:
  - {{item_name}}: "Example Item"
    {{item_type}}: {{enum_value_1}}
    {{item_description}}: "Brief description of this item"
    {{item_details}}:
      - Specific detail one
      - Specific detail two
      - Specific detail three
    {{item_connections}}: ["Related Item A", "Related Item B"]

{{metadata_section}}:
  {{meta_field_1}}:
    - "Important note for user"
    - "Another important note"
  {{meta_field_2}}:
    - "Recommendation based on output"
```

---

## Output Quality Checklist

Before delivering output, verify:

- [ ] All required sections present for the active mode
- [ ] Each element uses {{output format}} not {{wrong format}}
- [ ] Lists limited to {{min}}-{{max}} items per section
- [ ] Descriptions concise ({{limit}})
- [ ] Connections reference valid items
- [ ] Metadata includes actionable recommendations
- [ ] Tone maintained consistently throughout

---

## Mode-Specific Variations

### Mode: {{mode_1}}

**Sections included**: {{section_1}}, {{metadata_section}}

**Sections excluded**: {{section_2}}

### Mode: {{mode_2}}

**Sections included**: {{section_2}}, {{metadata_section}}

**Sections excluded**: {{section_1}}

### Mode: {{mode_both}}

**Sections included**: ALL

**Order**: {{section_1}} first, then {{section_2}}, finally {{metadata_section}}
