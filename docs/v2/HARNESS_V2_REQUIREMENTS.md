# autonomous-harness v2.0 - Requirements from SHERPA Build

**Source:** Learnings from SHERPA v1.0 build (165 features, 143 sessions)
**Date:** December 24, 2024

---

## 🎯 Critical Improvements Needed

### 1. File Organization Enforcement 🔴

**Problem Observed:**
- SHERPA created 150+ files in root directory
- test_*.html, SESSION_*.md, debug_*.js all scattered
- Required manual cleanup

**Root Cause:**
- No guidance in prompts about file organization
- Agent created files wherever convenient

**Solution:**
Add to both `initializer_prompt.md` and `coding_prompt.md`:

#### In initializer_prompt.md:
```markdown
## Project Structure (MANDATORY!)

Create this structure from the start:

```
project/
├── src/ or package_name/   # Source code
├── tests/                  # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .sessions/              # Session artifacts (gitignored)
├── scripts/                # Utility scripts
├── docs/                   # Documentation
└── (essential config files only in root)
```

Root directory limit: MAX 15 files
```

#### In coding_prompt.md:
```markdown
## After EVERY feature implementation:

**Check file organization:**

```bash
# Count root files
root_files=$(ls -1 | wc -l)

if [ "$root_files" -gt 15 ]; then
    echo "⚠️  Root directory has $root_files files!"
    echo "ORGANIZE NOW before continuing!"
    
    # Move to proper locations
    mkdir -p tests/manual tests/unit
    mkdir -p .sessions
    mkdir -p scripts/debug scripts/verify
    mkdir -p docs
    
    mv test_*.html tests/manual/
    mv test_*.py tests/unit/
    mv SESSION_*.md .sessions/
    mv debug_*.* scripts/debug/
    mv verify_*.* scripts/verify/
    mv *.md docs/ 2>/dev/null || true  # Keep README.md in root
    
    git add .
    git commit -m "chore: organize file structure"
fi
```

**Clean organization is NOT optional!**
```

---

### 2. Stop Condition 🔴

**Problem Observed:**
- SHERPA reached 165/165 ✅
- Agent continued working (Sessions 148-149)
- Added features beyond spec (keyboard shortcuts, tooltips)
- Risk of bugs, scope creep

**Root Cause:**
- Prompt says "Goal: All features passing"
- But doesn't say "STOP when goal achieved!"

**Solution:**
Add to `coding_prompt.md` as STEP 1 (before anything else):

```markdown
### STEP 1: CHECK COMPLETION STATUS (MANDATORY FIRST!)

**BEFORE doing anything else, check if project is complete:**

```bash
passing=$(grep -c '"passes": true' feature_list.json)
total=$(python -c "import json; print(len(json.load(open('feature_list.json'))))")

echo "Progress: $passing/$total features"

if [ "$passing" -eq "$total" ]; then
    echo "🎉 ALL $total FEATURES COMPLETE!"
    echo ""
    echo "✅ Application is DONE."
    echo "✅ All features implemented and tested."
    echo "✅ Ready for production deployment."
    echo ""
    echo "❌ DO NOT add features beyond the spec."
    echo "❌ DO NOT enhance or improve."
    echo "❌ DO NOT continue working."
    echo ""
    echo "Session complete. All features passing. Application ready."
    echo ""
    echo "If enhancements are needed, the human will create an enhancement spec."
    exit 0
fi
```

**Critical: If all features pass, say "Session complete" and STOP!**

Do NOT:
- Add features not in feature_list.json
- "Polish" or "improve" completed work
- Add "nice to have" features
- Continue working in any way

**The spec defines the scope. When scope is complete, STOP.**
```

---

### 3. TODO Prevention 🔴

**Problem Observed:**
- AutoGraph has 3 TODOs in features marked passing
- "Email sending" stubbed with TODO comments
- Features incomplete but marked done

**Root Cause:**
- No check for TODOs before marking passing
- Agent prioritizes progress over completeness

**Solution:**
Add to `coding_prompt.md`:

```markdown
### BEFORE marking "passes": true:

**Run TODO check:**

```bash
# Search for TODOs in this feature's code
if grep -r "TODO\|FIXME\|WIP\|HACK" src/ services/ --exclude-dir=node_modules | grep -v "test"; then
    echo "❌ CANNOT MARK PASSING - TODOs FOUND!"
    echo ""
    echo "Options:"
    echo "  1. Implement the TODO completely"
    echo "  2. Remove the TODO if not needed"
    echo "  3. Keep feature as 'passes': false"
    echo ""
    echo "Zero TODOs in passing features!"
    exit 1
