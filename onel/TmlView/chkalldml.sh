#!/bin/sh
for i in $(ls dml/*dml); do ./main.py $i; done
