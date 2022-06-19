@echo off
color a
title Updating %CD%...
git fetch
git pull
echo Adding Files...
git add *
git commit -m "Updated Files"
git push