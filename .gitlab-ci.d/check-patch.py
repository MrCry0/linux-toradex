#!/usr/bin/env python3
#
# check-patch.py: run checkpatch.pl across all commits in a branch
#
# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: GPL-2.0-or-later

import os
import os.path
import sys
import subprocess

namespace = "linux-bsp"
if len(sys.argv) >= 2:
    namespace = sys.argv[1]

cwd = os.getcwd()
reponame = os.path.basename(cwd)
repourl = "https://gitlab.int.toradex.com/rd/%s/%s.git" % (namespace, reponame)
masterbranch = "toradex_5.4.y"

# GitLab CI environment does not give us any direct info about the
# base for the user's branch. We thus need to figure out a common
# ancestor between the user's branch and current git master.
subprocess.check_call(["git", "remote", "add", "check-patch", repourl])
subprocess.check_call(["git", "fetch", "check-patch", masterbranch],
                      stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL)

ancestor = subprocess.check_output(["git", "merge-base",
                                    "check-patch/" + masterbranch, "HEAD"],
                                    universal_newlines=True)

ancestor = ancestor.strip()

subprocess.check_call(["git", "remote", "rm", "check-patch"])

errors = False

print("\nChecking all commits since %s...\n" % ancestor)

ret = subprocess.run(["scripts/checkpatch.pl", "-g", ancestor + "..."])

if ret.returncode != 0:
    print(ret)
    print("    ❌ FAIL one or more commits failed scripts/checkpatch.pl")
    sys.exit(1)

sys.exit(0)
