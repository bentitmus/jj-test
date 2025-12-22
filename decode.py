#!/usr/bin/env python3
from math import ceil
from itertools import accumulate
import sys

def l2i(n):
  return ord(n) - 64

def bases(header: list[str]) -> tuple[int, int]:
  offset = int(header[0][0] + header[0][4] + header[0][6])
  divisor = int(header[1][1])
  base = l2i(header[2][0]) * l2i(header[2][1]) * l2i(header[2][2]) + l2i(header[2][3])
  odd_offset = l2i(header[3][2]) - l2i(header[3][0])
  even_offset = l2i(header[3][3]) - l2i(header[3][1])
  common = ceil(ceil(abs(base - offset) / divisor) / l2i(header[2][0]))
  so = (common + odd_offset - 1) % 26
  se = (common + even_offset - 1) % 26
  return (so, se)

def process(state: tuple[int, int, str], ciphertext: str) -> tuple[int, int, str]:
  if ciphertext == "OOO":
    return (state[0], state[1], " ")
  return (state[1], state[0], chr((state[0] + (1 if ciphertext[0] == "A" else -1) * int(ciphertext[1:])) % 26 + 65))

def decode(ciphertext: str) -> str:
  return "".join(
    [m for _, _, m in accumulate(
      ciphertext[5:-1],
      process,
      initial=(*bases(ciphertext[:4]), ""))
    ])

def rand_header() -> tuple[int, int, str]:
  return (0, 0, "MMMMM\n")

def encode(plaintext: str) -> str:
  so, se, header = rand_header()

with open(sys.argv[1]) as f:
  l = [r.strip() for r in f.readlines()]

print(decode(l))