fi
```

**A feature is NOT complete if code contains:**
- ❌ `TODO:` comments
- ❌ `FIXME:` comments
- ❌ `WIP:` comments
- ❌ `HACK:` comments
- ❌ "For now" or "temporary" comments
- ❌ Placeholder implementations

**If external dependency required (SMTP, payment gateway, etc.):**
- Implement with mock/test mode that actually works
- Document clearly in README
- But make it FUNCTIONAL, not a TODO

**Only mark "passes": true when 100% implemented!**
```

---

### 4. .gitignore Template 🟡

**Learning:**
SHERPA needed comprehensive .gitignore

**Solution:**
Add to `initializer_prompt.md`:

```markdown
## Create .gitignore

**Comprehensive exclusions:**

```
# Python
__pycache__/
*.py[cod]
venv/
.venv/
*.db
*.db-journal

# Node
node_modules/
dist/
.next/

# Logs (NEVER commit!)
logs/
*.log

# Sessions (build artifacts)
.sessions/
SESSION_*.md

# Tests (generated)
*_verification.html
test_results*/

# IDE
.vscode/
.idea/

# OS  
.DS_Store
```
```

---

### 5. Test Organization 🟡

**Problem:**
Tests created wherever (root, random locations)

**Solution:**
```markdown
## Test File Naming and Location

**ALL test files MUST go in tests/ directory!**

```
tests/
├── unit/
│   └── test_*.py
├── integration/
│   └── test_*_integration.py
├── e2e/
│   └── *.spec.js (Playwright)
└── manual/
    └── verify_*.html
```

**NEVER create:**
- test_*.py in root ❌
- test_*.html in root ❌
- verify_*.js in root ❌

**Always:**
- tests/unit/test_feature.py ✅
- tests/manual/verify_feature.html ✅
```

---

### 6. Session Summary Organization 🟡

**Problem:**
50+ SESSION_*.md files in root

**Solution:**
```markdown
## Session Documentation

**Location:** `.sessions/` directory

```
.sessions/
├── feature_list.json
├── claude-progress.txt (or cursor-progress.txt)
├── SESSION_001_SUMMARY.md
├── SESSION_002_SUMMARY.md
└── ...
```

**Add to .gitignore:**
```
.sessions/
```

**Session artifacts are build history, not source code!**
```

---

### 7. Script Organization 🟡

**Learning:**
Debug, verify, test scripts scattered

**Solution:**
```markdown
## Utility Scripts

```
scripts/
├── debug/           # Debug utilities
│   └── debug_*.js
├── verify/          # Verification scripts
│   └── verify_*.sh
├── tests/           # Test runners
│   └── test_*.py
└── (named scripts at root)
    └── migrate_db.py
```
```

---

## 📊 Implementation Priority

### Phase 1: Critical Fixes (v2.0)
1. 🔴 Stop condition (STEP 1 in prompt)
2. 🔴 File organization rules (enforce in prompt)
3. 🔴 TODO prevention (check before marking passing)
4. 🔴 Comprehensive .gitignore

**Estimated time:** 2-3 hours
**Impact:** Prevents all major issues seen in SHERPA!

### Phase 2: Quality Enhancements (v2.0)
5. 🟡 Session artifact organization (.sessions/)
6. 🟡 Test file organization (tests/ structure)
7. 🟡 Script organization (scripts/ structure)

**Estimated time:** 1-2 hours
**Impact:** Professional file organization

### Phase 3: Documentation (v2.0)
8. 🟢 Python package structure guidance
9. 🟢 Best practices documentation

**Estimated time:** 1 hour
**Impact:** Better quality projects

---

## 🎯 Expected Results

**With these improvements:**

**Before (SHERPA experience):**
- 150+ files in root → Manual cleanup needed
- Agent continued after 100% → Manual stop needed
- Messy organization → Manual organization needed

**After (autonomous-harness v2.0):**
- ✅ Max 15 files in root (enforced!)
- ✅ Agent stops at 100% (automatic!)
- ✅ Clean organization (from start!)
- ✅ Zero TODOs in passing features
- ✅ Professional from day one!

---

## 🔄 Sync to SHERPA

**After implementing in autonomous-harness:**
1. Update SHERPA's harness code (sherpa/core/harness/)
2. Test with SHERPA
3. Release SHERPA v1.1 with improved harness

---

**These learnings are GOLD!** Apply them to make autonomous-harness v2.0 amazing! 🚀

