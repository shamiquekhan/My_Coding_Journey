#!/bin/bash
# initialize_repo.sh
# This script sets up a new Git repository with:
# - Conventional commit guidelines
# - Git hooks
# - Branch protection CODEOWNERS
# - Pull Request template

# Create Conventional Commit structure
echo "# Conventional Commits" > COMMIT_CONVENTION.md
cat <<EOT >> COMMIT_CONVENTION.md
feat:     A new feature
fix:      A bug fix
docs:     Documentation changes
style:    Code formatting, white-space, etc
refactor: Code restructuring without behavior changes
test:     Adding or updating tests
chore:    Maintenance tasks (build, dependencies)
EOT

# Setup Git hooks
mkdir -p .githooks
cat <<'EOT' > .githooks/pre-commit
#!/bin/sh
# Example pre-commit hook: run linter
npm run lint
EOT
chmod +x .githooks/pre-commit

git config core.hooksPath .githooks

# Create CODEOWNERS for branch protection
mkdir -p .github
echo "# Branch Protection Rules" > .github/CODEOWNERS
echo "* @yourusername" >> .github/CODEOWNERS

# Create Pull Request template
cat <<EOT > .github/pull_request_template.md
# Pull Request Template

## Description

Please describe your changes clearly.

## Related Issues

Fixes #

## Checklist

- [ ] I have tested my changes
- [ ] I followed the coding standards
- [ ] I updated documentation if necessary
EOT

echo "✅ Repository initialization complete."

- [ ] Tests added
- [ ] Documentation updated
- [ ] Code linted
" > .github/pull_request_template.md
