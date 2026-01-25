# Reliability Reviewer Examples

## Example Invocation

```markdown
Task(reliability-reviewer, prompt="Analyze reliability for integration pair:
{
  \"id\": 1,
  \"upstream\": \"PerplexityProvider\",
  \"downstream\": \"Normalizer\",
  \"upstream_file\": \"packages/connectors/perplexity_provider.py\",
  \"downstream_file\": \"packages/processing/normalizer.py\",
  \"data_flow_type\": \"direct\"
}")
```

## Example Output

See `reliability-reviewer.md` Output Format section for complete example.
