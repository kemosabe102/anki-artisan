# Convert Slash Command

**Command to Convert**: $ARGUMENTS

## Instructions

1. Read the conversion template: `.claude/templates/command-conversion-prompt.template.md`
2. Read the source command file specified above
3. Read the reference implementation: `.claude/commands/git/git.md` and its `docs/` subdirectory
4. Execute the conversion following all rules in the template
5. Delete the original flat file after successful conversion
6. Report what was created and what was moved

## Documentation Handling

- If documentation is ONLY used by this command → MOVE it to the command's `docs/` subdirectory
- If documentation is used by MULTIPLE commands → COPY it (or keep reference link)
- Always check for other references before moving shared docs

## Delegate To

Use the appropriate agent (claude-code-ecosystem or workflow) to accomplish this work.
