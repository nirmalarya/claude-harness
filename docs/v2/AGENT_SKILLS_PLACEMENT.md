# Agent Skills - Placement Strategy

**Question:** Where should Agent Skills live - Harness or SHERPA?

**Answer:** Both! Start in harness (testing), then SHERPA provides them (production)

---

## 🎯 Phase 1: Harness-Level Skills (v2.0 - Testing)

**For standalone harness testing:**

**Location:** `~/.skills/` (user-level)

**Why start here:**
- ✅ Test skills work with harness
- ✅ Validate skills improve quality
- ✅ Iterate on skill design
- ✅ No SHERPA dependency

**Structure:**
```
~/.skills/                    # User skills directory
├── security-patterns/
│   └── SKILL.md             # Security best practices
├── testing-patterns/
│   └── SKILL.md             # Testing templates
├── database-patterns/
│   └── SKILL.md             # DB best practices
├── api-design/
│   └── SKILL.md             # REST/GraphQL patterns
└── fastapi-patterns/
    └── SKILL.md             # FastAPI specific
```

**Harness code:**
```python
# In autonomous-harness/client.py

def load_agent_skills():
    """Load Agent Skills from ~/.skills/ directory."""
    skills_dir = Path.home() / ".skills"
    
    if not skills_dir.exists():
        return ""
    
    skills_content = []
    for skill_folder in skills_dir.iterdir():
        if not skill_folder.is_dir():
            continue
        
        skill_file = skill_folder / "SKILL.md"
        if skill_file.exists():
            content = skill_file.read_text()
            skills_content.append(f"\n## Skill: {skill_folder.name}\n\n{content}")
    
    return "\n".join(skills_content)

# Inject into system prompt
def build_prompt_with_skills(base_prompt):
    skills = load_agent_skills()
    if skills:
        return base_prompt + f"\n\n---\n\n## AVAILABLE SKILLS\n\n{skills}\n\n---\n"
    return base_prompt
```

**Testing (v2.0):**
```bash
# Test harness with skills
cd autonomous-harness

# Ensure skills loaded
python3 autonomous_agent.py --project-dir ./test-project

# Harness will:
# 1. Load skills from ~/.skills/
# 2. Inject into prompts
# 3. Agent follows skill patterns
# 4. Better code quality!
```

---

## 🎯 Phase 2: SHERPA-Provided Skills (v1.1 - Production)

**When embedding harness in SHERPA:**

**SHERPA becomes the skills provider!**

**SHERPA's knowledge hierarchy:**
```
SHERPA Knowledge Layer
├── Built-in skills (7 default skills)
├── ORG skills (S3/Bedrock or Qdrant)
├── PROJECT skills (./sherpa/snippets/)
└── LOCAL skills (./sherpa/snippets.local/)

Priority: LOCAL > PROJECT > ORG > BUILT-IN
```

**Integration:**
```python
# In SHERPA (v1.1)

class SHERPAOrchestrator:
    def run_autonomous_build(self, spec):
        # 1. SHERPA gathers all knowledge
        knowledge = self.knowledge_manager.get_all_snippets()
        
        # 2. Convert SHERPA knowledge → Agent Skills format
        skills = self.convert_to_agent_skills(knowledge)
        
        # 3. Pass to embedded harness
        from autonomous_harness import AutonomousAgent
        
        agent = AutonomousAgent(
            spec=spec,
            skills=skills,  # SHERPA provides skills!
            quality_gates=True
        )
        
        agent.build()
    
    def convert_to_agent_skills(self, snippets):
        """Convert SHERPA snippets to Agent Skills format."""
        skills = []
        
        for snippet in snippets:
            # Convert SHERPA snippet → SKILL.md format
            skill = f"""
# Skill: {snippet.title}

## When to use
{snippet.when_to_use}

## Pattern
{snippet.code}

## Best Practices
{snippet.best_practices}
"""
            skills.append(skill)
        
        return "\n\n".join(skills)
```

**Flow:**
```
User → SHERPA → Gathers knowledge → Converts to skills → 
Passes to harness → Harness uses skills → Better code!
```

---

## 📊 Skills Strategy Summary

### Now (Testing Phase)
**Location:** Harness level (`~/.skills/`)
- Harnesses load skills independently
- Test skills improve quality
- Validate Agent Skills standard works
- Iterate on skill design

**Why:** Test without SHERPA dependency

---

### Later (Production Phase - SHERPA v1.1)
**Location:** SHERPA provides skills to harness
- SHERPA's knowledge layer
- Organizational snippets → Skills format
- Passed to embedded harness
- Hierarchy: LOCAL > PROJECT > ORG > BUILT-IN

