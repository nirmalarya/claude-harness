# Useful Claude Skills for Autonomous Coding

**Sources:**
- Official: https://github.com/anthropics/skills/tree/main/skills
- Community: https://github.com/ComposioHQ/awesome-claude-skills

---

## 🎯 Priority Skills for autonomous-harness

### Tier 1: Critical for Code Quality (Must Have)

**1. Python Best Practices**
- **Source:** Anthropic official skills
- **Use:** FastAPI, Django, Flask patterns
- **Why:** SHERPA, AutoGraph use Python backends
- **Path:** `~/.claude/skills/python-best-practices/`

**2. Testing Patterns**
- **Source:** Anthropic official skills  
- **Use:** pytest, unittest, test organization
- **Why:** Prevent untested code (SHERPA/AutoGraph had this issue)
- **Path:** `~/.claude/skills/testing-patterns/`

**3. Security Patterns**
- **Source:** Anthropic official skills
- **Use:** Authentication, authorization, input validation
- **Why:** Critical for production apps (AutoGraph had security bugs!)
- **Path:** `~/.claude/skills/security-patterns/`

**4. API Design**
- **Source:** Anthropic official skills
- **Use:** REST, GraphQL, OpenAPI specs
- **Why:** SHERPA & AutoGraph are API-heavy
- **Path:** `~/.claude/skills/api-design/`

### Tier 2: Productivity (High Value)

**5. Code Organization**
- **Source:** Community skills
- **Use:** File structure, module organization
- **Why:** Fix SHERPA's 150+ files in root issue!
- **Path:** `~/.claude/skills/code-organization/`

**6. Error Handling**
- **Source:** Anthropic official skills
- **Use:** Try/except patterns, logging
- **Why:** Production-grade error handling
- **Path:** `~/.claude/skills/error-handling/`

**7. Documentation**
- **Source:** Community skills
- **Use:** Docstrings, README, API docs
- **Why:** Generate comprehensive docs automatically
- **Path:** `~/.claude/skills/documentation/`

**8. Performance Optimization**
- **Source:** Community skills
- **Use:** Database queries, caching, async patterns
- **Why:** Production performance requirements
- **Path:** `~/.claude/skills/performance/`

### Tier 3: Framework-Specific

**9. FastAPI Patterns**
- **Source:** Community skills
- **Use:** Dependency injection, middleware, Pydantic
- **Why:** SHERPA & AutoGraph use FastAPI
- **Path:** `~/.claude/skills/fastapi/`

**10. React Best Practices**
- **Source:** Community skills
- **Use:** Hooks, components, state management
- **Why:** SHERPA & AutoGraph frontends
- **Path:** `~/.claude/skills/react/`

**11. Next.js Patterns**
- **Source:** Community skills
- **Use:** App router, API routes, SSR
- **Why:** AutoGraph uses Next.js
- **Path:** `~/.claude/skills/nextjs/`

**12. Database Patterns**
- **Source:** Anthropic official skills
- **Use:** SQLAlchemy, migrations, optimization
- **Why:** Both projects use databases
- **Path:** `~/.claude/skills/database/`

### Tier 4: DevOps & Deployment

**13. Docker & Kubernetes**
- **Source:** Community skills
- **Use:** Containerization, orchestration
- **Why:** Production deployment (SHERPA v1.1)
- **Path:** `~/.claude/skills/docker-k8s/`

**14. CI/CD Patterns**
- **Source:** Community skills
- **Use:** GitHub Actions, testing pipelines
- **Why:** Automated quality gates
- **Path:** `~/.claude/skills/cicd/`

**15. Monitoring & Logging**
- **Source:** Community skills
- **Use:** Structured logging, metrics, alerts
- **Why:** Production observability
- **Path:** `~/.claude/skills/monitoring/`

---

## 📦 Skills We Should Create (Bayer-Specific)

**Custom Skills for Our Needs:**

### 1. Bayer Security Standards
```markdown
# Skill: Bayer Security Standards
## When to use
All Bayer production applications
## Requirements
- OAuth2 with Azure AD
- Secret scanning (detect-secrets)
- Security headers (OWASP)
- Audit logging
- Rate limiting
## Code Examples
[FastAPI + Azure AD integration]
```

### 2. Autonomous Coding Quality Gates
```markdown
# Skill: Autonomous Coding Quality
## When to use
Building with autonomous-harness
## Rules
- Max 15 files in root directory
- All tests in tests/ subdirectory
- Zero TODOs in passing features
- All passwords hashed (bcrypt cost 12)
- No credentials in URLs/logs
## File Organization
[Standard project structure]
```

### 3. Bayer Data Privacy
```markdown
# Skill: GDPR & Data Privacy
## When to use
Any application handling personal data
## Requirements
- User consent mechanisms
- Data retention policies
- Right to deletion
- Data encryption at rest
- PII masking in logs
```

---

## 🚀 Implementation Plan

### Phase 1: Clone Official Skills (Now)
```bash
# Create skills directory
mkdir -p ~/.claude/skills

# Clone official Anthropic skills
git clone https://github.com/anthropics/skills.git /tmp/claude-skills
cp -r /tmp/claude-skills/skills/* ~/.claude/skills/

# Verify
ls ~/.claude/skills/
```

### Phase 2: Add Community Skills (Week 1)
```bash
# Review awesome-claude-skills
# Select most starred/useful ones
# Copy to ~/.claude/skills/
```

### Phase 3: Create Custom Skills (Week 2)
```bash
# Create Bayer-specific skills
mkdir -p ~/.claude/skills/bayer/
# [Create security, privacy, quality skills]

# Create autonomous-harness skills
mkdir -p ~/.claude/skills/autonomous-harness/
# [Create quality gates, file org skills]
```

### Phase 4: Integrate with Harness (v2.0)
```python
# In client.py
def load_claude_skills():
    skills_dir = Path.home() / ".claude" / "skills"
    skills = []
    
    # Load all .md files from skills directory
    for skill_file in skills_dir.rglob("*.md"):
        skills.append(skill_file.read_text())
    
    return "\n\n".join(skills)

# In prompts
SKILLS_SECTION = load_claude_skills()
```

---

## 📊 Expected Impact

**With Skills Integration:**

| Metric | Without Skills | With Skills | Improvement |
|--------|---------------|-------------|-------------|
| Code Quality | B+ (8.5/10) | A (9.5/10) | +1.0 |
| Security Issues | 3-5 per build | 0-1 per build | -80% |
| File Organization | Messy (150+ files) | Clean (<20 files) | Perfect |
| TODOs in Code | 30+ | 0 | Perfect |
| Test Coverage | 70% | 95%+ | +25% |
| Production Ready | Manual cleanup | Immediate | 10x faster |

**ROI:**
- 2-3 hours to integrate skills
- Save 5-10 hours per project cleanup
- **Break even after 1 project!**

---

## 🎯 Next Steps

1. **Review official skills:** https://github.com/anthropics/skills
2. **Review awesome list:** https://github.com/ComposioHQ/awesome-claude-skills
3. **Select top 15** most relevant skills
4. **Clone to ~/.claude/skills/**
5. **Test with autonomous-harness v2.0**
6. **Create custom Bayer skills**

---

## 📚 Resources

- Official Skills: https://github.com/anthropics/skills
- Awesome List: https://github.com/ComposioHQ/awesome-claude-skills
- Claude Skills Docs: https://docs.anthropic.com/claude/docs/skills
- Our Integration Guide: `docs/v2/CLAUDE_SKILLS_INTEGRATION.md`

