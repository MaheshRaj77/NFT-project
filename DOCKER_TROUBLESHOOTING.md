# 🐳 Docker Build Troubleshooting Guide

## Common Docker Build Issues & Solutions

### Issue 1: Pandas Compilation Failure
**Error Message:**
```
ninja: build stopped: subcommand failed
error: metadata-generation-failed
× Encountered error while generating package metadata.
```

**Cause**: Pandas requires compilation (Cython) and needs build tools and Python development headers.

**Solution Applied**:
✅ Dockerfile now includes:
- `build-essential` - C/C++ compilers
- `python3-dev` - Python development headers
- `pip install --upgrade pip setuptools wheel` - Latest build tools
- `--prefer-binary` flag - Use pre-built wheels when available

**If Still Having Issues**:
1. Use requirements_docker.txt instead of requirements_api.txt (same versions, optimized for Docker)
2. Switch to `python:3.14` (full image) instead of `python:3.14-slim` (adds 300MB but more stable)
3. Pre-build wheel locally and add to Docker

---

### Issue 2: "COPY data/ not found"
**Status**: ✅ FIXED in Dockerfile

The Dockerfile now creates the data directory at runtime instead of trying to copy it.

---

### Issue 3: Out of Memory During Build
**Error Message:**
```
killed: memory limit exceeded
```

**Solution**:
1. Increase Docker memory limit:
   - Docker Desktop Settings → Resources → Memory: Set to 4GB+
2. Use smaller base image (already using python:3.14-slim)
3. Build with `--progress=plain` for debugging:
   ```bash
   docker buildx build --progress=plain -t nft-analytics .
   ```

---

### Issue 4: Build Timeout
**Error Message:**
```
context deadline exceeded
```

**Solution**:
1. Increase timeout: `docker build --timeout 600s .`
2. Check network connectivity to pip repository
3. Pre-cache dependencies locally

---

## 📋 Docker Build Commands

### Build Locally (macOS)
```bash
# Using buildx (modern approach)
docker buildx build -t nft-analytics:latest --load .

# Or using docker build (traditional)
docker build -t nft-analytics:latest .
```

### Build with Progress Output
```bash
docker buildx build --progress=plain -t nft-analytics . | tee build.log
```

### Build with Cache Debugging
```bash
docker buildx build --progress=plain --no-cache -t nft-analytics .
```

### Run Container Locally
```bash
# Interactive testing
docker run -p 8000:8000 \
  -e API_KEY_APP1=c830a7c501571649da6563c4bf28c2f564ee0eef9b51c8e9ce534ad14cbea5ee \
  -e API_KEY_APP2=f5e8dd56e12121c78d5e88932e7709e97be5ff1643a4c98b3b874e94f0292c48 \
  -e DATA_URL_LEVEL3_CRYPTOPUNKS=https://drive.google.com/uc?export=download&id=... \
  nft-analytics

# In background
docker run -d -p 8000:8000 \
  --env-file .env \
  --name nft-api \
  nft-analytics

# Check logs
docker logs -f nft-api

# Stop container
docker stop nft-api
```

---

## 🔍 Debugging Tips

### Check Image Layers
```bash
# See all layers
docker image history nft-analytics

# See image size
docker images nft-analytics
```

### Inspect Dockerfile
```bash
# Validate Dockerfile syntax
docker run --rm -i hadolint/hadolint < Dockerfile
```

### Test venv Separately
```bash
# Create test Dockerfile to debug venv creation
cat > Dockerfile.test << 'EOF'
FROM python:3.14-slim
RUN apt-get update && apt-get install -y build-essential python3-dev
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --prefer-binary pandas==2.1.3 numpy==1.26.2
CMD ["python", "-c", "import pandas; print(f'✅ Pandas {pandas.__version__} loaded')"]
EOF

docker build -f Dockerfile.test -t test-pandas .
docker run --rm test-pandas
```

---

## 📊 Docker Build Optimization

### Current Optimizations Applied
1. ✅ Multi-stage build - reduces final image size
2. ✅ `--no-cache-dir` - pip doesn't cache wheels
3. ✅ `--prefer-binary` - avoids compilation when possible
4. ✅ `.dockerignore` - excludes unnecessary files
5. ✅ `rm -rf /var/lib/apt/lists/*` - removes apt cache

### Additional Optimizations (Optional)
```dockerfile
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t nft-analytics .

# Parallel pip install (experimental)
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver

# Use Docker cache mounts
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
```

---

## 🚀 Platform-Specific Build Tips

### Render.com
- Automatically handles Docker builds
- Uses native buildx with cache
- No intervention needed - just push to GitHub

### Railway
- Detects Dockerfile automatically
- Auto-selects build strategy
- Monitor build logs in dashboard

### GitHub Actions (if using CI/CD)
```yaml
- name: Build Docker Image
  uses: docker/build-push-action@v4
  with:
    context: .
    push: false
    tags: nft-analytics:latest
```

---

## 🔐 Security Considerations

- ✅ Non-root user in runtime stage (USER appuser)
- ✅ Read-only filesystem option available
- ✅ .dockerignore prevents secrets exposure
- ✅ No secrets in Dockerfile (use environment variables)

**IMPORTANT**: Never include .env file in Dockerfile or Docker image
- Store secrets in platform environment variables (Render/Railway dashboard)
- Use runtime environment variable substitution

---

## 📈 Build Performance Metrics

| Stage | Time | Optimization |
|-------|------|--------------|
| Pull base image | 5-10s | Cached locally |
| Install apt packages | 15-30s | `--no-install-recommends` used |
| Create venv | 5s | Lightweight |
| Pip upgrade | 10-15s | Once per build |
| Install requirements | 60-120s | `--prefer-binary` reduces |
| Copy app files | <1s | Small files |
| **Total** | **2-4 min** | Multi-stage optimized |

---

## ✅ Verification Checklist

After successful Docker build:

- [ ] Image builds without errors
- [ ] Image size is reasonable (<1GB)
- [ ] Container starts without errors
- [ ] Health endpoint responds (GET /api/health)
- [ ] API key authentication works
- [ ] Data loads from Google Drive
- [ ] No warnings or deprecations in logs

---

## 📞 Getting Help

If Docker build fails:

1. **Check Dockerfile syntax**
   ```bash
   docker run --rm -i hadolint/hadolint < Dockerfile
   ```

2. **Test base image**
   ```bash
   docker run -it python:3.14-slim bash
   apt-get update && apt-get install -y build-essential python3-dev
   ```

3. **Check disk space**
   ```bash
   docker system df
   ```

4. **Clean up Docker**
   ```bash
   docker system prune -a
   ```

5. **Review logs**
   ```bash
   docker buildx build --progress=plain -t nft-analytics . 2>&1 | tee build.log
   cat build.log | grep -i error
   ```

---

**Last Updated**: April 19, 2026  
**Status**: ✅ Docker build optimized for pandas compilation  
**Next**: Push to GitHub and deploy on Render.com