**Why:** SHERPA is the knowledge platform

---

## 🎯 Revised V2.0 Harness Scope

**autonomous-harness v2.0 (Focused Scope!):**

### Core Executor Features
1. ✅ Take spec → Generate features
2. ✅ Implement features (any tech stack)
3. ✅ Run tests (unit, integration, E2E)
4. ✅ Validate quality (database, services, security)
5. ✅ Commit progress
6. ✅ Support modes (greenfield, enhancement, bugfix)

### Quality Gates (NEW!)
7. ✅ Database schema validation
8. ✅ Service health checks
9. ✅ E2E testing framework
10. ✅ Regression testing
11. ✅ Browser integration testing
12. ✅ Security checklist
13. ✅ Zero TODOs enforcement
14. ✅ Stop condition

### Skills Support (NEW!)
15. ✅ Load Agent Skills from `~/.skills/`
16. ✅ Inject into prompts
17. ✅ **OR** accept skills from caller (SHERPA!)

**NOT in scope:**
- ❌ Requirements gathering (SHERPA!)
- ❌ Architecture design (SHERPA!)
- ❌ Tracker integration (SHERPA!)
- ❌ Knowledge management (SHERPA!)

---

## 🎯 Integration Pattern

### Standalone Use (Testing/Development)
```bash
cd autonomous-harness

# Harness loads skills from ~/.skills/
python3 autonomous_agent.py \
  --project-dir ./my-project \
  --spec my_spec.txt
```

### Embedded in SHERPA (Production)
```python
# In SHERPA

# SHERPA provides skills to harness
skills = sherpa.get_knowledge_as_skills()

harness = AutonomousHarness(
    spec=sherpa_generated_spec,
    skills=skills,  # From SHERPA!
    quality_gates=True
)

harness.execute()
```

**Harness is flexible - works both ways!**

---

## 📋 Updated Roadmap

### Week 1-2: autonomous-harness v2.0 (Focused!)
**Add quality gates:**
- Database validation
- Service health
- E2E testing
- Regression testing
- Agent Skills support (load from ~/.skills/)

**Test standalone:**
- Simple projects
- Complex projects (AutoGraph!)
- Verify quality gates work

---

### Week 3: cursor-autonomous-coding v2.0
**Same quality gates, Cursor CLI**

---

### Week 4: Use v2.0 on AutoGraph
**Fix AutoGraph with quality-enforced harness**

---

### Week 5: SHERPA v1.1 - Embed Improved Harnesses
**SHERPA enhancements:**
- Embed autonomous-harness v2.0 (quality gates!)
- Embed cursor-harness v2.0 (quality gates!)
- SHERPA provides skills to harnesses
- Test full integration

**SHERPA calls harnesses, provides knowledge!**

---

## ✅ Clear Architecture

```
┌─────────────────────────────────────────┐
│           SHERPA v1.1                   │
│  (Orchestration & Knowledge Platform)   │
├─────────────────────────────────────────┤
│                                         │
│  Requirements → Architecture → Spec     │
│  Knowledge Base (snippets)              │
│  Tracker Integration (Azure DevOps)     │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Converts Knowledge → Skills      │ │
│  └───────────────────────────────────┘ │
│                ↓                        │
│  ┌───────────────────────────────────┐ │
│  │  Embedded Harnesses (v2.0)        │ │
│  │  ┌─────────────────────────────┐  │ │
│  │  │ autonomous-harness          │  │ │
│  │  │ - Takes: spec + skills      │  │ │
│  │  │ - Does: code + test + val   │  │ │
│  │  │ - Quality gates enforced    │  │ │
│  │  └─────────────────────────────┘  │ │
│  │  ┌─────────────────────────────┐  │ │
│  │  │ cursor-harness              │  │ │
│  │  │ - Same as above, Cursor CLI │  │ │
│  │  └─────────────────────────────┘  │ │
│  └───────────────────────────────────┘ │
│                ↓                        │
│  Monitors Progress → Syncs to Trackers │
└─────────────────────────────────────────┘
```

---

## 🎊 Corrected Vision

**SHERPA:** The platform (orchestration, knowledge, SDLC)  
**Harnesses:** The executors (quality-focused coding)  
**Agent Skills:** Start in harness (~/.skills/), later SHERPA provides them

**No conflict - clean separation of concerns!** ✅

---

**Tomorrow: Improve harnesses with RIGHT scope (execution quality, not full SDLC)!** 🎯

**Then embed them in SHERPA for the complete platform!** ✨
