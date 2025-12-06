## Description
<!-- Describe your changes in detail -->

## Type of Change
<!-- Mark the relevant option with an "x" -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🔧 Configuration change
- [ ] 🔒 Security update

## Checklist

### Code Quality
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings

### Testing
- [ ] I have tested my changes locally
- [ ] `terraform validate` passes
- [ ] `terraform plan` shows expected changes
- [ ] `make check` passes (validate, lint, security)

### Security
- [ ] `tfsec` scan passes with no HIGH/CRITICAL issues
- [ ] `tflint` passes with no errors
- [ ] No secrets or credentials in code
- [ ] Security implications have been considered

### Documentation
- [ ] I have updated the documentation accordingly
- [ ] I have updated the README if needed
- [ ] Architecture diagram reflects changes (if applicable)
- [ ] SECURITY.md updated if security-related

### Compliance
- [ ] Changes comply with AWS Well-Architected Framework
- [ ] Changes comply with CIS Controls (if applicable)
- [ ] Changes comply with NIST 800-53 (if applicable)

## Testing Evidence
<!-- Provide evidence of testing (screenshots, logs, etc.) -->

```bash
# Paste terraform plan output here
```

## Security Scan Results
<!-- Paste tfsec and tflint results -->

```bash
# tfsec results
```

```bash
# tflint results
```

## Additional Notes
<!-- Any additional information that reviewers should know -->

## Related Issues
<!-- Link to related issues: Fixes #123, Relates to #456 -->
