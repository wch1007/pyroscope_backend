# Merge mtaruno/pyroscope into This Repo

This guide merges content from https://github.com/mtaruno/pyroscope (robot/ROS side) into the dashboard repo without overwriting existing frontend/backend.

## Option A: Merge into subfolder `robot/` (recommended)

Keeps robot code in one place; no conflict with our `src/` or `backend/`.

```powershell
cd "e:\launch project\pyroscope_dashboard"

# 1. Add upstream and fetch
git remote add upstream https://github.com/mtaruno/pyroscope.git
git fetch upstream

# 2. Read their tree and merge into robot/
git read-tree --prefix=robot/ -u upstream/main

# 3. Commit
git add robot/
git status   # review
git commit -m "Merge mtaruno/pyroscope into robot/ (ROS, navigation, application)"
```

Result: Your repo will have both:
- `src/`, `backend/` — dashboard + API (unchanged)
- `robot/` — upstream content (application/, catkin_ws/, src/ for ROS, etc.)

## Option B: Plain merge (may have conflicts)

```powershell
git remote add upstream https://github.com/mtaruno/pyroscope.git
git fetch upstream
git merge upstream/main -m "Merge upstream pyroscope (robot/ROS)"
```

- Both repos have a `src/` directory → **conflict**. You would need to:
  - Keep our `src/` (React) and move their ROS `src/` into e.g. `robot_src/` or `robot/src/`, or
  - Merge contents by hand.
- Their `application/` and our `backend/` are different backends; both can coexist if paths don’t clash.

## After merge

- **README**: Consider adding a short “Robot (ROS)” section that points to `robot/` and links to [mtaruno/pyroscope](https://github.com/mtaruno/pyroscope) for ROS/navigation docs.
- **.gitignore**: If you use Option A, ensure `robot/devel/`, `robot/build/` (and any large binaries) are ignored if desired.
