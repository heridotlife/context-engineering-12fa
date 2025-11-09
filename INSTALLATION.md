# Installation Quick Reference

> Quick guide for copying this template to your existing project

---

## TL;DR - Copy These Files

### Minimum Required (~810 KB, 95 files)

```bash
your-project/
├── CLAUDE.md              # Or GEMINI.md or COPILOT.md (pick one)
├── core/
│   ├── AGENTIC_GUIDE.md
│   └── SPEC_CLARIFICATIONS.md
├── implementations/
│   ├── factor-03-context-window/
│   ├── factor-05-state-management/
│   ├── factor-09-error-handling/
│   └── factor-10-focused-agents/
├── personas/
│   ├── PERSONA_CATALOG.md
│   └── agents/           # All 86 persona files
└── templates/
    └── SESSION_LOG.md
```

### Optional but Recommended (~31 KB, 6 files)

```bash
your-project/
├── schemas/              # Validation schemas
│   ├── README.md
│   ├── context-contract.json
│   ├── sample-context.json
│   ├── sample-context.toon
│   └── state-schema.json
└── 12-factor-agents/     # Reference docs
    └── README.md
```

---

## One-Line Install

### Method 1: Subdirectory (Recommended)

```bash
# Copy to .agentic/ subdirectory
mkdir -p .agentic && cp -r /path/to/template/{core,implementations,personas,templates,schemas,CLAUDE.md} .agentic/ && ln -s .agentic/CLAUDE.md CLAUDE.md
```

### Method 2: Root Directory

```bash
# Copy to project root
cp -r /path/to/template/{core,implementations,personas,templates,schemas,CLAUDE.md} .
```

### Method 3: Git Submodule

```bash
# Add as submodule (requires git)
git submodule add https://github.com/yourusername/context-engineering-12fa.git .agentic && ln -s .agentic/CLAUDE.md CLAUDE.md
```

---

## File Size Breakdown

| Component | Files | Size | Required |
|-----------|-------|------|----------|
| **Platform binding** | 1 file | 2 KB | ✅ YES |
| **Core specs** | 3 files | 36 KB | ✅ YES |
| **Implementations** | 4 dirs | 20 KB | ✅ YES |
| **Personas** | 87 files | 748 KB | ✅ YES |
| **Templates** | 1 file | 4 KB | ✅ YES |
| **Schemas** | 5 files | 28 KB | ⚠️ Optional |
| **Reference** | 1 file | 3 KB | ⚠️ Optional |
| **TOTAL (min)** | ~95 files | **~810 KB** | - |
| **TOTAL (rec)** | ~101 files | **~841 KB** | - |

---

## DO NOT Copy

❌ **Skip these files** (template-specific):

- `README.md` - Template README (write your own)
- `CHANGELOG.md` - Template history
- `MIGRATION_SUMMARY.md` - Template migration docs
- `AGENTIC_GUIDE.md.old` - Backup file
- `SESSION_LOG.md` (root) - Active session (use `templates/SESSION_LOG.md`)
- `.git/` - Template git history
- `scripts/` - Maintenance scripts
- `examples/` - Empty placeholder

---

## Quick Verification

After copying, verify with:

```bash
# Check essential files exist
test -f CLAUDE.md && echo "✅ Platform binding"
test -f core/AGENTIC_GUIDE.md && echo "✅ Master spec"
test -d personas/agents && echo "✅ Personas ($(ls -1 personas/agents/*.md 2>/dev/null | wc -l) files)"
test -f templates/SESSION_LOG.md && echo "✅ Session template"
test -d implementations && echo "✅ Implementations"

# Check optional files
test -d schemas && echo "⚠️ Schemas (optional)" || echo "❌ Schemas not copied (optional)"
```

Expected output:
```
✅ Platform binding
✅ Master spec
✅ Personas (86 files)
✅ Session template
✅ Implementations
⚠️ Schemas (optional)
```

---

## Post-Install Checklist

- [ ] Files copied to project
- [ ] Verified with quick verification script above
- [ ] Updated `core/AGENTIC_GUIDE.md` section 7 with project settings
- [ ] Added `.session-archive/` and `SESSION_LOG.md` to `.gitignore`
- [ ] Tested AI loads CLAUDE.md correctly
- [ ] (Optional) Validated context with `schemas/context-contract.json`

---

## Example: Python Project

```bash
# For Python project using FastAPI + pytest
cd my-fastapi-project/

# Install template
mkdir -p .agentic
cp -r ~/context-engineering-12fa/{core,implementations,personas,templates,schemas,CLAUDE.md} .agentic/
ln -s .agentic/CLAUDE.md CLAUDE.md

# Customize
cat >> .agentic/core/AGENTIC_GUIDE.md << 'EOF'

## 7. Project Customization

| Field | Value |
|-------|-------|
| Language/Framework | Python 3.12 + FastAPI |
| Build Tool | uv + ruff |
| Test Command | pytest tests/ -v |
| Common Commands | uv run dev, uv run test, uv run lint |
EOF

# Add to .gitignore
cat >> .gitignore << 'EOF'
.session-archive/
SESSION_LOG.md
EOF

# Verify
ls .agentic/core/AGENTIC_GUIDE.md && echo "✅ Installed"
```

---

## Example: Node.js Project

```bash
# For Node.js project using TypeScript + Jest
cd my-nodejs-app/

# Install template
cp -r ~/context-engineering-12fa/{core,implementations,personas,templates,schemas,CLAUDE.md} .

# Customize
cat >> core/AGENTIC_GUIDE.md << 'EOF'

## 7. Project Customization

| Field | Value |
|-------|-------|
| Language/Framework | Node.js 20 + TypeScript |
| Build Tool | npm + tsc |
| Test Command | npm test |
| Common Commands | npm run dev, npm run build, npm run lint |
EOF

# Add to .gitignore
echo ".session-archive/" >> .gitignore
echo "SESSION_LOG.md" >> .gitignore

# Verify
npm test  # AI should now follow 12FA principles
```

---

## Troubleshooting

### AI doesn't load CLAUDE.md

**Check**:
```bash
# Verify file exists at root
ls CLAUDE.md

# Check it references core/
grep "core/AGENTIC_GUIDE.md" CLAUDE.md
```

**Fix**: Ensure `CLAUDE.md` is at project root or create symlink

### "Persona not found" error

**Check**:
```bash
# Verify personas copied
ls personas/agents/*.md | wc -l
# Should show 88 files
```

**Fix**: Ensure entire `personas/agents/` directory copied

### SESSION_LOG.md not created

**Check**:
```bash
# Verify template exists
ls templates/SESSION_LOG.md
```

**Fix**: Copy `templates/` directory, AI creates SESSION_LOG.md from template automatically

---

## Need Help?

- **Full docs**: See `README.md` in this repo
- **Issues**: https://github.com/yourusername/context-engineering-12fa/issues
- **12FA Reference**: https://www.humanlayer.dev/12-factor-agents

---

**Quick Install**: `~1 minute` | **Total Size**: `~841 KB` | **Files**: `~101`
